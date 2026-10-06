#!/usr/bin/env python3
"""Check that public changes carry a CHANGELOG entry, and say which were late.

The changelog is the public record of WHY this framework looks the way it does,
tied to the failure that forced each change. Its reader is someone who was not
there, does not have the repo checked out, and is reading this file on its own
— for a portfolio-visible repo it is often the only part read in depth. A
commit message is not a substitute (nobody reads a git log to learn a system's
reasoning) and neither is a diff, which that reader does not have. The rule is
that any change to `framework/` or a root doc owes an entry in the same commit.

That rule was enforced by intention until 2026-10-06, when an audit found NINE
of fourteen framework-touching commits carried none. The misses were not random
— entries got written for changes that felt architecturally large and skipped
for fixes and follow-ups, which are the ones carrying the most transferable
content. A reorganisation is visible in the tree; a silent failure mode is not.

TRIVIAL CHANGES ARE EXEMPT, BUT THE EXEMPTION MUST BE CLAIMED. A rename, a
typo, a path fix, a reflow — put `[no-changelog: <reason>]` in the commit
message. Claimed exemptions are counted and printed rather than hidden, so
"trivial" cannot quietly become the default excuse. If the MECHANISM changed it
is not trivial, however small the diff.

TWO WAYS TO BE COVERED, AND THEY ARE NOT EQUAL:

  same-commit   the commit touched CHANGELOG.md itself. The good case.
  backfilled    a later entry cites the hash in an HTML comment:
                    <!-- covers: abc1234 def5678 · backfilled YYYY-MM-DD -->
                Invisible in rendered Markdown, greppable here.

Backfilling is deliberately NOT silent, but what the ratio measures took two
wrong guesses to pin down. It is not that reconstruction always loses the
reasoning, and not that another author's commit is the problem. Measured: the
entries that survived backfilling came from commit bodies of 200-425 words; the
one that came out thin came from a body of 41. **An entry inherits its commit
body's richness.**

So the real lever is the commit message, not the timing of the entry. And when
a body is thin, the recovery is the session log rather than the diff — the one
thin entry was missing the measurement that gave its change the whole point,
and that measurement was in the day's log all along.

**A cited hash is verified to resolve.** Two ways to be covered is also a second
way to be wrong: a typo'd hash would otherwise read as covered forever.

THE RULE HAS A START DATE, AND CHASING HISTORY IS THE WRONG INSTINCT. Commits
before RULE_START are reported as predating it and do not fail the check. The
gaps behind that line run back weeks, and filling them would mean reconstructing
dozens of entries from diffs alone — which produces text that LOOKS like a
record while carrying none of the reasoning that makes one worth keeping. A
thin entry is worse than an honest absence, because it stops anyone looking
further.

Usage: check_changelog.py [N]      (default: last 20 commits)
Exit 1 if any public commit on or after RULE_START is uncovered.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"
# The day the rule was written down and the audit that forced it was run.
# Earlier commits predate it; see the docstring on why they are not chased.
RULE_START = "2026-10-01"
# A change to any of these owes an entry.
PUBLIC = re.compile(r"^(framework/|README\.md|SESSION_INIT\.md|QUICKSTART\.md"
                    r"|ARCHITECTURE\.md|CLAUDE\.md|AGENTS\.md)")
COVERS = re.compile(r"<!--\s*covers:\s*([0-9a-f\s]+?)\s*(?:·|-->)")
# The exemption has to be spelled out, with a reason, in the commit message.
EXEMPT = re.compile(r"\[no-changelog:\s*([^\]]+)\]", re.I)


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
    same, late, predates, missing, exempt = 0, 0, 0, [], []

    for line in git("log", f"-{n}", "--format=%h%x00%s").splitlines():
        if not line.strip():
            continue
        sha, subject = line.split("\x00", 1)
        full_msg = git("log", "-1", "--format=%B", sha)
        when = git("log", "-1", "--format=%ad", "--date=short", sha).strip()
        files = git("show", "--stat=200", "--format=", sha).splitlines()
        names = [f.split("|")[0].strip() for f in files if "|" in f]
        if not any(PUBLIC.match(f) for f in names):
            continue                       # private-only commit, owes nothing
        claim = EXEMPT.search(full_msg)
        if claim:
            exempt.append((sha, claim.group(1).strip()))
        elif any(f == "CHANGELOG.md" for f in names):
            same += 1
        elif sha in cited:
            late += 1
        elif when < RULE_START:
            predates += 1
        else:
            missing.append((sha, subject))

    for h in bogus:
        print(f"  ERROR  CHANGELOG cites `{h}`, which is not a commit in this repo")
    for sha, subject in missing:
        print(f"  MISSING  {sha}  {subject[:64]}")

    for sha, why in exempt:
        print(f"  exempt   {sha}  claimed trivial: {why}")
    total = same + late
    print(f"check_changelog: {total} public commit(s) covered "
          f"({same} at the time, {late} backfilled), {len(missing)} uncovered"
          + (f", {len(exempt)} claimed trivial" if exempt else "")
          + (f", {predates} predate the rule" if predates else "")
          + (f", {len(bogus)} bad citation(s)" if bogus else ""))
    if late and not missing:
        print("  note: an entry inherits its commit body's richness. A terse body"
              " yields a thin entry whoever writes it,")
        print("        and the recovery for a terse body is the session log, not"
              " the diff.")
    return 1 if (missing or bogus) else 0


if __name__ == "__main__":
    sys.exit(main())
