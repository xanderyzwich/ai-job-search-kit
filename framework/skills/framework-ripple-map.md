# Skill: Framework Ripple Map

**Load when:** you have just changed a `framework/` or root-doc file and need to know what else to touch in the same batch, or you are editing this table itself. Most sessions never open this file: a verbatim copy is generated into `private/temp/context_map.md` at every session start.

**Why it is its own file:** the table is consulted AFTER a change, and it is needed in full only when someone edits it, so it does not belong in the maintenance skill that every framework change loads. It was split out of `framework-maintenance.md` on 2026-11-17 (that file keeps the rules for where things belong; this one keeps the lookup).

---

## The ripple map: when X changes, also touch Y

- **Directory layout** (framework or the private contract) → CONTRACT's
  layout block · README tree · SESSION_INIT tree · **framework/README.md**
  (the public half's own index) · the private instance's session_init map
  and README tree · QUICKSTART steps 1–2 ·
  **bootstrap.py's DIRS/COPIES/SEEDS lists** — the one place layout is
  deliberately duplicated in code, and the easiest to forget.
- **A board or ATS skill added or changed** → the **mechanics / overlay split**:
  `framework/skills/boards/<x>.md` (or `ats/`) holds how the surface works
  (endpoints, data shapes, how listings lie, what is verifiable browserless) and
  nothing about one search; the instance's same-named file is the OVERLAY
  (its filters, results, decisions) and its header points at the framework file.
  A mechanics change goes to the framework file; a result or filter goes to the
  overlay. Run the leak scan: employer names and figures belong in the overlay.
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
- **A FILE MOVED OR DISSOLVED** → every reference to it, in BOTH halves — and
  the reference check only finds those it is scoped to scan, so widen the scope
  before trusting a clean run. Live pointers get repointed individually, each to
  the successor **verified to hold the content it cites**: a dissolved file has
  several successors and one destination will be wrong for most of them.
  Chronological records (a session log, an archive) keep their text and get a
  link whose TEXT is the historical path and whose TARGET is current. Write-once
  records get a `<!-- moved-refs -->` annotation instead, since their claims are
  about a date. **Search the CONTENT's vocabulary, not the referring file's**,
  before concluding anything is missing — a pointer names things in its own
  words, and grepping those words finds nothing and looks exactly like loss.
- **A new GENERATED VIEW** → answer "who reads this" BEFORE choosing a path,
  and put the answer in the file's own header. The assistant's working
  references go in the gitignored `temp/`; anything the candidate reads goes in
  `data/` and is committed, because the search is checked from a phone when the
  machine is off. **A view written to `temp/` by default is a view its intended
  reader cannot open**, which is how a calendar built for phone-reading spent
  its first day where only one machine could see it. Committed views compute
  their internal links relative to their own directory — a wrong relative link
  renders as a dead link rather than failing, so it survives review.
- **Tracker schema** → CONTRACT schema text · the template CSV · migrate
  the live CSV (backup to `temp/` first) · confirm the readers still
  tolerate it. Standing compatibility rule: columns get **added, never
  renamed or removed**; scripts read by column name and treat absent or
  blank as empty.
- **A data-file SCHEMA** — a frontmatter key, or a structured body block, in
  `data/contacts/*.md`, `data/companies/*.md` or any other hand-written
  markdown record → CONTRACT's row for that file type · the template it is
  created from · whatever parses it · **every skill whose ownership or
  fan-out table names the fact the new structure now holds.**

  **That last one is the trap, and it is why this entry exists.** A block
  that holds a fact an existing table already assigns to another file creates
  a SECOND OWNER for it, silently — so the one-owner rule gets violated by
  the very change meant to strengthen it. Grep the ownership tables for THE
  FACT, not for the filename, before writing the schema; if a row already
  claims it, that row has to narrow in the same batch or the schema does not
  land.

  **Frontmatter stays FLAT key/value scalars by contract.** The hand-rolled
  parsers split on the first colon, so a nested list reads as a present-but-
  empty value — which several of them treat as MEANINGFUL — and a line
  carrying a timestamp becomes a garbage key from the `08:30`. Both fail
  silently, and the empty-value case fails in the worst direction: a fully
  booked schedule reads as nothing scheduled. Anything needing nesting goes
  in a body block with a line grammar, which can at least report the lines it
  could not read.
- **ANYTHING EXECUTABLE — a script, a template that gets COPIED, a schema a
  parser reads** → **exercise it BEFORE the commit, not after.** Run the script
  against the real directory and against a throwaway one. Copy the template the
  way its own header says to, and look at what the copy produces. Feed the
  parser a malformed line and confirm it REPORTS rather than drops.

  **The evidence is one day's log: fourteen commits produced four features, and
  ten of the fourteen were repairs to the commit immediately before.** Every
  repair came from running the thing; not one came from re-reading it. A
  template shipped with a worked example still in it, so copying it wrote a
  fabricated meeting into a real calendar under a real person's name. A
  conformance check ran at every session close with its output captured and
  discarded, asserting nothing. A generator crashed the moment it was pointed
  outside the repository. **None of those are visible in a diff**, which is
  exactly why reading the change again is not the check.

  **A test that exercises a NEARBY path proves nothing.** One of those repairs
  was first "verified" by invoking a command that never calls the code under
  test, and it passed. Run the path that actually runs, and prove a check works
  by breaking it on purpose — if deleting the thing it guards produces no
  error, the check is decoration.

  This is not an argument for committing less often. **The commit is still the
  recovery point and the checkpoint should run constantly.** It is about which
  commit the dogfood pass lands in: before it, the history records what was
  built; after it, the history records what was nearly built and then fixed.
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

- **A new check or annotation in `framework/scripts/lint_skills.py`** → its docstring
  list · the header-contract section of `framework-maintenance.md` (the annotations
  are part of the authoring contract) · `build_context_map.py` if it changes what a
  skill's routing line should show · a CHANGELOG entry.
- **`framework/scripts/build_contact_index.py`** → the installed copy in
  `private/scripts/` (the drift check errors until it is re-copied) · the calendar
  it renders · the hard-dates format in the instance's open-items file.
- **This file itself** → `framework/scripts/build_context_map.py` extracts the `## The ripple map` section of this file by that exact heading; renaming the heading empties the generated copy. Keep the heading, and keep the table here and nowhere else.
