#!/usr/bin/env python3
"""Build the session context map — a generated "when to do what" cheat-sheet.

Materializes two things the assistant needs in context from the first moment
of a session, so a mid-session pivot into a framework edit already has the
obligations in front of it instead of relying on a remembered header scan:

  1. Skill routing — every skill's `**Load when:**` header, so choosing what
     to load is a glance, not a grep.
  2. The ripple map — "when X changes, also touch Y", lifted from
     framework-maintenance.md.

WHY GENERATED, NOT VERSIONED:
A checked-in index of skills/ripples would be one more mirror to keep in sync
— the exact drift this framework fights. So this file is rebuilt every
session from the canonical sources and written to private/temp/context_map.md
(gitignored). It is a VIEW, never a source: it never re-encodes the map, it
extracts it. Skill headers stay the source of truth for routing; the ripple
section of framework-maintenance.md stays the source of truth for ripples.
Never hand-edit the output — fix the source and rerun.

Invoked automatically by daily_log.py open; safe to run standalone anytime.
Paths resolve from this script's own location.
"""
import re
import sys
from datetime import datetime
from pathlib import Path

FRAMEWORK = Path(__file__).resolve().parent.parent
ROOT = FRAMEWORK.parent
PRIVATE = ROOT / "private"
MAINT = FRAMEWORK / "skills" / "framework-maintenance.md"
OUT = PRIVATE / "temp" / "context_map.md"
RIPPLE_HEADING = "## The ripple map"


def scan_load_when(*skill_dirs):
    """[(relpath, load_when_text)] for every skill file, from its first 8 lines."""
    entries = []
    for d in skill_dirs:
        if not d.is_dir():
            continue
        for path in sorted(d.rglob("*.md")):
            head = "\n".join(path.read_text(encoding="utf-8").splitlines()[:8])
            m = re.search(r"\*\*Load when:\*\*\s*(.+?)(?:\n\n|\Z)", head, re.S)
            lw = " ".join(m.group(1).split()) if m else "(!! no Load-when header)"
            entries.append((path.relative_to(ROOT).as_posix(), lw))
    return entries


def extract_ripple_section():
    """Lift the ripple-map section verbatim — extract, never re-encode."""
    if not MAINT.exists():
        return "(framework-maintenance.md not found)"
    text = MAINT.read_text(encoding="utf-8")
    start = text.find(RIPPLE_HEADING)
    if start == -1:
        return (f"(!! {RIPPLE_HEADING!r} not found in framework-maintenance.md "
                "— heading renamed? fix the extractor or the heading)")
    nxt = text.find("\n## ", start + len(RIPPLE_HEADING))
    return text[start:nxt if nxt != -1 else len(text)].strip()


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    skills = scan_load_when(FRAMEWORK / "skills", PRIVATE / "skills")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    out = [
        f"# Session Context Map (generated {now})",
        "",
        "> GENERATED at session start by framework/scripts/build_context_map.py.",
        "> Do NOT edit — rebuilt every session from the skill headers and the",
        "> framework-maintenance ripple map. A view, never a source.",
        "> **Before editing any framework/ or root-doc file, read the ripple",
        "> section below and touch every mirror it names in the same batch.**",
        "",
        "## Skill routing (load on demand, by task)",
        "",
    ]
    out += [f"- **{rel}** — {lw}" for rel, lw in skills]
    out += ["", extract_ripple_section(), ""]
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(skills)} skills + ripple map.")
    missing = [r for r, lw in skills if lw.startswith("(!!")]
    if missing:
        print("  WARNING: skills missing a Load-when header: " + ", ".join(missing))


if __name__ == "__main__":
    main()
