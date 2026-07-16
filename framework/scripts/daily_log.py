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

Notes:
  - close stages the whole working tree (git add -A), on purpose: the daily
    commit carries the day's tracker edits and regenerated views together.
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
ARCHIVE_DAYS = 21

HEADER_RE = re.compile(r"^## Session Notes \((\w{3} \d{1,2} \d{4})", re.M)


def load_rituals():
    if not RITUALS.exists():
        return {}
    import yaml
    return yaml.safe_load(RITUALS.read_text(encoding="utf-8")) or {}


def ritual_warnings():
    lines = []
    for name, info in load_rituals().items():
        if not isinstance(info, dict):
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
    import yaml
    data = load_rituals()
    if name not in data:
        known = ", ".join(data) or "(none — seed data/rituals.yml first)"
        sys.exit(f"Unknown ritual '{name}'. Known: {known}")
    data[name]["last_run"] = date.today().isoformat()
    header = ("# Last-run stamps for non-daily rituals (machine-managed).\n"
              "# daily_log.py open/status warn when cadence_days has"
              " elapsed;\n# stamp with: daily_log.py ritual <name>."
              " cadence_days null = on demand.\n")
    RITUALS.write_text(header + yaml.safe_dump(data, sort_keys=False),
                       encoding="utf-8")
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


def cmd_open():
    TODAY_FILE.parent.mkdir(exist_ok=True)
    refresh_context_map()  # always refresh, even on re-open
    if TODAY_FILE.exists():
        print(f"{TODAY_FILE.relative_to(ROOT)} already exists; append to it.")
        return
    TODAY_FILE.write_text(
        f"## Session Notes ({today_header_date()})\n\n", encoding="utf-8")
    print(f"Created {TODAY_FILE.relative_to(ROOT)}")


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
