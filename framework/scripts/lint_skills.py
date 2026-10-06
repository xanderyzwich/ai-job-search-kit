#!/usr/bin/env python3
"""Check every skill file against the header contract, and warn on size.

The header contract is what makes `grep -rA2 '^\\*\\*Load when'` list every
skill's routing in one call, and what makes the generated context map complete.
It has been enforced by eye until now, which is the same arrangement that let a
2,207-line file accumulate and let a delegation rule go unfollowed for two
months because nobody could find it.

Checks, in order of how much damage they prevent:

  ERROR   no title line, or no `**Load when:**` block
  ERROR   the Load-when does not start within the first 8 lines
  WARN    the Load-when itself runs longer than 3 lines
  WARN    the file is longer than SIZE_WARN lines

ERROR is reserved for what actually BREAKS the mechanism: a Load-when below the
budget is invisible to the head-scan, and a missing one cannot be routed at all.
Everything else warns. The first version of this script errored on a literal
`# Skill:` prefix and on any Load-when over three lines, and would have forced
churn across fifteen files for two things that were not problems — the private
instance titles its skills `# <Name>` by house style, and a Load-when's fourth
line is usually a disambiguation clause ("distinct from X"), which is routing
information worth having rather than a second concern.

The 8-line budget is not aesthetic: a scan reads the head of each file, so a
header below the budget is invisible to it. The 3-line cap is a smell test — a
Load-when that outgrows it is usually a skill covering two concerns, and the
fix is to split it rather than to pad the budget.

The size warning is advisory on purpose. A big reference file is sometimes the
right answer; a big file nobody can load selectively is not, and under the
sub-agent flow every extra line is paid again by every agent that reads it.

Exit 1 on any ERROR, 0 otherwise. Run it from the repo root; `daily_log.py
close` runs it so the check happens at a ritual rather than on request.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKILL_DIRS = [ROOT / "framework" / "skills", ROOT / "private" / "skills"]

HEADER_BUDGET = 8      # Load-when must START within this many lines
LOADWHEN_MAX = 3       # ...and SHOULD run no longer than this (warning)
SIZE_WARN = 450        # advisory only


def check(path: Path):
    """-> (errors, warnings) for one skill file."""
    errors, warns = [], []
    lines = path.read_text(encoding="utf-8").splitlines()

    if not any(l.startswith("# ") for l in lines[:4]):
        errors.append("no title line in the first 4 lines")

    start = next((i for i, l in enumerate(lines) if l.startswith("**Load when:**")), None)
    if start is None:
        errors.append("no `**Load when:**` block")
    else:
        if start + 1 > HEADER_BUDGET:
            errors.append(f"Load-when starts at line {start + 1}, budget is {HEADER_BUDGET}"
                          " — a scan reads only the head, so this one is invisible to it")
        # the block runs until the first blank line
        end = next((i for i in range(start + 1, len(lines)) if not lines[i].strip()), len(lines))
        span = end - start
        if span > LOADWHEN_MAX:
            warns.append(f"Load-when runs {span} lines, over the {LOADWHEN_MAX}-line"
                         " guide — check it is one concern and not two")

    if len(lines) > SIZE_WARN:
        warns.append(f"{len(lines)} lines (>{SIZE_WARN}) — every agent that loads this"
                     " pays for all of it; consider splitting by surface or concern")
    return errors, warns


def main():
    n = fails = 0
    out = []
    for d in SKILL_DIRS:
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*.md")):
            n += 1
            errors, warns = check(path)
            rel = path.relative_to(ROOT).as_posix()
            for e in errors:
                out.append(f"  ERROR  {rel}: {e}")
                fails += 1
            for w in warns:
                out.append(f"  warn   {rel}: {w}")
    if out:
        print("\n".join(out))
    print(f"lint_skills: {n} skills checked, {fails} error(s)"
          + ("" if fails else " — OK"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
