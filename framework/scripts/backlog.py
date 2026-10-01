#!/usr/bin/env python3
"""The scored-but-never-applied check.

THE PROBLEM THIS EXISTS FOR: a stack rank gets worked top-down and the day
ends. The roles below the waterline are not rejections -- nobody decided
against them -- they just ran out of daylight. They stay `researching`
forever, and the only way they have ever surfaced is someone deciding to
comb back through the tracker by hand. Rows do not raise their own hands.

    backlog.py [--min 100] [--all] [--unscored] [--stale-days N]

Lists `researching` rows whose tech_fit clears the bar, newest first,
with the two things that decide whether the number can be trusted.

READ THE REQUIREMENT COUNT, NOT JUST THE SCORE. match_gap_scoring.md
promoted `N hard (M tech-named)` to a required field on 2026-09-15 because
a 22-JD pass found that EVERY batch put a vagueness artifact in its top two
and the requirement count predicted it every time -- an entry-level req
scored 150 while the most trustworthy row in the pass scored 77. A score
computed against few, non-technology-named requirements is inflated. This
script prints the count and marks a row VAGUE? when a JD names several hard
requirements and almost none of them name a technology.

AGE IS A LIVENESS QUESTION. A role scored seven weeks ago is probably no
longer posted. Old rows are listed last and flagged, not hidden -- the
check is "is this worth re-verifying", not "is this dead".
"""
import argparse
import csv
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT if (ROOT / "job_tracker.csv").exists() else ROOT.parent / "private"
TRACKER = PRIV / "job_tracker.csv"

DISOWN = re.compile(r"\bWAS WRONG\b|NEEDS RESCORE|\bRESCORE\b|OVERSTATED"
                    r"|INFLATED|artifact-inflated", re.I)
SCORE_IN_NOTES = re.compile(r"tech_fit\s*[=:]?\s*\d")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def row_date(r):
    """Best available date for the row: the sweep that found it."""
    m = re.search(r"(\d{4}-\d{2}-\d{2})", r.get("sweep_id", "") or "")
    if m:
        return m.group(1)
    m = re.search(r"(\d{4}-\d{2}-\d{2})", r.get("found_via", "") or "")
    return m.group(1) if m else ""


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--min", type=float, default=100.0,
                   help="tech_fit floor (default 100)")
    p.add_argument("--all", action="store_true", help="include rows below the floor")
    p.add_argument("--unscored", action="store_true",
                   help="also list researching rows that were never scored")
    p.add_argument("--stale-days", type=int, default=21,
                   help="flag rows older than this (default 21)")
    a = p.parse_args()

    rows = list(csv.DictReader(TRACKER.open()))
    research = [r for r in rows if r.get("application_status", "").strip() == "researching"]

    hits, needs_rescore, unscored = [], [], []
    for r in research:
        tf = num(r.get("tech_fit"))
        if tf is None:
            (needs_rescore if SCORE_IN_NOTES.search(r.get("notes", "")) else unscored).append(r)
        elif a.all or tf >= a.min:
            hits.append((tf, r))

    hits.sort(key=lambda x: (row_date(x[1]), x[0]), reverse=True)
    today = date.today()

    print(f"SCORED >= {a.min:.0f}, STATUS researching, NEVER APPLIED: {len(hits)}")
    print(f"{'score':>6}  {'reqs':>12}  {'found':10}  {'age':>4}  company / role")
    print("-" * 100)
    for tf, r in hits:
        hr, tn = num(r.get("hard_reqs")), num(r.get("tech_named_reqs"))
        reqs = f"{int(hr)} hard/{int(tn)} tech" if hr is not None and tn is not None else "--"
        flags = []
        if hr is not None and tn is not None and hr >= 4 and tn <= 1:
            flags.append("VAGUE?")
        d = row_date(r)
        age = ""
        if d:
            try:
                age = (today - datetime.strptime(d, "%Y-%m-%d").date()).days
                if age > a.stale_days:
                    flags.append("STALE")
            except ValueError:
                pass
        print(f"{tf:6.1f}  {reqs:>12}  {d or '?':10}  {str(age):>4}  "
              f"{r['company'][:34]} - {r['role'][:40]}"
              + (f"   [{' '.join(flags)}]" if flags else ""))

    if needs_rescore:
        print(f"\nSCORE RECORDED IN NOTES BUT NOT TRUSTED: {len(needs_rescore)}")
        print("  (conflicting values, or the note itself disowns the score)")
        for r in needs_rescore[:20]:
            print(f"    {r['company'][:36]} - {r['role'][:44]}")

    if a.unscored:
        print(f"\nRESEARCHING, NEVER SCORED: {len(unscored)}")
        for r in unscored[:40]:
            print(f"    {row_date(r) or '?':10}  {r['company'][:34]} - {r['role'][:40]}")
    else:
        print(f"\n{len(unscored)} researching rows were never scored "
              f"(--unscored to list them).")


if __name__ == "__main__":
    main()
