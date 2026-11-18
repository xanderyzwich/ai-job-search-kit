# Skill: Review — Dogfood

**Load when:** you are a REVIEW AGENT dispatched by `framework-audits.md` to check whether a change followed the project's OWN rules and whether those rules still agree with each other. Not for making changes.

**Your constraints:** read-only. No edits, no staging, no commits, no git writes, no network. Write ONLY the report file the dispatcher names. Never copy a person's name, an employer, a dollar figure or an address into the report; cite `file:line`.

---

## The question

A project that asks others to follow rules has to follow them itself. Dogfood asks two things: **did the work in scope obey the project's declared principles**, and **do the files that state those principles now agree with each other**?

## Where the principles live (read each that exists)

- `framework/skills/framework-maintenance.md`: the skill-versus-data test (a skill holds what the task needs, not what happened; history and state go to data files), method travels but research about one employer does not, the header contract.
- The always-loaded instructions (root `CLAUDE.md`, instance `private/CLAUDE.md`) and the instance's orchestration skill (`private/skills/coordination.md`) for the working rules: how agents are prompted (name the files, never ask an agent to rediscover an index), how long work is run, what is never done without the owner.
- **The owner's standing decisions,** which live in the instance: the settled-decisions block of `private/data/open_threads.md`, `private/profile.yml`, `private/skills/search-constraints.md`, and the lane and scoring skills. These are the rules most likely to be stated in more than one place and to drift apart.
- `framework/templates/` for how each kind of file must be shaped.

## What to check

1. **Did the work follow the rules?** New skill files hold learnings only (no per-run counts, results or narrative); removed history was archived verbatim in a data file; new data files obey their template; tracker edits were backed up and CRLF-safe; anything generated was not hand-edited; no convention was invented where a skill was silent without being flagged.
2. **Do the rules agree?** For each standing decision touched in scope, find EVERY file that states a rule on the same matter and list any pair that now gives different instructions (thresholds, orderings, exclusions, who decides, what a status means). A decision recorded in one file and contradicted in another is the most common finding.
3. **Reader test.** Pick two roles that load the changed material (for example a scoring agent and a sweep coordinator) and trace each from its entry point to its outputs: can it do its job with only what it loads, or does it depend on a file it is never told to read?
4. **Stale instructions.** Anything that still describes a flow, tool or step the project has retired.
5. **Unowned items.** Decisions the owner has made that are recorded nowhere durable, or open items with no owner and no next step.

## Report

A markdown table: severity (HIGH / MED / LOW), `file:line`, the finding, the proposed fix. A 3-line summary first, worst first, capped at 35 rows. Report ONLY real findings; mark anything you cannot verify UNVERIFIED, and for a check that found nothing say how you know it could have found something. End with a three-sentence hand-back naming the report file.
