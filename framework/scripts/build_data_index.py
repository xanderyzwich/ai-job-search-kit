#!/usr/bin/env python3
"""Render the data layer's README — the layout, lifted from CONTRACT.

WHY THIS IS GENERATED AND NOT WRITTEN. The first version of this README was
hand-written, and it was a second description of what CONTRACT already defines:
what each directory under data/ holds and what must exist. Two descriptions of
one fact is the mirror this kit keeps paying to remove -- so the descriptions
are EXTRACTED from CONTRACT's own rows rather than re-encoded, the same way the
context map lifts the ripple section verbatim instead of restating it. CONTRACT
stays the single place a directory's purpose is defined.

IT ALSO CHECKS CONFORMANCE, which is the part a hand-written file could never
do. Every entry on disk is matched against a CONTRACT row: anything present but
undocumented is reported, and anything documented but absent is reported. A
README that quietly omits an undocumented directory is worse than no README,
because it reads as a complete map.

NO FILE LIST. Directories are named; their contents are not. `ls` answers what
is in a directory, and a list here would rot the first busy week.

Usage: build_data_index.py [--data PATH] [--contract PATH]
"""
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_DATA = ROOT / "private" / "data"
DEFAULT_CONTRACT = ROOT / "framework" / "CONTRACT.md"
ROW = re.compile(r"^\|\s*`private/data/([^`]+)`\s*\|\s*(.+?)\s*\|\s*$", re.M)


def first_sentence(s, limit=220):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    m = re.search(r"(.+?[.!?])(\s|$)", s)
    out = (m.group(1) if m else s).strip()
    return (out[: limit - 1] + "…") if len(out) > limit else out


def contract_rows(contract):
    """{spec: description} for every documented path under data/."""
    return {m.group(1).strip(): first_sentence(m.group(2))
            for m in ROW.finditer(contract.read_text(encoding="utf-8"))}


def match(name, is_dir, specs):
    """The CONTRACT spec covering this entry, or None."""
    for spec in specs:
        # A directory is described only by a row for the DIRECTORY -- `name/` or
        # the one-per-thing convention `name/*.md`. A row for a specific file
        # inside it (`dashboard/calendar.md`) describes that file, and letting it
        # stand in for the directory silently attributes one child's purpose to
        # the whole, which is exactly the kind of plausible-looking wrong answer
        # a generated index must not produce.
        if is_dir and (spec == name + "/" or spec.startswith(name + "/*")):
            return spec
        if not is_dir and "/" not in spec:
            if spec == name:
                return spec
            if "*" in spec and re.fullmatch(spec.replace("*", ".*"), name):
                return spec
    return None


def main():
    d = Path(sys.argv[sys.argv.index("--data") + 1]) if "--data" in sys.argv else DEFAULT_DATA
    c = Path(sys.argv[sys.argv.index("--contract") + 1]) if "--contract" in sys.argv else DEFAULT_CONTRACT
    if not d.is_dir() or not c.exists():
        print("build_data_index: no data directory or no CONTRACT — skipped.")
        return 0
    specs = contract_rows(c)

    dirs = sorted(p for p in d.iterdir() if p.is_dir() and not p.name.startswith("."))
    files = sorted(p for p in d.iterdir()
                   if p.is_file() and p.name not in ("README.md",)
                   and not p.name.startswith("."))

    L = ["# Data", "",
         "> **GENERATED FILE — do not hand-edit.** Built by"
         " `framework/scripts/build_data_index.py` on %s. **Every description"
         " below is lifted from `framework/CONTRACT.md`**, which stays the one"
         " place a directory's purpose is defined — fix it there."
         % date.today().isoformat(),
         ">",
         "> **This is the LAYOUT, not the contents.** Directories are named;"
         " what is inside them is not. `ls` answers that, and a file list here"
         " would rot the first busy week.", "",
         "## Directories", "", "| directory | what goes in it |", "|---|---|"]

    undocumented = []
    for p in dirs:
        spec = match(p.name, True, specs)
        if spec:
            L.append("| **`%s/`** | %s |" % (p.name, specs[spec]))
        else:
            undocumented.append(p.name + "/")
            L.append("| **`%s/`** | **NOT IN CONTRACT** — document it or remove it. |" % p.name)

    L += ["", "## Files kept in the root", "",
          "Live state, read most sessions. Anything that ACCUMULATES belongs in a"
          " directory instead.", "", "| file | what it is |", "|---|---|"]
    for p in files:
        spec = match(p.name, False, specs)
        if spec:
            L.append("| `%s` | %s |" % (p.name, specs[spec]))
        else:
            undocumented.append(p.name)
            L.append("| `%s` | **NOT IN CONTRACT** — document it or move it. |" % p.name)

    present = {p.name for p in dirs} | {p.name for p in files} | {"README.md"}

    # WHAT A FRESH INSTANCE IS SUPPOSED TO HAVE IS DEFINED BY bootstrap.py, so
    # ask it rather than guessing. Most of what CONTRACT documents is created
    # ON DEMAND -- an outreach queue when there is outreach, a story bank when
    # there are stories -- and reporting those as missing told a new user that
    # five things were broken about an installation that was perfectly correct.
    # Importing the lists keeps one source of truth: change bootstrap and this
    # follows.
    expected = set()
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import bootstrap
        for bd in getattr(bootstrap, "DIRS", []):
            expected.add(bd.split("/")[-1] + "/")
        for k in getattr(bootstrap, "SEEDS", {}):
            expected.add(k.split("/")[-1])
        for _src, dst in getattr(bootstrap, "COPIES", []):
            expected.add(dst.split("/")[-1])
    except Exception:
        expected = None      # cannot tell -- report nothing rather than noise

    def want(spec):
        if expected is None:
            return False
        base = spec.rstrip("/").split("/")[-1]
        return (base + "/") in expected or base in expected

    missing = [s for s in specs
               if "/" not in s and "*" not in s and s not in present and want(s)]
    missing += [s for s in specs
                if s.endswith("/") and s.rstrip("/") not in present and want(s)]

    if undocumented or missing:
        L += ["", "## Conformance", ""]
        if undocumented:
            L.append("- **On disk, not in CONTRACT:** %s" % ", ".join(
                "`%s`" % u for u in undocumented))
        if missing:
            L.append("- **In CONTRACT, not on disk:** %s" % ", ".join(
                "`%s`" % m for m in sorted(set(missing))))
        L.append("")
    L += ["", "**The test for a new file: does it accumulate?** Output produced by"
          " a process, and studies written once and referenced later, both grow"
          " without bound and belong in a directory. Only live state read most"
          " sessions belongs in the root.", ""]

    (d / "README.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote %s: %d dir(s), %d root file(s), %d undocumented, %d missing."
          % (d.name + "/README.md", len(dirs), len(files),
             len(undocumented), len(set(missing))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
