#!/usr/bin/env python3
"""Check that public changes carry a CHANGELOG entry, and say which were late.

The changelog is the public record of WHY this framework looks the way it does,
tied to the failure that forced each change. A commit message is not a
substitute: nobody reads a git log to learn a system's reasoning. The rule is
that any change to `framework/` or a root doc owes an entry in the same commit.

That rule was enforced by intention until 2026-10-06, when an audit found NINE
of fourteen framework-touching commits carried none. The misses were not random
— entries got written for changes that felt architecturally large and skipped
for fixes and follow-ups, which are the ones carrying the most transferable
content. A reorganisation is visible in the tree; a silent failure mode is not.

TWO WAYS TO BE COVERED, AND THEY ARE NOT EQUAL:

  same-commit   the commit touched CHANGELOG.md itself. The good case.
  backfilled    a later entry cites the hash in an HTML comment:
                    <!-- covers: abc1234 def5678 · backfilled YYYY-MM-DD -->
                Invisible in rendered Markdown, greppable here.

Backfilling is deliberately NOT silent. An entry reconstructed from a diff
carries what changed; an entry written at the decision carries why the
alternative was rejected, and that half does not survive the week. So the two
are counted separately and the ratio is printed — a rising backfill count means
the discipline is slipping even while every commit technically passes.

**A cited hash is verified to resolve.** Two ways to be covered is also a second
way to be wrong: a typo'd hash would otherwise read as covered forever.

Usage: check_changelog.py [N]      (default: last 20 commits)
Exit 1 if any public commit is uncovered.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"
# A change to any of these owes an entry.
PUBLIC = re.compile(r"^(framework/|README\.md|SESSION_INIT\.md|QUICKSTART\.md"
                    r"|ARCHITECTURE\.md|CLAUDE\.md|AGENTS\.md)")
COVERS = re.compile(r"<!--\s*covers:\s*([0-9a-f\s]+?)\s*(?:·|-->)")


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True).stdout


def cited_hashes():
    """Hashes claimed by a backfilled entry, verified to exist."""
    if not CHANGELOG.exists():
        return set(), []
    good, bogus = set(), []
    for m in COVERS.finditer(CHANGELOG.read_text(encoding="utf-8")):
        for h in m.group(1).split():
            full = git("rev-parse", "--verify", "--quiet", h + "^{commit}").strip()
            (good.add(full[:7]) if full else bogus.append(h))
    return good, bogus


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    cited, bogus = cited_hashes()
    same, late, missing = 0, 0, []

    for line in git("log", f"-{n}", "--format=%h%x00%s").splitlines():
        if not line.strip():
            continue
        sha, subject = line.split("\x00", 1)
        files = git("show", "--stat=200", "--format=", sha).splitlines()
        names = [f.split("|")[0].strip() for f in files if "|" in f]
        if not any(PUBLIC.match(f) for f in names):
            continue                       # private-only commit, owes nothing
        if any(f == "CHANGELOG.md" for f in names):
            same += 1
        elif sha in cited:
            late += 1
        else:
            missing.append((sha, subject))

    for h in bogus:
        print(f"  ERROR  CHANGELOG cites `{h}`, which is not a commit in this repo")
    for sha, subject in missing:
        print(f"  MISSING  {sha}  {subject[:64]}")

    total = same + late
    print(f"check_changelog: {total} public commit(s) covered "
          f"({same} at the time, {late} backfilled), {len(missing)} uncovered"
          + (f", {len(bogus)} bad citation(s)" if bogus else ""))
    if late and not missing:
        print("  note: backfilled entries are weaker than entries written at the"
              " decision — a rising count here means the rule is slipping.")
    return 1 if (missing or bogus) else 0


if __name__ == "__main__":
    sys.exit(main())
