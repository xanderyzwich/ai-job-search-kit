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
Load-when that outgrows 3 lines is usually a skill trying to cover two
concerns — split it before padding it.

**`framework/scripts/lint_skills.py` checks this mechanically, and the daily-log tool
runs it at `close`** so the check happens at a ritual rather than on request.
It ERRORS on what breaks the scan — a missing routing header, or one below the
line budget — **and on a backticked file reference that resolves to nothing**,
which is how a move or rename announces itself. It WARNS on the rest, including
file size. The size
warning is how the next oversized file announces itself: the one that prompted
all this had reached 2,207 lines before anyone measured it.

**Keep the error set narrow.** The first version of that script also errored on
a literal title prefix and on any Load-when over three lines, and would have
forced churn across fifteen files for two things that were not problems — an
instance may title its skills in its own house style, and a fourth line is
usually a disambiguation clause worth keeping.

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
  matters) · `bootstrap.py`'s COPIES if it installs into `private/` ·
  CONTRACT if it's contract-level. Framework copies are canonical; re-copy
  installed private copies after upstream changes.

  **Nothing else enumerates scripts, by design — the same rule that already
  held for skills.** A script's first docstring line is its routing header and
  the context map indexes it from there, so there is no list to update. This
  used to name five more mirrors: a Scripts block in the private session_init,
  a transcribed `cp` list in QUICKSTART, and script lines in three trees. They
  were removed 2026-10-01 after the session_init block went stale on the day
  two scripts were added and the QUICKSTART list still said "the three
  scripts" when there were five. **If you find yourself writing a list of
  scripts into a document, you are recreating a mirror that was deliberately
  deleted** — write the reference instead.
- **Tracker schema** → CONTRACT schema text · the template CSV · migrate
  the live CSV (backup to `temp/` first) · confirm the readers still
  tolerate it. Standing compatibility rule: columns get **added, never
  renamed or removed**; scripts read by column name and treat absent or
  blank as empty.
- **ANY public change — not just a new skill** → a CHANGELOG entry, in the
  same commit. **This is the ripple most often skipped**: an audit on
  2026-10-06 found nine of fourteen framework-touching commits had none, and
  the entries had to be reconstructed afterwards from the diffs. The CHANGELOG
  is the public record of WHY the framework looks like this, tied to the
  failure that forced each change — a commit message is not a substitute,
  because nobody reads a log to learn a system's reasoning. A new skill also
  owes the header contract above.

  **`framework/scripts/check_changelog.py` verifies this and runs at `close`.**
  A commit counts as covered if it touched the CHANGELOG itself, or if a later
  entry cites its hash:
  `<!-- covers: abc1234 · backfilled YYYY-MM-DD -->` — invisible in rendered
  Markdown, greppable in source, and the hash is verified to resolve so a typo
  cannot read as covered forever. **The two are counted separately on purpose.**
  An entry written at the decision records why the alternative was rejected; one
  reconstructed from a diff records only what changed, and that difference does
  not survive the week. A rising backfill count means the rule is slipping even
  while every commit technically passes. A skill in a CONVENTIONED directory (one file per board, per
  ATS vendor, per any other named surface) still needs the header, but nothing
  routes to it — the parent derives the path from the surface name, and the
  directory listing is the inventory. `build_context_map.py`'s `COLLAPSED_DIRS`
  is what keeps a dozen near-identical entries from drowning the skills that
  ARE routed; add a new conventioned directory there or it will. Nothing enumerates skills by design (discovery is the header
  scan), so there's no index to update — keep it that way.
- **Anything an always-loaded instance file DESCRIBES** (the private
  `CLAUDE.md`, or whatever the harness auto-loads) → that file. It was
  missing from this map until 2026-10-01 and had gone stale twice over:
  it carried a hard-coded skill COUNT, and it told readers the generated
  map indexed skills when it had begun indexing scripts too. **Prefer
  deleting the mirror to adding an obligation** — a count or a list in an
  always-loaded file is drift waiting to happen, so describe what the
  generated view contains, never how many things are in it.
- **A template** → bootstrap.py's COPIES list · QUICKSTART · its line in
  framework/README.md's templates entry — the README is how an
  always-loaded private map discovers new templates without being edited,
  so a template missing from it is undiscoverable at task time.
- **The private session_init** → refresh any persistent-context copy of it
  (a Claude Project or similar) **in the same session, before the session
  ends**. The whole point of loading it into static context is that it rarely
  changes; when it DOES change, the loaded copy is stale until it's replaced —
  a drift that produced eight stale states in one day of heavy maintenance
  before this entry existed.

  **If the persistent store is writable through a tool available in the
  session, the assistant does this itself rather than handing it back as a
  human step.** Read the current stored copy, write the updated file to the
  same path, and confirm the round-trip. Only when no such tool exists does
  this become a request to the human, and then it gets named explicitly as an
  outstanding step rather than assumed.

  Two traps, both seen in practice. First, the upload is not done until it's
  verified — treat it like any other write and read it back. Second, and less
  obvious: **a later change in the same session re-stales the copy you just
  uploaded.** Editing session_init, uploading it, and then making one more
  edit (even to an unrelated file, if it invalidates a line in the map) leaves
  the store wrong again. So this ripple fires at the END of the batch, after
  the last edit that could touch it, not the moment session_init is first
  saved. Anything that stamps a "copy refreshed" ritual stamps it only after
  that final upload.
- **A new resume version** → the `resume_version` tag on subsequent
  applications · a dated log note that starts the funnel's before/after clock
  · the instance's platform-copies inventory, which holds two kinds of mirror
  that are NOT walked the same way (see the release section of
  `search-apply-ritual.md`): **submission-system copies** get marked stale and
  refreshed at submit time for that one system, since that's the only moment a
  stale stored file can reach an employer; **content mirrors** — a
  professional-network profile's experience section, a personal site listed on
  applications — get refreshed at release, because nothing else will ever
  prompt it and they fail differently. A stored file is merely old. A content
  mirror is retyped prose, so it contradicts the resume on facts (titles,
  employment date ranges, present-vs-past tense) while looking current, and
  strangers read it unprompted. Check the field's character limit before
  drafting one: a capped field makes a release a selection problem, not an
  append.
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

## The changelog entry — what it owes, and how to rebuild one

**Any change to the mechanisms of this framework owes an entry, in the same
commit.** Not "a new skill" — that phrasing was the rule for a while and it is
why nine of fourteen framework-touching commits went unrecorded: most of them
added no skill at all.

**Trivial changes are exempt, but the exemption must be CLAIMED, not assumed.**
A reference rename, a typo, a path correction, a reflow — put
`[no-changelog: <reason>]` in the commit message. `check_changelog.py` counts
claimed exemptions separately and prints the total, so "trivial" cannot quietly
become the default. If the mechanism changed, it is not trivial, however small
the diff.

### Write the body, not just the entry

**An entry inherits its commit body's richness.** Measured on this repo: the
entries that survived being written up later came from commit bodies of 200–425
words; the one that came out thin came from a body of 41. Authorship and timing
were coincidences — body length was the variable.

So the preservation mechanism is the commit body. It should carry **what
changed, what forced it, and the numbers** — the measurement, the failure, the
count. Anyone writing the entry later, including you next week, has only what
the body says.

### Who the entry is written for

**Someone who was not there, does not have the repo checked out, and is reading
this file on its own.** That is the actual audience: the changelog is the public
record of why this framework looks the way it does, and for a portfolio-visible
repo it is often the only part anyone reads in depth. A commit message is not a
substitute — nobody reads a git log to learn a system's reasoning — and neither
is a diff, which the reader does not have open.

Three consequences:

- **Name the problem, not just the fix.** What was going wrong, what it cost,
  and how it was noticed. A reader learns more from "nine of fourteen commits
  had no entry, and the misses skewed toward fixes" than from "improved
  changelog coverage."
- **Keep the numbers.** They are what make an entry credible rather than
  decorative, and they survive anonymisation: *one of twenty-one requisitions*,
  *2.2K tokens against 149K*, *0 for 12*. Strip the employer, keep the
  measurement.
- **Do not polish the failures out.** The portfolio value is in the failures
  being visible and honestly described — a record that only contains successes
  reads as marketing and teaches nobody anything. An entry that says a first
  attempt was wrong, and why, is worth more than one that implies the design
  arrived finished.

**The filter for what deserves one is not diff size.** It is *would someone
otherwise relearn this the hard way*. A reorganisation is visible in the tree; a
silent failure mode is not, and the silent ones are exactly what gets
rediscovered expensively. The historical misses skewed toward fixes and
follow-ups for precisely this reason — they felt small and carried the most
transferable content.

### Rebuilding an entry after the fact

In this order, and stop when you have the mechanism and the numbers:

1. **The commit body.** Read the FULL message — subject and body. A rich body
   usually contains the entry already.
2. **The session log for that date.** This is the recovery when the body is
   terse, and it is where people look last. One thin entry here was missing the
   measurement that gave its change the whole point — a single keyword returning
   one of twenty-one open requisitions — and that number had been in the day's
   log all along.
3. **The diff.** Last resort. It tells you what changed and never why, which
   produces text that reads like a record and carries nothing.

**If none of those yield a reason, write a short honest entry or none at all.**
A thin entry is worse than an absence, because it stops the next person looking
further.

**Cite what you backfill.** A late entry names the commits it covers:
`<!-- covers: abc1234 · backfilled YYYY-MM-DD -->` — invisible in rendered
Markdown, greppable in source, and the hash is verified to resolve so a typo
cannot read as covered forever. Written-at-the-time and backfilled are counted
separately on purpose; collapsing them hides the only signal worth watching.

**Do not chase history.** The rule has a start date and commits before it are
reported as predating it. Backfilling months of history from diffs alone
produces a wall of thin entries that look like records.

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

## The three closing audits

End every maintenance batch by asking, and actually checking:

1. **Do the human-readable docs match reality?** Both READMEs, QUICKSTART,
   both directory trees, CONTRACT — against the actual filesystem.
2. **Is every script wired to its moment?** Named in the task-time skill
   that governs when it runs, and in the always-loaded private map — not
   just in setup docs.
3. **Can every role actually do its job with what it loads?** See below. Run
   this one after any split, move, or rename — it is the only audit here that
   asks about READERS rather than files.

If an audit finds nothing, say so and stop; if it finds something, the fix
belongs in the same batch, not a someday list.

### Audit 3 — trace a role, not a file

Audits 1 and 2 ask whether the files are right and whether they are reachable.
Both can pass while a role is unable to work, because neither asks what any
particular reader ends up holding. On 2026-10-06 every structural check passed
— valid headers, resolving references, planned sizes — while **three roles were
missing inputs they could not function without**, including one whose skill
documents a real failure caused by exactly the input that had been left out.

For each role in turn:

1. **Write down what it must DO**, from the flow, in one line. Not what it
   loads — what it produces.
2. **List what it loads**, resolving every path. An input that does not exist
   is the cheap failure and the structural checks already catch it.
3. **Close the list transitively.** For every skill it loads, read that skill's
   `Depends on:` and confirm each name is also in the role's list. This is
   where the 2026-10-06 defect was: a role loaded the scoring skill and none of
   the six things that skill declares it needs.
4. **Ask the judgment question the script cannot:** given ONLY this, could the
   reader produce what step 1 says it must? Read the files and answer honestly.
   The failures look like a rule filed under the wrong reader — present in the
   repo, absent from the one role that performs it.
5. **Check for two documents disagreeing about who does what.** Closing a list
   transitively tends to surface these: one file says the scorer deduplicates,
   the flow says the coordinator does, and following both means an agent
   repeating finished work with hundreds of lines of state it should never have
   loaded.
6. **Record the load size per role.** Not a pass/fail — a cost. A role that is
   expensive for a good reason (honest matching needs the whole verified
   record) is different from one that is expensive by accident.

**Why this is not a script.** The mechanical half — resolve the paths, check
the transitive closure — could be automated, and it would have caught the worst
defect. It is not automated yet because the load lists are prose in a table,
and making them machine-readable means either parsing that prose, which is
fragile, or adding a structured copy, which is a second source of truth about
the same thing. **If those lists ever become structured for another reason,
build the check that day.** Until then the procedure above finds more than the
script would, because step 4 is the half that matters and no parser can do it.
