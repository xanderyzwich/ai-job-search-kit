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

## The context map (generated at session start — read it first)

`daily_log.py open` runs `build_context_map.py`, which materializes the
ripple map below plus every skill's `Load when` header into
`private/temp/context_map.md` (gitignored, rebuilt each session — a view,
never a source). It exists so "what do I touch when" is in context from the
first moment instead of depending on a remembered header scan: this was
added after a documentation ripple was missed because the routing scan is a
session-start ritual and the edit that needed it arrived as a mid-session
pivot. Before editing any `framework/` or root-doc file, read that file's
obligations in the ripple section and touch every mirror it names in the same
batch. The generator EXTRACTS the section below verbatim rather than
re-encoding it, so this stays the one place the ripple map lives; it keys off
this heading, which fails loudly (an empty section) if the heading is renamed.

## The ripple map: when X changes, also touch Y

- **Directory layout** (framework or the private contract) → CONTRACT's
  layout block · README tree · SESSION_INIT tree · **framework/README.md**
  (the public half's own index) · the private instance's session_init map
  and README tree · QUICKSTART steps 1–2 ·
  **bootstrap.py's DIRS/COPIES/SEEDS lists** — the one place layout is
  deliberately duplicated in code, and the easiest to forget.
- **A script added or changed** → the task-time skill that governs its
  moment (a script referenced only from setup docs is invisible when it
  matters) · the private session_init's Scripts block · QUICKSTART's copy
  step if it installs into `private/` · the scripts lines in README,
  SESSION_INIT trees, and framework/README.md · CONTRACT if it's
  contract-level. Framework copies
  are canonical; re-copy installed private copies after upstream changes.
- **Tracker schema** → CONTRACT schema text · the template CSV · migrate
  the live CSV (backup to `temp/` first) · confirm the readers still
  tolerate it. Standing compatibility rule: columns get **added, never
  renamed or removed**; scripts read by column name and treat absent or
  blank as empty.
- **A new skill** → the header contract above · a CHANGELOG line if
  public. Nothing enumerates skills by design (discovery is the header
  scan), so there's no index to update — keep it that way.
- **A template** → bootstrap.py's COPIES list · QUICKSTART · its line in
  framework/README.md's templates entry — the README is how an
  always-loaded private map discovers new templates without being edited,
  so a template missing from it is undiscoverable at task time.
- **The private session_init** → refresh any persistent-context copy of it
  (a Claude Project or similar). The whole point of loading it into static
  context is that it rarely changes; when it DOES change, the loaded copy
  is stale until someone re-uploads it — a drift that produced eight stale
  states in one day of heavy maintenance before this entry existed.
- **A new resume version** → the instance's platform-copies inventory
  (every ATS/board that stores its own copy of the resume — those are
  mirrors, and one auto-attached a stale file in practice) · the
  `resume_version` tag on subsequent applications · a dated log note that
  starts the funnel's before/after clock.
- **The `resume_content.yml` schema** (the skills-ledger shape, or any new
  content key the renderer reads) → `build_resume.py` (edit the canonical
  framework copy, re-copy the private one, and fidelity-gate the render
  byte-for-byte before trusting it) · the template `resume_content.yml` ·
  CONTRACT's `resume_content.yml` row · the resume-strategy skill (framework
  `resume-lane-strategy.md` and the private `resume_strategy.md`) · the
  match/gap step in `search-apply-ritual.md`, which reads the ledger. The
  ledger is a match/gap source of truth as well as a render input, so a shape
  change ripples into both the renderer and the vetting rule.
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
