# Skill: Review — Standards

**Load when:** you are a REVIEW AGENT dispatched by `framework-audits.md` to check a change against the project's DECLARED STANDARDS. Not for making changes.

**Your constraints:** read-only. No edits, no staging, no commits, no git writes, no network. Write ONLY the report file the dispatcher names for you (yours alone — two other reviewers are writing their own files at the same time; never touch theirs). Never copy a person's name, an employer, a dollar figure or an address into the report; cite `file:line` instead.

---

## Scope

The dispatcher gives you a scope: a git range or a file list. Review that, not the whole repo. If you were given no scope, say so in the report and review `git log` since the last review report you can find under `temp/review-*/`; mark the scope as UNVERIFIED.

## Where the standards live (read each that exists, in this order)

1. **The always-loaded instructions:** the root `CLAUDE.md` and the instance `private/CLAUDE.md`. These carry the HARD rules: the public/private boundary, never push, which files are generated, git discipline.
2. **`framework/CONTRACT.md`:** the declared layout, file schemas and field vocabularies.
3. **`framework/skills/framework-maintenance.md`:** the header contract, the skill-versus-data test, "a skill holds learnings, not history", and the three lint annotations (`moved-refs`, `absent-refs`, `**Size budget:**`).
4. **`CHANGELOG.md`:** the standard an entry must meet is stated near the top of its history (audience, name the problem and what it cost, keep the numbers, claim a trivial exemption explicitly).
5. **`framework/templates/`:** the shape every instance file of that kind must follow.
6. **The instance's own declared standards,** where the change touched instance files: `private/skills/session_init.md` and the standing decisions recorded in `private/profile.yml` and `private/data/open_threads.md`.

## What to check

1. **Boundary.** Nothing under `framework/` or the root docs may hold a real dollar figure, a search employer, a person, a contact or an email. Derive the sets you scan for from the private half (company file names, the tracker's company column, contact names) into a variable and never print them; run `python3 framework/scripts/leak_scan.py` and explain every hit. **Prove the scan can fire** before you trust a zero (plant a probe in a scratch file, see `framework-audits.md`).
2. **Contract versus reality.** Every file, directory, key and field the CONTRACT declares against the live files: `profile.yml` key PATHS (never values), the `private/data` tree, the templates. Report anything declared but absent, or present but undeclared.
3. **Templates.** New or changed instance files against their template's own rules.
4. **Header contract.** Each skill created or edited has a title, a `**Load when:**` within 8 lines, at most 3 lines long; run `python3 framework/scripts/lint_skills.py` and explain errors. Check any annotation uses the documented format.
5. **Changelog standard.** Every public commit in scope is covered (`python3 framework/scripts/check_changelog.py`), each entry states the failure and its cost with numbers, and no trivial exemption is claimed for a change that altered a mechanism.
6. **Generated files.** Nothing generated was hand-edited: check the diffs of the generated paths (dashboards, the data README, the context map).
7. **Installed copies.** Every script the installer copies is byte-identical to its canonical source.
8. **Data discipline.** The tracker is CRLF with one physical line per row (`grep -c $'\r'` equals `wc -l`), no duplicate URL groups of the same role, every status inside the declared vocabulary.

## Report

Write the report as a markdown table: severity (HIGH / MED / LOW), `file:line`, the standard breached (quote its source `file:line`), the evidence, a one-line fix. A 3-line summary comes first. Cap at 35 rows, worst first. Mark anything you could not verify UNVERIFIED rather than guessing; a check that found nothing must say how you know the check could have found something. Report only REAL findings. End with a hand-back of three sentences that name the report file.
