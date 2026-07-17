#!/usr/bin/env python3
"""Daily session-log tool: split/assemble plus one commit per day.

Workflow:
  open    create temp/today.md, a cheap working file for the day's entries —
          append session notes there during the day instead of editing the
          full log. Also refreshes temp/context_map.md (skill routing + the
          ripple map) so "what to touch when" is in context from the start.
  close   fold temp/today.md into the top of data/session_log.md, archive
          entries older than ARCHIVE_DAYS into data/archive/YYYY-MM.md,
          regenerate data/application_history.md, then stage everything and
          commit as the single daily commit "log: YYYY-MM-DD" — amending
          today's commit if it exists and hasn't been pushed yet
  status  show whether a working file and/or today's commit exist
  ritual NAME
          stamp a non-daily ritual as run today in data/rituals.yml —
          e.g. `daily_log.py ritual weekly_review`

`open` and `status` also print overdue warnings for any ritual in
data/rituals.yml whose cadence_days has elapsed since its last_run, so a
skipped weekly ritual announces itself at session start instead of waiting
to be discovered.

Weekly review — anchored to Friday's close (not a rolling 7-day timer):
  A ritual carrying `anchor: <weekday>` in rituals.yml (weekly_review =
  friday) is "due" whenever its last_run predates the most recent occurrence
  of that weekday. So the weekly review comes due every Friday and STAYS due
  until it runs — a skipped Friday simply carries forward. When `close` runs
  and the weekly review is due, close first runs the funnel report, writes
  data/funnel_report.md, stamps weekly_review, and makes its OWN commit
  ("weekly-review: YYYY-MM-DD") — separate from the daily "log:" commit that
  follows. `open` flags the weekly review when it's due so the next session
  picks up a missed Friday and closes it out.

Notes:
  - close stages the whole working tree (git add -A), on purpose: the daily
    commit carries the day's tracker edits and regenerated views together.
    The weekly-review commit is made first and stages only its own two
    artifacts (data/funnel_report.md, data/rituals.yml) so it stays distinct.
  - Remote pushes still happen through GitKraken; this script only makes
    local commits. Amending stops automatically once today's commit has
    been pushed (a pushed commit gets an addendum commit instead).

Usage: python3 scripts/daily_log.py {open|close|status}
"""
import re
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "session_log.md"
TODAY_FILE = ROOT / "temp" / "today.md"
ARCHIVE_DIR = ROOT / "data" / "archive"
RITUALS = ROOT / "data" / "rituals.yml"
FUNNEL_MD = ROOT / "data" / "funnel_report.md"
ARCHIVE_DAYS = 21

HEADER_RE = re.compile(r"^## Session Notes \((\w{3} \d{1,2} \d{4})", re.M)

ANCHOR_WEEKDAYS = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
                   "friday": 4, "saturday": 5, "sunday": 6}

RITUAL_HEADER = (
    "# Last-run stamps for non-daily rituals (machine-managed).\n"
    "# daily_log.py open/status warn when cadence_days has elapsed;\n"
    "# stamp with: daily_log.py ritual <name>. cadence_days null = on demand.\n"
    "# anchor: <weekday> makes a ritual due-by-weekday (weekly_review = friday);\n"
    "# it runs and is committed separately at that day's `close`.\n")


def load_rituals():
    if not RITUALS.exists():
        return {}
    import yaml
    return yaml.safe_load(RITUALS.read_text(encoding="utf-8")) or {}


def write_rituals(data):
    import yaml
    RITUALS.write_text(RITUAL_HEADER + yaml.safe_dump(data, sort_keys=False),
                       encoding="utf-8")


def stamp_ritual(name):
    """Set a ritual's last_run to today. Returns True if the name existed."""
    data = load_rituals()
    if name not in data or not isinstance(data[name], dict):
        return False
    data[name]["last_run"] = date.today().isoformat()
    write_rituals(data)
    return True


def most_recent_weekday(weekday, ref=None):
    """Date of the most recent given weekday (Mon=0..Sun=6) on or before ref."""
    ref = ref or date.today()
    return ref - timedelta(days=(ref.weekday() - weekday) % 7)


def anchored_due(info, ref=None):
    """True if a weekday-anchored ritual's last_run predates the most recent
    occurrence of its anchor weekday (i.e. this week's — or a missed earlier
    week's — instance hasn't run yet)."""
    weekday = ANCHOR_WEEKDAYS.get(str(info.get("anchor", "")).lower())
    if weekday is None:
        return False
    anchor_date = most_recent_weekday(weekday, ref)
    last = info.get("last_run")
    return last is None or date.fromisoformat(str(last)) < anchor_date


def weekly_review_due(ref=None):
    info = load_rituals().get("weekly_review")
    return (isinstance(info, dict) and bool(info.get("anchor"))
            and anchored_due(info, ref))


def ritual_warnings():
    lines = []
    for name, info in load_rituals().items():
        if not isinstance(info, dict):
            continue
        if info.get("anchor"):
            if anchored_due(info):
                weekday = ANCHOR_WEEKDAYS[str(info["anchor"]).lower()]
                anchor_date = most_recent_weekday(weekday)
                last = info.get("last_run") or "never"
                lines.append(
                    f"!! ritual '{name}' due (anchored to {info['anchor']}):"
                    f" last run {last}; anchor {anchor_date}."
                    f" Runs + commits at the next `close`.")
            continue
        cadence = info.get("cadence_days")
        if not cadence:
            continue  # on-demand rituals are stamped for reference only
        last = info.get("last_run")
        if last is None:
            lines.append(f"!! ritual '{name}' has never run"
                         f" (cadence: every {cadence}d)")
            continue
        days = (date.today() - date.fromisoformat(str(last))).days
        if days > cadence:
            lines.append(f"!! ritual '{name}' overdue: last run {last}"
                         f" ({days}d ago, cadence {cadence}d)")
    return lines


def print_ritual_warnings():
    for line in ritual_warnings():
        print(line)


def cmd_ritual(name):
    data = load_rituals()
    if name not in data:
        known = ", ".join(data) or "(none — seed data/rituals.yml first)"
        sys.exit(f"Unknown ritual '{name}'. Known: {known}")
    stamp_ritual(name)
    print(f"Stamped '{name}': {date.today().isoformat()}")


def git(*args, check=True):
    return subprocess.run(["git", *args], cwd=ROOT, check=check,
                          capture_output=True, text=True)


def today_header_date():
    return date.today().strftime("%b ") + str(date.today().day) \
        + date.today().strftime(" %Y")


def commit_message():
    return f"log: {date.today().isoformat()}"


def parse_header_date(text):
    return datetime.strptime(text, "%b %d %Y").date()


def refresh_context_map():
    """Best-effort: rebuild temp/context_map.md (skill routing + ripple map)
    via the framework script, so the 'when to do what' reference is current in
    context from the first moment of the session. Never blocks session start."""
    script = ROOT.parent / "framework" / "scripts" / "build_context_map.py"
    if not script.exists():
        return
    try:
        result = subprocess.run([sys.executable, str(script)], check=False,
                                capture_output=True, text=True)
        first = (result.stdout or "").strip().splitlines()
        if first:
            print(first[0])
    except Exception:
        pass


def run_weekly_review():
    """Friday-anchored weekly review, run as part of `close` but committed on
    its own. Refreshes the funnel report into data/funnel_report.md, stamps
    weekly_review, and commits just those two artifacts as
    "weekly-review: YYYY-MM-DD" — separate from the daily "log:" commit.

    The judgment steps of the review (staleness sweeps, open-thread date scan;
    see framework/skills/search-apply-ritual.md) are done in-session before
    close; this formalizes the measurable, stampable part."""
    funnel = ROOT.parent / "framework" / "scripts" / "funnel_report.py"
    output = ""
    if funnel.exists():
        try:
            result = subprocess.run([sys.executable, str(funnel)], check=False,
                                    capture_output=True, text=True)
            output = (result.stdout or "").strip()
        except Exception:
            output = ""
    header = (f"# Weekly Funnel Report\n\n"
              f"_Generated {date.today().isoformat()} at the Friday weekly"
              f" close. Regenerated view — do not hand-edit; it is rewritten"
              f" each time `close` runs on/after a due Friday._\n\n")
    FUNNEL_MD.parent.mkdir(parents=True, exist_ok=True)
    FUNNEL_MD.write_text(header + "```\n" + output + "\n```\n", encoding="utf-8")
    stamp_ritual("weekly_review")

    git("add", str(FUNNEL_MD), str(RITUALS))
    if git("diff", "--cached", "--quiet", check=False).returncode != 0:
        git("commit", "-m", f"weekly-review: {date.today().isoformat()}")
        print(f"Weekly review: funnel refreshed + stamped; committed"
              f" (weekly-review: {date.today().isoformat()}).")
    else:
        print("Weekly review ran; no artifact changes to commit.")
    if output:
        print("\n" + output)


def cmd_open():
    TODAY_FILE.parent.mkdir(exist_ok=True)
    refresh_context_map()  # always refresh, even on re-open
    if TODAY_FILE.exists():
        print(f"{TODAY_FILE.relative_to(ROOT)} already exists; append to it.")
    else:
        TODAY_FILE.write_text(
            f"## Session Notes ({today_header_date()})\n\n", encoding="utf-8")
        print(f"Created {TODAY_FILE.relative_to(ROOT)}")
    if weekly_review_due():
        print("NOTE: weekly review is due (Friday-anchored). Do the staleness"
              " sweeps in-session, then run `close` — it will run the funnel,"
              " stamp the ritual, and make its own weekly-review commit.")


def fold_today():
    """Insert temp/today.md above the newest log entry. True if folded."""
    if not TODAY_FILE.exists():
        return False
    body = TODAY_FILE.read_text(encoding="utf-8").strip()
    if not body or body == f"## Session Notes ({today_header_date()})":
        TODAY_FILE.unlink()
        return False
    log_text = LOG.read_text(encoding="utf-8")
    match = re.search(r"^## Session Notes", log_text, re.M)
    idx = match.start() if match else len(log_text)
    LOG.write_text(log_text[:idx] + body + "\n\n" + log_text[idx:],
                   encoding="utf-8")
    TODAY_FILE.unlink()
    return True


def archive_old():
    """Move whole entries older than ARCHIVE_DAYS to monthly archive files.

    Entries are newest-first, so everything from the first too-old header to
    the end of the file gets moved. Returns the number of entries archived.
    """
    cutoff = date.today() - timedelta(days=ARCHIVE_DAYS)
    text = LOG.read_text(encoding="utf-8")
    split_at = None
    for match in HEADER_RE.finditer(text):
        try:
            if parse_header_date(match.group(1)) < cutoff:
                split_at = match.start()
                break
        except ValueError:
            continue
    if split_at is None:
        return 0

    old, kept = text[split_at:], text[:split_at].rstrip() + "\n"
    LOG.write_text(kept, encoding="utf-8")
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    headers = list(HEADER_RE.finditer(old))
    count = 0
    for i, match in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(old)
        try:
            entry_date = parse_header_date(match.group(1))
        except ValueError:
            entry_date = cutoff
        dest = ARCHIVE_DIR / f"{entry_date:%Y-%m}.md"
        with open(dest, "a", encoding="utf-8") as f:
            f.write(old[match.start():end].rstrip() + "\n\n")
        count += 1
    return count


def head_is_todays_log_commit():
    result = git("log", "-1", "--pretty=%s", check=False)
    return result.stdout.strip() == commit_message()


def head_is_pushed():
    upstream = git("rev-parse", "--abbrev-ref", "@{u}", check=False)
    if upstream.returncode != 0:
        return False  # no upstream configured — safe to amend
    contained = git("merge-base", "--is-ancestor", "HEAD",
                    upstream.stdout.strip(), check=False)
    return contained.returncode == 0


def cmd_close():
    if weekly_review_due():
        run_weekly_review()  # its own commit, before the daily commit

    folded = fold_today()
    archived = archive_old()
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_history.py")],
        check=True)

    git("add", "-A")
    if git("diff", "--cached", "--quiet", check=False).returncode == 0:
        print("Nothing to commit.")
        return
    if head_is_todays_log_commit() and not head_is_pushed():
        git("commit", "--amend", "-m", commit_message())
        print(f"Amended today's commit ({commit_message()}).")
    elif head_is_todays_log_commit():
        git("commit", "-m", f"{commit_message()} (addendum — earlier commit"
            " already pushed)")
        print("Today's commit was already pushed; created an addendum.")
    else:
        git("commit", "-m", commit_message())
        print(f"Created commit ({commit_message()}).")
    if folded:
        print("Folded temp/today.md into the log.")
    if archived:
        print(f"Archived {archived} old log entries to data/archive/.")


def cmd_status():
    if TODAY_FILE.exists():
        lines = TODAY_FILE.read_text(encoding="utf-8").count("\n")
        print(f"Working file: {TODAY_FILE.relative_to(ROOT)} ({lines} lines)")
    else:
        print("No working file (run 'open' to create one).")
    if head_is_todays_log_commit():
        pushed = "pushed" if head_is_pushed() else "not pushed (will amend)"
        print(f"Today's commit exists: {commit_message()} — {pushed}")
    else:
        print("No commit for today yet.")
    print_ritual_warnings()


def main():
    args = sys.argv[1:]
    if args and args[0] == "ritual":
        if len(args) != 2:
            sys.exit("usage: daily_log.py ritual <name>")
        cmd_ritual(args[1])
        return
    commands = {"open": cmd_open, "close": cmd_close, "status": cmd_status}
    if len(args) != 1 or args[0] not in commands:
        print(__doc__)
        sys.exit(1)
    commands[args[0]]()
    if args[0] == "open":
        print_ritual_warnings()


if __name__ == "__main__":
    main()
