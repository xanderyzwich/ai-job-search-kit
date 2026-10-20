#!/usr/bin/env python3
"""Render the dashboard index — the menu of human-readable generated views.

WHY A DIRECTORY AND AN INDEX. The instance's data layer accumulates one-off
analyses -- a dozen dated stack-rank files, lane explorations, superseded
proposals -- and the handful of CURRENT rendered views were filed among them in
alphabetical order. On a laptop that is untidy. On a phone, through a web view
of the repository, it makes the views effectively unfindable, and the whole
reason those views are committed rather than left in the ignored temp directory
is that the search gets read in the evening with the machine off.

A web view renders README.md when you open a directory, so this file turns
arrival at the folder into a menu rather than a file listing.

IT IS BUILT BY SCANNING THE DIRECTORY, never from a list. A hand-kept index of
generated files is a mirror of a filesystem, and this kit has paid for that
mistake in several forms already: a skills list that went stale the day two
skills were added, a script list removed for the same reason. Add a view to the
folder and it appears here; delete one and it leaves.

Usage: build_dashboard.py [--dir PATH]
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DIR = ROOT / "private" / "data" / "dashboard"
READ_BY = re.compile(r"\*\*READ BY: ([^.*]+)", re.I)
STAMP = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")


def describe(p):
    """Title, audience and render stamp, taken from the file's own header."""
    text = p.read_text(encoding="utf-8", errors="replace")
    title = p.stem.replace("_", " ").title()
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    head = "\n".join(text.splitlines()[:12])
    m = READ_BY.search(head)
    who = m.group(1).strip().rstrip(",") if m else None
    s = STAMP.search(head)
    return title, who, (s.group(1) if s else None)


def main():
    d = Path(sys.argv[sys.argv.index("--dir") + 1]) if "--dir" in sys.argv else DEFAULT_DIR
    d.mkdir(parents=True, exist_ok=True)
    views = sorted(p for p in d.glob("*.md") if p.name != "README.md")

    L = ["# Dashboard", "",
         "> **GENERATED FILE — do not hand-edit.** Built by"
         " `framework/scripts/build_dashboard.py` on %s by SCANNING this"
         " directory, so a view added here appears without anyone editing a"
         " list." % date.today().isoformat(),
         ">",
         "> **READ BY: the candidate.** Every file here is a rendered view of"
         " records kept elsewhere — committed so the search reads from a phone"
         " with the machine off. **Fix the record and regenerate; never edit a"
         " view.** The assistant's own working references are not here: they"
         " are rebuilt each session into the ignored `temp/` directory.", ""]

    if not views:
        L += ["*No views rendered yet.*", ""]
    for p in views:
        title, who, stamp = describe(p)
        bits = [b for b in [("rendered " + stamp) if stamp else None,
                            ("read by " + who) if who else None] if b]
        L.append("- **[%s](%s)**%s" % (
            title, p.name, (" — " + "; ".join(bits)) if bits else ""))
    L.append("")

    (d / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    out = d / "README.md"
    try:
        shown = out.relative_to(ROOT)
    except ValueError:      # --dir outside the repo, e.g. a test fixture
        shown = out
    print("Wrote %s: %d view(s)." % (shown, len(views)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
