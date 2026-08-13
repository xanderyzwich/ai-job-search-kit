# Changelog

The public framework's history, newest first. Dates are commit dates; the
framework is extracted from a working private instance, so entries here
generally land after the pattern they describe survived real use. The
private search data has its own repository and its own history — nothing
from it appears here.

## 2026-08-13 — Refreshing the persistent copy is the assistant's job, and it goes last

The session-init file is designed to be loaded once into a persistent context
store rather than re-read every session, which is what makes it cheap. The cost
is a second copy that goes stale the moment the file changes, so the ripple map
has long said to refresh it. What it didn't say is who does it, and the default
assumption — that a human re-uploads it — turned out to be wrong in at least one
setup, where the store was writable through a tool that had been available the
whole time. Months of handing back a manual step that never needed to be manual.

So the entry now says the assistant does it whenever the store is writable, and
only falls back to asking when it genuinely isn't — in which case it has to be
named as an outstanding step rather than quietly assumed.

The more interesting half is ordering. Refreshing the copy as soon as the file
is saved feels right and is wrong: any later edit in the same batch can
invalidate a line in it, including an edit to a completely different file. That
happened here — a `.gitignore` change falsified a sentence in the map minutes
after a correct copy had been uploaded. The ripple therefore fires at the end of
the batch, after the last change that could touch the file, and any
"copy refreshed" stamp waits for that final verified upload. Verified meaning
read back, like any other write.

## 2026-08-13 — One log heading per day, because checkpoint closes fragment it

The close step is deliberately not just an end-of-day ritual: running it at
every meaningful batch of edits is what makes each checkpoint a recovery point,
and because it amends, doing so costs nothing in commit noise. The fold didn't
match that design. It inserted a fresh `## Session Notes (date)` heading above
the newest entry every time it ran, so a day with four checkpoints produced
four headings carrying the same date.

That isn't only untidy. Session start is contracted to read the top entry of
the log for recent context, and with the day split across several headings the
top one holds whatever happened in the last twenty minutes rather than the
day's arc. Worse, the fragments read as separate days to anyone scanning, which
is exactly the confusion the newest-first ordering exists to prevent.

The fold now checks whether the newest entry already carries today's date and,
if so, appends into it rather than repeating the heading. Within a day that
leaves entries in the order they were recorded; across days the log stays
newest-first. Existing runs of repeated same-date headings collapse cleanly,
since the old behaviour always prepended and therefore always left them
contiguous — the redundant heading is removable without moving any content, so
no note that refers to something "earlier today" can be invalidated by the
cleanup.

## 2026-08-13 — Name the working file's full path, because a decoy swallows days

Every tool here resolves its paths from its own location, so they all read and
write under `private/` regardless of the directory you invoke them from. The
docs, though, wrote the day's working file as `temp/today.md`. Read from the
repo root that names a different directory — and if one exists there, notes
written to it are accepted in silence. Both are gitignored, so there is no
error, no dirty status, nothing missing. The close step folds nothing and the
day is simply absent from the log, discoverable only when someone later
notices a gap.

That happened twice before it was traced. The second time it also produced a
confident wrong diagnosis: the close step does skip folding a working file
that holds nothing but its header, so that looked like the cause, and the
conclusion drawn was that the notes had gone into other files. They hadn't.
They were sitting intact at a path no tool reads. The header-only file was the
downstream symptom.

Four fixes, in increasing order of how much they actually help. Every path
reference in the docs and templates now reads `private/temp/...`, with a
warning that a root-level `temp/` is a trap and an instruction to check the
working file has content beyond its header before closing. The daily-log tool's
own output stopped printing the ambiguous form: it was rendering the path
relative to `private/`, so every open, status, and close taught the wrong path
to whoever read it — documentation that contradicts tool output loses, because
the tool is what people copy.

Those two only help someone who reads. The other two fail loudly instead. The
daily-log tool now checks for a root-level `temp/today.md` at open, status, and
close, and says plainly that nothing reads it and the work will be missing from
the log — the close check runs before the fold, which is the last moment the
notes can be rescued. And `/temp/` came out of the root `.gitignore`. It was
ignored for symmetry with `/private/` and `/output/`, but bootstrap creates
`temp/` under `private/`, so a root-level one is never legitimate. Ignoring it
was the reason a stray directory full of a day's work never appeared in `git
status`.

The general shape is worth stating. When a wrong path silently succeeds, the
failure is invisible by construction, and writing the correct path in prose
does not fix it — that was tried, and the second occurrence followed the first
by a month. Delete the decoy if it isn't sanctioned, make the tool print the
unambiguous path every time it runs, and add a check that names the mistake out
loud. Prose is the weakest of the four.

## 2026-08-13 — Two kinds of resume mirror, and each check where it fires

The platform-copies idea started from a file problem: an ATS auto-attached a
cached stale PDF to live applications. So the rule became "a release walks the
inventory of every platform storing a copy." Two things were wrong with that.

It missed the copies most people actually read. A professional-network
profile's own experience section and a personal site listed on applications are
retyped prose, not uploaded files, so they drift differently: not merely stale,
but contradictory on facts. A release that re-dates an employment range, and
then walks only the stored files, ships a profile that disagrees with the
resume about where the candidate works and when. Nothing will prompt that fix,
because there's no submit event to hang a check on.

And for the stored files it was the wrong moment. A stale stored file can only
do damage when something is submitted through that system, so the release now
just marks those stale in the inventory and the refresh lands in the apply
ritual, at submit time, for the one system in play. Walking every ATS on
release day spends effort on systems the search may never touch again, and the
effort expires the next time the resume changes.

So the release section of the search-apply ritual splits the inventory in two
and sends each half to the moment where its check actually fires, apply-ritual
step 2 refreshes the stored copy rather than only verifying it, and the ripple
map records the distinction. One addition from practice: check the field's
character limit before drafting a content mirror. A capped field makes a
release a selection problem rather than an append, and finding that out after
the copy is written wastes the draft.

## 2026-08-13 — The tracker's column-shift bug fails loudly now

A single unquoted comma inside a tracker field shifts every column after it,
and the last columns are the analysis ones — `source`, `lane`,
`resume_version`, `notes`, `found_via`. The row still parses, the views still
render, and the funnel report still prints a resume-version split built from
fields reading their neighbors' values. This was found, repaired by hand, and
then found again weeks later on eight fresh rows, because the repair shipped
without a guard: the history generator reported "0 unrecognized" the whole
time, since it tolerated the shape rather than validating it.

`build_history.py` now counts fields against the header on every row and
exits without generating anything if any row disagrees, naming the line
number, the field count, and the organization and role so the row is findable
without a diff. `funnel_report.py` imports the same loader instead of doing
its own `DictReader` pass — a guard that only one of two readers honors is a
guard that gets routed around. The application-tracking skill gained the
reasoning, so the failure is legible at the moment it fires rather than only
in the script.

## 2026-07-17 — A skills ledger under the resume, so match/gap stops guessing

Match/gap reads kept getting a candidate's own stack wrong — a language flagged
as a gap when it was a decade of tooling, a database counted as a match when the
real engine was a different one under a shared brand name. The facts were correct
in the experience summary; the judgment step just wasn't consulting them, running
off recall instead.

So the resume content file now carries a two-layer skills ledger. `skills` became
a group → item → children tree where each node can hold `depth`, `years`, and the
`canonical` spelling listings use; a sibling `context_ledger` records off-resume
technologies as evaluated-not-adopted, honest-gap, or tooling-only. The renderer
prints names only and drops every tag, so the resume is unchanged (verified
byte-for-byte across both lanes before the swap). The match/gap step in the search
ritual now resolves every JD term against both layers rather than from memory, and
the maintenance ripple map gained an entry so a future schema change touches the
renderer, template, CONTRACT, the resume-strategy skill, and the vetting rule
together.

## 2026-07-17 — The weekly review, anchored to Friday's close

The weekly pipeline review used to ride a rolling seven-day timer, so it drifted
to whatever weekday it last happened to run. It's now weekday-anchored: a ritual
in the stamps file can carry `anchor: <weekday>`, and the weekly review uses
`anchor: friday`. It comes due every Friday and stays due if a Friday is missed,
so a skipped week surfaces at the next `open` instead of resetting the clock.

Running `close` on a due Friday now performs the measurable half of the review:
it runs the funnel report, writes it to `data/funnel_report.md`, stamps the
ritual, and makes its own `weekly-review: <date>` commit — kept separate from
the daily `log:` commit so the week's measurement is its own event in history.
The judgment steps (staleness sweeps, the passed-date scan) stay in-session,
done before the close.

## 2026-07-16 — Public-to-private handoff prompt, and a template close ritual

Two follow-ons to the first-session parity work. The template's end-of-session
guidance was one thin sentence while the mature private map has a full close
ritual, so the template now carries it: rewrite the open-threads file so the
next startup reads truth, promote durable learnings into a skill file, and run
the daily-log `close` (or update the log by hand). It stops short of
prescribing optional files (`companies/`, outreach queues, rituals) a new user
may not have. And the public-to-private transition is now prompted explicitly:
`SESSION_INIT.md` spells out that the private map is generated from the
template by bootstrap, must be personalized, and supersedes the generic
checklist permanently from the next session on; `bootstrap.py`'s next-steps
names personalizing it.

## 2026-07-16 — First-session parity with long-term usage

The context-map/ripple discipline — and, further back, reading current state
at startup — had landed in the mature private session-init checklist but not
in the two first-time entry points: the public `SESSION_INIT.md` generic
fallback and the `templates/session_init.md` a new instance inherits. A
first-time user would have silently skipped checks that long-term usage
treats as mandatory. Both were brought to parity with the mature checklist:
read current state (open threads + session log) before acting; regenerate and
read the context map, and consult its ripple section before editing any
framework or root-doc file; and route skills through `framework/README.md`.
The generic fallback calls `build_context_map.py` directly (it assumes no
installed tooling); the template uses the daily-log tool's `open` when present
and falls back to the script otherwise.

## 2026-07-16 — The context map: routing generated at load, not remembered

The template-honesty change below shipped without its documentation ripples
— the CHANGELOG, QUICKSTART, and bootstrap updates got caught only when
asked about explicitly. The cause wasn't a bad skill header; it was trigger
timing. The Load-when scan that routes tasks to skills is a session-start
ritual, but framework edits arrive mid-session as a pivot, and nothing
re-invoked the scan at the moment of the edit. The map existed; nobody
opened it.

Fix: stop relying on remembering to scan. `build_context_map.py` now runs
from `daily_log.py open` at every session start and materializes
`private/temp/context_map.md` — every skill's Load-when header (routing)
plus the ripple map, lifted verbatim from `framework-maintenance.md`. It's
generated, gitignored, and rebuilt each session, so it can't drift: a view,
never a source. The point is that "what to touch when" sits in context from
the first moment, so a mid-session pivot into a framework edit already has
the ripple obligations in front of it. The generator extracts rather than
re-encodes — skill headers and the ripple-map section stay the single
sources of truth — so the only new coupling is the section heading the
extractor keys off, which fails loudly (empty section) if renamed.

Per the ripple map, adding the script also touched the scripts lines in the
README, SESSION_INIT, and framework/README trees; the private session-init
map's checklist and scripts block; CONTRACT's generated-files table; and
session-continuity. Dogfooded: the map was run against its own change.

## 2026-07-16 — Template honesty, and a shape for feedback docs

A documentation audit caught the root README claiming `templates/` held
"blank versions of every file private/ needs." The framework deliberately
templates only files with a canonical *shape*: state files (session log,
open threads) start empty, and generated views (application history, build
record) come from scripts — three buckets, not one. `CONTRACT.md` already
sorted the files correctly; only the summary had drifted. Two fixes:

- **Wording aligned to the design.** The root README's templates line now
  names the three buckets instead of implying a template per file, and
  `framework/README.md`'s templates entry reads "every file type that has
  one."
- **A feedback template, optional by design.** `framework/templates/feedback.md`
  gives feedback docs a canonical shape — a free-text record of the feedback
  plus an actionable takeaways list — without requiring any to exist. Like
  the per-company brief, it's an on-demand template: created when feedback
  actually arrives, not instantiated at bootstrap, so `bootstrap.py`'s COPIES
  list is deliberately left untouched. QUICKSTART and CONTRACT note where the
  shape lives.

## 2026-07-10 — Discovery-point tracking in the funnel

The tracker's `source` column answers "which channel"; it can't answer
"which specific place keeps turning up roles worth applying to" — a board
listing URL, a saved search, a person. New `found_via` column (URL
preferred, short text allowed, blank when it would only repeat `source`),
added per the standing schema rule: columns are added, never renamed, and
readers treat absent as blank. The funnel report gains a discovery-point
split, grouping URL values by domain so the report measures places rather
than fragmenting into one-row groups. The application-tracking skill now
lists four analysis columns to fill at log time.

## 2026-07-10 — The public half got its own index

Earned by a real failure: a per-company call brief was regenerated without
its template because nothing at task time routed to `framework/templates/`
— the directory existed only as a path inside one grep command, and the
skills that govern brief-writing never named it. Three fixes, each at the
layer that failed:

- **`framework/README.md`** — a small routing index of the public half
  (skills, templates, scripts, contract; what each is and when to read
  it). A private instance's session init points here once; new skills and
  templates announce themselves by adding a README line in the same commit
  that adds them, so the always-loaded private map never needs editing to
  keep discovery working.
- **Templates rule** stated where it's discoverable: before creating any
  new file, check `templates/` — if a template exists, the file is created
  from it and keeps its sections through later edits. The screen-prep
  skill now names `templates/company_brief.md` directly, and the
  session-init template routes new instances through the README.
- **Ripple map updated** in the maintenance skill: layout changes, new
  templates, and script changes now list `framework/README.md` among the
  mirrors to touch.

## 2026-07-09 — Drift prevention, the data layer, and working tooling

A full-system review found the framework's own instance violating several of
its own rules: a canonical config file that had drifted behind a decided
policy, a scrubbed claim surviving inside a skill file's example, dated
market data embedded in a methodology file, and a hand-maintained mirror of
the application tracker that had already broken once and needed
reconstruction. Every fix became a rule, and most rules became structure:

- **Data layer.** The private contract now separates working state
  (`data/`: session log, an open-threads file read first every session,
  dated snapshots, per-company call briefs) from methodology (`skills/`),
  with the rule that a methodology file never carries an "as of" fact.
- **Generated views.** The tracker CSV is the single hand-edited
  application record; the human-readable history is rendered from it by
  script. Mirror drift is now structurally impossible rather than
  procedurally discouraged.
- **Drift-prevention rules** added to the session-continuity skill: policy
  changes land in canonical files the same session they're decided;
  scrubbing an overclaim means searching the entire private instance,
  including examples inside skill files; dated content lives only in the
  data layer.
- **One commit per day.** A daily-log tool folds the day's working notes
  into the log, archives old entries, regenerates views, and amends a
  single dated commit until it's pushed.
- **Communications skills.** Warm outreach (sequencing, queue pattern,
  raising gates in conversation rather than on forms) and screen-call prep
  (the per-company brief) — the post-application half of the funnel the
  framework previously didn't cover, added as the instance's own pipeline
  reached that stage.
- **A measured funnel.** New tracker columns (source, lane, resume version)
  and a report script turning them into response and advance rates, split
  by each.
- **Generalized resume builder.** The two per-lane build scripts turned out
  to be identical layout code with different content baked in; they became
  one layout-only renderer driven by a YAML content file, verified
  output-identical before the swap. A positioning-strategy change is now a
  data edit. This closed the framework's oldest known limitation.
- **Onboarding and display.** QUICKSTART rewritten for the new layout with
  a tooling copy step; README gained the state-vs-methodology and
  measured-funnel design ideas, an explicit two-stage session-init
  lifecycle, and a work-sample section; the private instance documented a
  full run-it-by-hand fallback.
- **Maintenance became a skill.** The framework describes itself in seven
  places, and self-description drifts like any other mirror — so the
  ripple map (when X changes, also touch Y, including the bootstrap
  script's deliberate layout duplication), the change workflow (fidelity
  gates, migration backups, boundary checks), and two closing audits now
  live in `framework/skills/framework-maintenance.md`. It also sets the
  skill header contract: complete routing information in the first 8 lines
  of every skill, Load-when at most 3 lines, so one grep scans every
  skill's purpose in a single call.
- **The pipeline's rituals got runbooks.** Session boundaries (init and
  end-of-day) live in the private session map; the search and apply
  sequences live in a new ordered runbook skill that sequences the other
  skills by pointer rather than copying their content — including the
  verify-what-the-ATS-actually-attached step, earned when a platform
  auto-attached a cached stale resume. Non-daily rituals get machine-
  checked stamps: the daily-log tool records last-run dates and warns at
  session start when a cadence has elapsed, and the resume renderer
  writes a build record (timestamp plus content hash) so platform-copy
  staleness is a mechanical compare instead of an act of memory.

## 2026-07-06 — Published

Pre-publication audit of every public file for personal-data leakage
(nothing found; the config-separation rule did its job), then announced
publicly with the repository linked. No code changes — the boundary held
without needing any.

## 2026-07-01 — Extraction

The framework's first public form, extracted from a private methodology that
had grown across several weeks of real search sessions: repository layout
and the public/private split, the session-init startup sequence, the single
methodology file decomposed into small on-demand skills, blank templates for
every private file, the quickstart including the adversarial
experience-summary generation process, the two-lane search reframing, and
the stable-map versus dynamic-log separation with the public init checking
for and loading a private counterpart. Ten commits in one day because the
patterns already existed — the work was separating the reusable system from
one person's data.
