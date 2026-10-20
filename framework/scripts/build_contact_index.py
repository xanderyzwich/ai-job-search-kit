#!/usr/bin/env python3
"""Build the contact index and the calendar — who you know, how cold, who brought whom, and what is coming when.

Generated at session start from the contact files themselves, never
hand-maintained, for the same reason the context map is: a hand-kept index of
anything goes stale the first busy week and is then believed anyway.

WHY THIS EXISTS. The funnel in one real instance read 9 advances, 7 of them
sourced by a person, against roughly 180 board applications producing 2. When
the people channel is the one that works, "who do I know and who has gone
quiet" stops being bookkeeping and becomes the search. It was unanswerable
without grepping, and the cost showed: a referral list of nine warm
introductions sat untouched for three months, including one contact who had
volunteered a weekly cadence and a direct phone channel. One of those nine had
already produced an interview. Nobody could see the list as a list.

THE AGE COLUMN IS THE POINT, AND IT IS WHY FILES CARRY A DATE AND NOT A
DURATION. A contact file records `Last touch | YYYY-MM-DD`. The days are
computed here, every run. Writing "85 days ago" into the file instead makes a
number that is wrong tomorrow and misleading next month -- the same mirror
problem the ripple map exists to prevent.

REFERRAL PROVENANCE IS READ FROM BOTH ENDS. A file says who referred it; this
builds the reverse edge so a hub's yield is visible without anyone maintaining
a tally. That is the difference between "I met nine recruiters once" and "this
person has produced two of my nine advances."

WHAT THIS DOES NOT DO: it does not decide who is overdue. Pacing is a fact
about a relationship, not a category -- see
framework/skills/communications/communication-logging.md. The index reports
elapsed time and lets a person judge it.

THE CALENDAR IS THE SECOND OUTPUT AND IT EXISTS BECAUSE A SCALAR CANNOT HOLD
A LOOP. `next_contact` is one field; a four-stage interview round with an
assessment deadline beside it is a list. Collapsing them lost the stages that
had no date yet -- the exact ones most likely to be forgotten -- so commitments
and deadlines moved to a parsed `## Scheduled` block and this renders them.
UNPARSEABLE LINES ARE REPORTED, NEVER DROPPED: a malformed frontmatter entry
becomes a garbage key nobody ever sees again, and that failure is the reason
the schedule is a body block at all.

Usage: build_contact_index.py [--out PATH] [--cal-out PATH]
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CONTACTS = ROOT / "private" / "data" / "contacts"
DEFAULT_OUT = ROOT / "private" / "temp" / "contact_index.md"
DEFAULT_CAL = ROOT / "private" / "temp" / "calendar.md"
COMPANIES = ROOT / "private" / "data" / "companies"
OPEN_THREADS = ROOT / "private" / "data" / "open_threads.md"

SCHED_RE = re.compile(r"^##+\s+Scheduled\s*$", re.M)
COMMENT = re.compile(r"<!--.*?-->", re.S)
EVENT = re.compile(
    r"^\s*-\s+"
    r"(?P<when>TBD"
    r"|DUE\s+\d{4}-\d{2}-\d{2}"
    r"|\d{4}-\d{2}-\d{2}(?:\s+\d{1,2}:\d{2}(?:\s*[^|]*?)?)?)"
    r"\s*\|\s*(?P<kind>[A-Z][A-Z0-9_-]*)"
    r"\s*\|\s*(?P<who>[^|]*?)"
    r"\s*(?:\|\s*(?P<note>.*?))?\s*$")
# open-items hard dates stay PROSE on purpose -- only a leading bold date is
# read, and anything else in that section is simply not an event.
THREAD_DATE = re.compile(r"^\s*-\s+\*\*~?(\d{4}-\d{2}-\d{2})(?P<inbold>[^*]*)\*\*\s*(?P<rest>.*)$")

FM = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
DATE = re.compile(r"^(\d{4}-\d{2}-\d{2})$")


def read(p):
    """Parse a contact record's YAML frontmatter.

    Hand-rolled rather than PyYAML on purpose: the frontmatter is flat
    key/value scalars by contract (see framework/templates/contact_record.md),
    and a public framework someone clones should not acquire a dependency for
    fifteen lines of parsing.

    A key present with an empty value is MEANINGFUL and is not the same as a
    missing key -- `next_contact:` with nothing after it means "no date set",
    which the index reports as undecided rather than at rest.
    """
    text = p.read_text(encoding="utf-8")
    m = FM.match(text)
    f = {}
    if m:
        for line in m.group(1).splitlines():
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            k, sep, v = line.partition(":")
            if sep:
                f[k.strip().lower()] = v.strip()
    name = f.get("name") or next(
        (l[2:].strip() for l in text.splitlines() if l.startswith("# ")), p.stem)
    ref = None
    mm = re.search(r"Referred BY[:,]?\s*\**\s*\[([^\]]+)\]", text, re.I)
    if mm:
        ref = mm.group(1).strip()
    last = f.get("last_contact", "").strip()
    return dict(file=p.name, name=name, fields=f, referred_by=ref,
                last=last if DATE.match(last) else None)


def days_since(iso, today):
    y, m, d = map(int, iso.split("-"))
    return (today - date(y, m, d)).days


def strip_md(s, n=58):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s or "")
    s = s.replace("**", "").replace("`", "").strip()
    return (s[: n - 1] + "…") if len(s) > n else s


def title_of(path, text):
    """A short source label: the H1 up to its first dash, else the filename."""
    for line in text.splitlines():
        if line.startswith("# "):
            return re.split(r"\s+(?:—|--)\s+", line[2:].strip())[0].strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def scheduled_block(text):
    """Lines between a `## Scheduled` heading and the next heading."""
    m = SCHED_RE.search(text)
    if not m:
        return []
    rest = text[m.end():]
    end = re.search(r"^#{1,3}\s+\S", rest, re.M)
    return (rest[: end.start()] if end else rest).splitlines()


def parse_events(path, today):
    """Return (events, malformed) for one record file."""
    text = COMMENT.sub("", path.read_text(encoding="utf-8"))
    src = title_of(path, text)
    events, bad = [], []
    for line in scheduled_block(text):
        if not line.strip() or line.lstrip().startswith(("#", ">")):
            continue
        m = EVENT.match(line)
        if not m:
            if line.lstrip().startswith("-"):
                bad.append((src, path, line.strip()))
            continue
        when = m.group("when").strip()
        iso, due = None, when.upper().startswith("DUE")
        dm = re.search(r"\d{4}-\d{2}-\d{2}", when)
        if dm:
            iso = dm.group(0)
        tm = re.search(r"\d{1,2}:\d{2}\s*\S*", when)
        events.append(dict(
            iso=iso, due=due, time=(tm.group(0).strip() if tm else ""),
            kind=m.group("kind"), who=strip_md(m.group("who") or "", 40),
            note=strip_md(m.group("note") or "", 72), src=src, path=path))
    return events, bad


def thread_dates():
    """Dated lines from the open-items file's hard-dates section."""
    if not OPEN_THREADS.exists():
        return []
    text = OPEN_THREADS.read_text(encoding="utf-8")
    m = re.search(r"^##\s+\d+\.\s+Hard dates\s*$", text, re.M)
    if not m:
        return []
    rest = text[m.end():]
    end = re.search(r"^##\s+\S", rest, re.M)
    out = []
    for line in (rest[: end.start()] if end else rest).splitlines():
        d = THREAD_DATE.match(line)
        if not d:
            continue
        label = (d.group("rest") or d.group("inbold") or "").strip(" —-,.")
        out.append(dict(iso=d.group(1), due=False, time="", kind="NOTE",
                        who="", note=strip_md(label, 72),
                        src="open threads §3", path=None))
    return out


def link(e):
    if e["path"] is None:
        return e["src"]
    rel = "companies" if e["path"].parent.name == "companies" else "contacts"
    return "[%s](../data/%s/%s)" % (e["src"], rel, e["path"].name)


def render_calendar(today, cal_out):
    events, bad = [], []
    for d in (CONTACTS, COMPANIES):
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                ev, bd = parse_events(f, today)
                events += ev
                bad += bd
    events += thread_dates()

    dated = sorted([e for e in events if e["iso"]], key=lambda e: (e["iso"], e["time"]))
    undated = [e for e in events if not e["iso"]]
    busy = {}
    for e in dated:
        busy[e["iso"]] = busy.get(e["iso"], 0) + 1

    L = ["# Calendar (generated %s)" % today.isoformat(), "",
         "> GENERATED by framework/scripts/build_contact_index.py from the",
         "> `## Scheduled` blocks of the contact and company records. Do NOT edit —",
         "> **fix the block and regenerate.** Rescheduling changes one line;",
         "> cancelling REMOVES the line and the reason goes in that file's log.", ""]

    def emit(title, rows, note=None):
        if not rows:
            return
        L.append("## %s" % title)
        L.append("")
        for e in rows:
            days = days_since(e["iso"], today) if e["iso"] else None
            when = (e["iso"] or "**TBD**") + (" " + e["time"] if e["time"] else "")
            tag = "**DUE**" if e["due"] else ""
            extra = []
            if days is not None and days > 0:
                extra.append("**%dd overdue**" % days)
            if e["iso"] and busy.get(e["iso"], 0) > 1:
                extra.append("⚠ %d items this day" % busy[e["iso"]])
            bits = [b for b in [tag, "`%s`" % e["kind"], link(e),
                                e["who"], e["note"]] + extra if b]
            L.append("- %s — %s" % (when, " · ".join(bits)))
        if note:
            L.extend(["", note])
        L.append("")

    emit("PASSED, NOT RESOLVED",
         [e for e in dated if days_since(e["iso"], today) > 0],
         "**A date that passed is not a date that happened.** Each of these is "
         "either held (move it out of the block) or dropped (remove it and say "
         "why in the log). Leaving it here is the third option and it is the "
         "one that reads as neglect.")
    week = [e for e in dated if 0 >= days_since(e["iso"], today) >= -6]
    emit("THIS WEEK", week)
    emit("UPCOMING", [e for e in dated if days_since(e["iso"], today) < -6])
    emit("UNDATED BUT SEQUENCED", undated,
         "**These are real stages with no date yet** — the ones a chronological "
         "view has nowhere to put and therefore loses. Two stacked on one thread "
         "is a stall, not a schedule.")

    if bad:
        L += ["## DIDN'T PARSE", ""]
        for src, path, line in bad:
            L.append("- %s — `%s`" % (src, line[:100]))
        L += ["", "Expected `- <WHEN> | <KIND> | <WHO> | <NOTE>` — see "
              "framework/templates/contact_record.md.", ""]

    if not events:
        L += ["*No `## Scheduled` blocks found.* Add one to a contact record or "
              "company brief; the grammar is in the templates.", ""]

    cal_out.parent.mkdir(parents=True, exist_ok=True)
    cal_out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote %s: %d dated, %d undated, %d unparsed."
          % (cal_out.relative_to(ROOT), len(dated), len(undated), len(bad)))


def main():
    out = Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else DEFAULT_OUT
    cal = Path(sys.argv[sys.argv.index("--cal-out") + 1]) if "--cal-out" in sys.argv else DEFAULT_CAL
    render_calendar(date.today(), cal)
    if not CONTACTS.is_dir():
        print("No private/data/contacts/ directory — nothing to index.")
        return 0
    today = date.today()
    cs = [read(p) for p in sorted(CONTACTS.glob("*.md"))]
    if not cs:
        print("contact index: no contact files found.")
        return 0

    brought = {}
    for c in cs:
        if c["referred_by"]:
            brought.setdefault(c["referred_by"], []).append(c)

    def agedays(c):
        return days_since(c["last"], today) if c["last"] else -1

    L = ["# Contact Index (generated %s)" % today.isoformat(), "",
         "> GENERATED by framework/scripts/build_contact_index.py from the contact",
         "> files themselves. Do NOT edit — fix the contact file and regenerate.",
         "> **Elapsed days are computed here; the files carry only a date.**", ""]

    owed, due = [], []
    for c in cs:
        na = c["fields"].get("next_action") or ""
        sched = (c["fields"].get("next_contact") or "").strip()
        d = DATE.match(sched)
        if d:
            due.append((sched, c, na))
        elif na:
            owed.append(c)   # an action with no date = undecided

    if due or owed:
        L += ["## NEEDS A DECISION OR AN ACTION", ""]
        for iso, c, na in sorted(due, key=lambda x: x[0]):
            flag = "**DUE %s**" % iso if days_since(iso, today) >= 0 else "scheduled %s" % iso
            L.append("- %s — [%s](../data/contacts/%s): %s" % (
                flag, c["name"], c["file"], strip_md(na, 88)))
        for c in sorted(owed, key=agedays, reverse=True):
            a = "%d days since last contact" % agedays(c) if c["last"] else "no date on file"
            L.append("- **no date set** — [%s](../data/contacts/%s), %s: %s" % (
                c["name"], c["file"], a, strip_md(c["fields"].get("next_action", ""), 76)))
        L += ["",
              "**A contact with no next-action date is NOT at rest — it is undecided.**",
              "Deliberate inaction is recorded as `Next action: NONE` with its reason, which",
              "is what keeps a later session from inventing a chase nobody wanted.", ""]

    L += ["## By time since last contact", "",
          "| days | contact | owed | next action | who |", "|---:|---|---|---|---|"]
    for c in sorted(cs, key=agedays, reverse=True):
        d = "%d" % agedays(c) if c["last"] else "?"
        L.append("| %s | [%s](../data/contacts/%s) | %s | %s | %s |" % (
            d, c["name"], c["file"], c["fields"].get("owed_by", "?"),
            strip_md(c["fields"].get("next_action", ""), 46),
            strip_md(c["fields"].get("company") or c["fields"].get("role", ""), 28)))

    L += ["", "## Referral provenance — who brought whom", ""]
    if brought:
        for hub, kids in sorted(brought.items(), key=lambda kv: -len(kv[1])):
            L.append("**%s — %d contact(s)**" % (hub, len(kids)))
            for k in sorted(kids, key=agedays, reverse=True):
                a = "%d days" % agedays(k) if k["last"] else "unknown"
                L.append("  - [%s](../data/contacts/%s) — %s — %s" % (
                    k["name"], k["file"], a, strip_md(k["fields"].get("note", ""), 66)))
            L.append("")
    else:
        L.append("*No referral edges recorded yet.*\n")

    orphans = [c for c in cs if not c["referred_by"] and c["name"] not in brought]
    if orphans:
        L += ["**No recorded source and no onward referrals:** "
              + ", ".join(c["name"] for c in orphans), ""]

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote %s: %d contacts, %d needing a decision, %d referral hub(s)."
          % (out.relative_to(ROOT), len(cs), len(owed) + len(due), len(brought)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
