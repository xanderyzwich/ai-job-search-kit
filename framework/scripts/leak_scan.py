#!/usr/bin/env python3
"""Scan the PUBLIC half for private data, with patterns taken from the private half.

THE ONE MISTAKE HERE THAT CANNOT BE UNDONE is a real name, employer, or figure
reaching the public repository. The scan that guards it was, until now, an
ad-hoc grep typed fresh each time -- which meant the pattern list depended on
what the author happened to remember, and a company added last week was simply
not in it.

SO THE PATTERNS ARE DERIVED, NOT TYPED. Employer names come from the company
brief filenames, person names from the contact records' own frontmatter, and
personal values from profile.yml. Add a company and it is covered on the next
run, with nobody editing a list.

AND THE SCAN PROVES IT CAN FIRE BEFORE REPORTING CLEAN. Every check that can
return "nothing found" can also return "nothing found" because it was broken,
and the two are indistinguishable in the output. On 2026-10-20 that happened
four times in one session: a shell that silently declined to split an unquoted
list, a glob that aborted a loop before it ran, a case-sensitive match on an
uppercased heading, and phrase searches spanning a line break. Each returned
zero and each zero was read as good news. **A clean result here is only printed
after a known-positive control has matched.**

Usage: leak_scan.py [--staged]      (--staged scans only files staged in git)
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PRIVATE = ROOT / "private"
PUBLIC_DIRS = [ROOT / "framework"]
PUBLIC_ROOT_GLOBS = ["*.md"]
SKIP = {"CHANGELOG.md"}          # records its own history; see note below

MONEY = re.compile(r"\$\s?\d[\d,]{2,}")
# A line carrying this marker is a deliberate placeholder or this scan's own
# control probe. It is spelled out rather than inferred, so that silencing a
# finding is always a visible edit to the line that was flagged.
ALLOW = "leak-scan: allow"
EXAMPLE_DOMAIN = re.compile(r"@example\.(com|org|net)\b", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
# US phone numbers, added 2026-10-28 when contact records gained a `phone:`
# field. Universal like MONEY and EMAIL rather than derived, for the same
# reason: a number can be typed into a framework file before any private
# data exists to derive it from. Deliberately NARROW -- it requires the
# punctuation a written phone number carries, so a bare ten-digit run (an
# id, a timestamp, a row count) does not match. A number written without
# any separator is the known blind spot and is accepted: widening it to
# catch that costs false positives on every long integer in the repo, and
# a scan nobody reads is the failure mode this file already documents.
PHONE = re.compile(r"(?:\(\d{3}\)\s*|\b\d{3}[.\-\s])\d{3}[.\-\s]\d{4}\b")


# A single word from a name is not a name. A hyphenated employer yields its
# first word and a two-word person yields a given name -- both commonly plain
# English -- and matching those produced 210 hits across the framework scripts
# on the first run, every one of them a false positive. (Those examples are
# written generically here ON PURPOSE: the first draft of this comment named a
# real employer and a real contact, and this scan caught them.) A scan
# that cries wolf 210 times is a scan nobody reads, which is the same failure
# as not having one. So: WHOLE names, as phrases, with flexible separators.
STOP = {"health", "software", "group", "technologies", "systems", "labs",
        "solutions", "services", "digital", "data", "cloud", "global",
        "interactive", "media", "partners", "capital", "works", "studio"}


def _phrase(words):
    """A regex matching those words in order, separated by space/dash/underscore."""
    return re.compile(r"\b" + r"[-_ ]+".join(re.escape(w) for w in words) + r"\b", re.I)


def derived_patterns():
    """(label -> compiled regex) built from the private half, never hand-typed."""
    pats = {}
    comp = PRIVATE / "data" / "companies"
    if comp.is_dir():
        for p in comp.glob("*.md"):
            words = [w for w in re.split(r"[-_]+", p.stem) if w.isalpha()]
            if not words:
                continue
            # the full name always; a single distinctive word only if it is
            # long, not a generic industry suffix, and not a plain dictionary
            # word someone might legitimately write in a framework file.
            pats[p.stem] = _phrase(words)
            if len(words) == 1 and len(words[0]) >= 6 and words[0].lower() not in STOP:
                pats[words[0].lower()] = _phrase(words)
    # PEOPLE ARE ALSO NAMED IN COMPANY BRIEFS, under their own `### ` heading,
    # and most of them have no contact record at all. Deriving names only from
    # data/contacts/ missed every one of them -- a planted surname from a brief
    # sailed through a "clean" run while this was being written.
    if comp.is_dir():
        for p in comp.glob("*.md"):
            in_people = False
            for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("## "):
                    # only `### ` headings INSIDE a contacts section are people.
                    # Without this gate, section headings like "Resume release"
                    # became patterns and matched ordinary framework prose.
                    in_people = bool(re.search(r"contact|reference|people|who",
                                               line, re.I))
                    continue
                if not in_people or not line.startswith("### "):
                    continue
                head = re.split(r"[—\-|(,]", line[4:])[0]
                words = [w.strip(".") for w in head.split() if w.strip(".").isalpha()]
                words = [w for w in words if w[:1].isupper()]
                if len(words) >= 2:
                    pats["brief:" + "-".join(words).lower()] = _phrase(words)
                    if len(words[-1]) >= 7:
                        pats["surname:" + words[-1].lower()] = _phrase([words[-1]])

    cont = PRIVATE / "data" / "contacts"
    if cont.is_dir():
        for p in cont.glob("*.md"):
            for line in p.read_text(encoding="utf-8", errors="replace").splitlines()[:15]:
                if not line.lower().startswith("name:"):
                    continue
                words = [w.strip(".,") for w in line.split(":", 1)[1].split()
                         if w.strip(".,").isalpha()]
                if len(words) >= 2:
                    pats["name:" + "-".join(words).lower()] = _phrase(words)
                    surname = words[-1]
                    if len(surname) >= 7:      # distinctive enough alone
                        pats["surname:" + surname.lower()] = _phrase([surname])
                break
    return pats


def has_private_data():
    """True when there is anything a name pattern could be derived FROM."""
    for sub in ("companies", "contacts"):
        d = PRIVATE / "data" / sub
        if d.is_dir() and any(d.glob("*.md")):
            return True
    return False


def self_test(pats):
    """Prove the matcher fires. A clean run is meaningless without this.

    THE EMPTY CASE IS NOT A FAILURE, and getting that wrong made this script
    exit non-zero on a fresh clone and on a freshly bootstrapped instance --
    the two states every new user passes through. **An instance with no private
    data has nothing that could leak**, so zero name patterns is the correct
    answer there, not a broken scan.

    What must never happen is the inverse: private data present and patterns
    empty, which means derivation broke and the scan would cheerfully report a
    clean public half it never actually examined. That is a hard failure.

    The money, email and phone patterns are universal and are controlled either
    way, because a hard-coded figure can be written into a framework file on day
    one, before any private data exists at all.
    """
    if not MONEY.search("a probe figure of $123,456 not real"):  # leak-scan: allow
        return "control FAILED: money pattern did not match a known-positive"
    if not EMAIL.search("a probe address nobody@probe-domain.invalid here"):  # leak-scan: allow
        return "control FAILED: email pattern did not match a known-positive"
    if not PHONE.search("a probe number of (555) 010-9999 not real"):  # leak-scan: allow
        return "control FAILED: phone pattern did not match a known-positive"
    if PHONE.search("a bare run of digits 5550109999 is not a phone"):  # leak-scan: allow
        return "control FAILED: phone pattern matched an unpunctuated digit run"
    if pats:
        probe_key = sorted(pats)[0].split(":")[-1].replace("-", " ")
        if not pats[sorted(pats)[0]].search(f"a line mentioning {probe_key} here"):
            return f"control FAILED: pattern {probe_key!r} did not match its own probe"
    elif has_private_data():
        return ("control FAILED: private data exists but NO name patterns were"
                " derived — derivation is broken, and a clean result here would"
                " be meaningless")
    return None


def files_to_scan(staged):
    if staged:
        out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                             cwd=ROOT, capture_output=True, text=True).stdout
        return [ROOT / f for f in out.split() if (ROOT / f).is_file()]
    fs = []
    for d in PUBLIC_DIRS:
        fs += [p for p in d.rglob("*") if p.is_file() and p.suffix in (".md", ".py", ".yml", ".csv")]
    for g in PUBLIC_ROOT_GLOBS:
        fs += list(ROOT.glob(g))
    return fs


def main():
    staged = "--staged" in sys.argv
    pats = derived_patterns()
    failure = self_test(pats)
    if failure:
        print(f"leak_scan: {failure}")
        return 2                      # never report clean on a broken scan

    hits = []
    for f in files_to_scan(staged):
        try:
            rel = f.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        if rel.startswith("private/") or Path(rel).name in SKIP:
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if ALLOW in line or EXAMPLE_DOMAIN.search(line):
                continue
            for m in (MONEY.search(line), EMAIL.search(line), PHONE.search(line)):
                if m:
                    hits.append((rel, i, m.group(0)[:40]))
            for key, rx in pats.items():
                m = rx.search(line)
                if m:
                    hits.append((rel, i, m.group(0)[:40]))
                    break

    scope = (f"{len(pats)} derived pattern(s)" if pats else
             "NO name patterns — this instance has no private data yet, so only"
             " the universal figure/address checks ran")
    print(f"leak_scan: {len(files_to_scan(staged))} public file(s), {scope}, "
          f"control PASSED.")
    for rel, i, what in hits[:40]:
        print(f"  !! {rel}:{i}  {what!r}")
    if hits:
        print(f"leak_scan: {len(hits)} POSSIBLE LEAK(S) — read each before committing.")
        return 1
    print("leak_scan: no private data found in the public half.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
