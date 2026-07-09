# Changelog

The public framework's history, newest first. Dates are commit dates; the
framework is extracted from a working private instance, so entries here
generally land after the pattern they describe survived real use. The
private search data has its own repository and its own history — nothing
from it appears here.

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
