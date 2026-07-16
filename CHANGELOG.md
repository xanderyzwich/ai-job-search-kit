# Changelog

The public framework's history, newest first. Dates are commit dates; the
framework is extracted from a working private instance, so entries here
generally land after the pattern they describe survived real use. The
private search data has its own repository and its own history — nothing
from it appears here.

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
