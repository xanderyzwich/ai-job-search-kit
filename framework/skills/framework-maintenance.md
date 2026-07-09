# Skill: Framework Maintenance

**Load when:** changing the system itself — adding or renaming skills,
scripts, templates, directories, or schema columns; syncing documentation
after a structural change; or auditing whether the docs still match reality.

---

## Why maintenance is its own skill

This system describes itself in several places: two READMEs, two directory
trees, a contract, a quickstart, a bootstrap script, and an always-loaded
session map. Self-description drifts exactly the way any other mirror
drifts — a structural change lands, four of the seven descriptions get
updated, and the other three quietly start lying. The fixes below were all
earned during real maintenance sessions; this file exists so the next one
doesn't rediscover them.

## The header contract (skill routing in one call)

Every skill file must deliver its complete routing information — the
`# Skill:` title and the full `**Load when:**` block — within its **first 8
lines**, with the Load-when itself at most 3 lines. Not by padding to a
fixed length; by budget. The point is that one command scans every skill's
routing without truncation, so choosing what to load costs one tool call:

```bash
grep -rA2 --include='*.md' '^\*\*Load when' framework/skills private/skills
```

(or `head -n 8` per file, guaranteed sufficient by the same budget). A
Load-when that outgrows 3 lines is a skill trying to cover two concerns —
split it before padding it.

## The ripple map: when X changes, also touch Y

- **Directory layout** (framework or the private contract) → CONTRACT's
  layout block · README tree · SESSION_INIT tree · the private instance's
  session_init map and README tree · QUICKSTART steps 1–2 ·
  **bootstrap.py's DIRS/COPIES/SEEDS lists** — the one place layout is
  deliberately duplicated in code, and the easiest to forget.
- **A script added or changed** → the task-time skill that governs its
  moment (a script referenced only from setup docs is invisible when it
  matters) · the private session_init's Scripts block · QUICKSTART's copy
  step if it installs into `private/` · the scripts lines in README and
  SESSION_INIT trees · CONTRACT if it's contract-level. Framework copies
  are canonical; re-copy installed private copies after upstream changes.
- **Tracker schema** → CONTRACT schema text · the template CSV · migrate
  the live CSV (backup to `temp/` first) · confirm the readers still
  tolerate it. Standing compatibility rule: columns get **added, never
  renamed or removed**; scripts read by column name and treat absent or
  blank as empty.
- **A new skill** → the header contract above · a CHANGELOG line if
  public. Nothing enumerates skills by design (discovery is the header
  scan), so there's no index to update — keep it that way.
- **A template** → bootstrap.py's COPIES list · QUICKSTART.
- **Anything public-visible** → a CHANGELOG entry, tied to the failure or
  need that motivated it.

## Change workflow

1. **Order the work:** rules/structure first, data corrections second,
   enhancements third — one commit per activity, so each is reviewable and
   revertable on its own.
2. **Replacing a generator:** fidelity gate before the swap — compare old
   and new output mechanically (text, styles, whatever the artifact
   carries), and verify the checked-in artifacts match the OLD generator
   first, so no manual edit gets silently clobbered.
3. **Migrating live data:** copy the file to `temp/` first. One-off
   migration scripts live in `temp/` and get deleted after they run;
   they're scaffolding, not tooling.
4. **Every public commit:** run `git status` and read it, then grep the
   new/changed public files for personal data. The `.gitignore` is a
   backstop, not the check.

## The two closing audits

End every maintenance batch by asking, and actually checking:

1. **Do the human-readable docs match reality?** Both READMEs, QUICKSTART,
   both directory trees, CONTRACT — against the actual filesystem.
2. **Is every script wired to its moment?** Named in the task-time skill
   that governs when it runs, and in the always-loaded private map — not
   just in setup docs.

If either audit finds nothing, say so and stop; if it finds something, the
fix belongs in the same batch, not a someday list.
