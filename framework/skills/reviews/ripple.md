# Skill: Review — Ripple

**Load when:** you are a REVIEW AGENT dispatched by `framework-audits.md` to check that every file a change was supposed to touch WAS touched. Not for making changes.

**Your constraints:** read-only. No edits, no staging, no commits, no git writes, no network. Write ONLY the report file the dispatcher names for you (yours alone — two other reviewers are writing their own files at the same time; never touch theirs). Never copy a person's name, an employer, a dollar figure or an address into the report; cite `file:line`.

---

## Scope

The dispatcher gives you a git range or a file list. Every change in scope is a row you must trace. With no scope, say so and mark the scope UNVERIFIED.

## Where the ripples live

- **`framework/skills/framework-ripple-map.md`** is the table of "when X changes, also touch Y". Read it in full. `private/temp/context_map.md` carries a generated verbatim copy; it is a view, never the source.
- **The mirrors the table names:** the README trees, `framework/README.md`, `SESSION_INIT.md`, `QUICKSTART.md`, the CONTRACT layout and schemas, `framework/scripts/bootstrap.py` (its `DIRS`, `COPIES` and `SEEDS` lists, the one place layout is deliberately duplicated in code), the instance's README tree and session-init map, and the always-loaded instruction files that DESCRIBE a changed thing.

## Method

For EVERY change in scope:

1. Find the ripple rule(s) that apply. If none applies and the change is structural, that is itself a finding: the table is missing a row.
2. Walk each mirror the rule names and verify it was actually updated, by reading the mirror, not by trusting the commit message.
3. Apply the standing mechanical checks:
   - **Installed copies:** `cmp` each script the installer copies against its canonical source (and the resume builder against its instance copy).
   - **Generated files:** a change to a generator's source needs the generated output re-rendered and not hand-edited (read the generated file's header).
   - **A new directory:** the CONTRACT layout, `bootstrap.py` `DIRS`, every README tree and `SESSION_INIT.md`.
   - **A new skill:** its header contract, and whether its directory is conventioned (then it belongs in `COLLAPSED_DIRS` in `build_context_map.py`) or routed (then it appears in the context map).
   - **A changed schema, field or file shape:** the CONTRACT row, the template, and every script or skill that reads or writes it.
   - **Every public commit** has a CHANGELOG entry: run `python3 framework/scripts/check_changelog.py`.
4. For a change to HOW A DATA FILE IS USED, find every reader and writer of that file (grep the scripts and skills for its name) and confirm each still matches.

## Report

A markdown table: severity (HIGH / MED / LOW), the change, the rule that requires the touch, what is out of step (`file:line`), the one-line fix. A 3-line summary first, worst first, capped at 30 rows. Report ONLY real misses; mark anything you cannot verify UNVERIFIED. A check that found nothing must say how you know it could have found something. End with a three-sentence hand-back naming the report file.
