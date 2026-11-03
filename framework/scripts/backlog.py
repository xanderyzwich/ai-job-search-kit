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
check is "is this worth re-verifying", not "is this dead". Note the age is
measured from when the role was FOUND, not when it was posted; a listing
can already be months old on the day it is swept.

THE BAR HAS TO BEND FOR POSTINGS WITH NO PREFERRED LIST. tech_fit is
`hard_match_pct + 0.5 * nice_match_pct`, so a JD that names no
preferred/nice-to-have section CANNOT SCORE ABOVE 100 -- a flawless match
lands exactly on the threshold and a single missed requirement drops it
under. Screening on a flat 100 therefore excludes the cleanest matches in
the tracker for a reason that has nothing to do with fit. Rows recorded with
`nice_reqs=0` are admitted down to `--min minus --margin` and flagged
NO-PREF. `--margin` covers the other one-off shapes too; widen it rather
than inventing a second threshold.
"""
import argparse
import csv
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRIV = ROOT if (ROOT / "job_tracker.csv").exists() else ROOT.parent / "private"
TRACKER = PRIV / "job_tracker.csv"

# The single definition of the bar. daily_log.py imports it rather than
# repeating the number, because a threshold written in two places drifts in
# one of them and nothing announces it.
DEFAULT_MIN = 100.0
DEFAULT_MARGIN = 15.0

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


def req_count(cell):
    """How many requirements a cell describes, and whether it LISTS them.

    The column holds a pipe-delimited list of requirements ("+Java | -Go").
    Rows scored before that change hold a bare integer count instead; the
    contract says to distinguish the two and never read an integer as a
    one-item list. Returns (count, is_listed).
    """
    cell = (cell or "").strip()
    if not cell:
        return None, False
    if "|" in cell or cell[:1] in "+-":
        return len([x for x in cell.split("|") if x.strip()]), True
    n = num(cell)
    return (int(n), False) if n is not None else (None, False)


def row_score(r):
    """Rank a row by min() of the scoring dimensions it actually has.

    Per the contract: the bar is per dimension and there is no composite, so a
    row short on one half must not average its way up. A dimension the posting
    does not ask about is N/A, not zero -- which is why this takes the minimum
    over the dimensions PRESENT rather than over both. For a row with only
    tech_fit that is tech_fit, so rows scored before the second dimension
    existed rank exactly as they always did.
    """
    dims = {}
    for key, short in (("tech_fit", "T"), ("mgmt_fit", "M")):
        v = num(r.get(key))
        if v is not None:
            dims[short] = v
    if not dims:
        return None, {}
    return min(dims.values()), dims


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--min", type=float, default=DEFAULT_MIN,
                   help=f"tech_fit floor (default {DEFAULT_MIN:.0f})")
    p.add_argument("--margin", type=float, default=DEFAULT_MARGIN,
                   help="how far below the floor a no-preferred-list posting"
                        f" still counts (default {DEFAULT_MARGIN:.0f})")
    p.add_argument("--all", action="store_true", help="include rows below the floor")
    p.add_argument("--unscored", action="store_true",
                   help="also list researching rows that were never scored")
    p.add_argument("--reqs", action="store_true",
                   help="print each row's requirement lists under it")
    p.add_argument("--stale-days", type=int, default=21,
                   help="flag rows older than this (default 21)")
    a = p.parse_args()

    rows = list(csv.DictReader(TRACKER.open()))
    research = [r for r in rows if r.get("application_status", "").strip() == "researching"]

    hits, needs_rescore, unscored = [], [], []
    for r in research:
        score, dims = row_score(r)
        if score is None:
            (needs_rescore if SCORE_IN_NOTES.search(r.get("notes", "")) else unscored).append(r)
        else:
            no_pref = (r.get("nice_reqs", "").strip() == "0")
            floor = a.min - a.margin if no_pref else a.min
            if a.all or score >= floor:
                hits.append((score, r, no_pref, dims))

    hits.sort(key=lambda x: (row_date(x[1]), x[0]), reverse=True)
    today = date.today()

    print(f"SCORED >= {a.min:.0f}, STATUS researching, NEVER APPLIED: {len(hits)}")
    print(f"{'score':>6}  {'reqs':>12}  {'found':10}  {'age':>4}  company / role")
    print("-" * 100)
    for score, r, no_pref, dims in hits:
        n_hard, listed = req_count(r.get("hard_reqs"))
        n_mgmt, _ = req_count(r.get("mgmt_reqs"))
        parts = [f"{n_hard}t" if n_hard is not None else "?t"]
        if n_mgmt:
            parts.append(f"{n_mgmt}m")
        reqs = "/".join(parts) + ("" if listed else "*")
        flags = []
        if len(dims) > 1:
            flags.append("+".join(f"{k}{v:.0f}" for k, v in dims.items()))
        if no_pref:
            flags.append("NO-PREF")       # ceiling is 100; read the score as hard-match %
        if n_hard is not None and n_hard <= 2:
            flags.append("THIN")          # too few requirements for the score to mean much
        d = row_date(r)
        age = ""
        if d:
            try:
                age = (today - datetime.strptime(d, "%Y-%m-%d").date()).days
                if age > a.stale_days:
                    flags.append("STALE")
            except ValueError:
                pass
        print(f"{score:6.1f}  {reqs:>12}  {d or '?':10}  {str(age):>4}  "
              f"{r['company'][:34]} - {r['role'][:40]}"
              + (f"   [{' '.join(flags)}]" if flags else ""))
        if a.reqs:
            for key, label in (("hard_reqs", "tech"), ("mgmt_reqs", "mgmt")):
                cell = (r.get(key) or "").strip()
                if cell and ("|" in cell or cell[:1] in "+-"):
                    print(f"{'':>8}{label}: " + "  ".join(x.strip() for x in cell.split("|")))

    if needs_rescore:
        print(f"\nSCORE RECORDED IN NOTES BUT NOT TRUSTED: {len(needs_rescore)}")
        print("  (conflicting values, or the note itself disowns the score)")
        for r in needs_rescore[:20]:
            print(f"    {r['company'][:36]} - {r['role'][:44]}")

    # Never-scored rows split in two, because they are not one problem.
    # A row with a live URL can still be scored retroactively; a row without
    # one cannot be recovered without re-finding the posting. And many were
    # never scored because the search process is supposed to gate on
    # geography and pay BEFORE scoring -- so a missing score is often a
    # decision, not an omission. Only the scoreable half is a backlog.
    scoreable = [r for r in unscored if r.get("job_url", "").strip()]
    no_url = [r for r in unscored if not r.get("job_url", "").strip()]
    if a.unscored:
        print(f"\nNEVER SCORED, HAS A URL -- scoreable retroactively if still"
              f" live: {len(scoreable)}")
        for r in sorted(scoreable, key=row_date, reverse=True)[:60]:
            print(f"    {row_date(r) or '?':10}  {r['company'][:32]} - {r['role'][:38]}")
        print(f"\nNEVER SCORED, NO URL -- needs re-finding first: {len(no_url)}")
        for r in no_url[:20]:
            print(f"    {row_date(r) or '?':10}  {r['company'][:32]} - {r['role'][:38]}")
    else:
        print(f"\n{len(unscored)} researching rows were never scored "
              f"({len(scoreable)} still have a URL and could be scored"
              f" retroactively -- `--unscored` to list them).")


if __name__ == "__main__":
    main()
