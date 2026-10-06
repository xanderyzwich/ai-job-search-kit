# Skill: <Board|ATS> — <Surface Name>

**Load when:** <the one situation that brings a reader here — sweeping this
board, or applying through this vendor. One or two lines, never more than
three.>

**Addressed BY NAME** (`skills/<boards|ats>/<slug>.md`), not by routing. Shared
rules live in `../board-strategy.md` (discovery) or `../form-filling.md`
(application); this file carries only what is specific to this surface.

---

## Capability — as of <YYYY-MM-DD>

| | | |
|---|---|---|
| listing page | text-readable / needs browser / n/a | |
| individual posting | fetches / needs browser / API | |
| application form | text-readable / `form_input` works / n/a | |

**Re-probe once per SWEEP, not per listing, and update this block with the
date when it changes.** A surface's capability is stable within a sweep and not
across months — one board was recorded browser-only in August and fetched
cleanly in September, and the stale row silently forced the browser onto the
highest-volume board for six weeks.

**A capability change is reported, not self-written.** An agent returns it as
`capability_delta`; a context that knows this repository's standards writes it
here. See `framework/skills/agent-contracts.md`.

## Filters / queries  <!-- boards only -->

## Form mechanics  <!-- ats only -->

## Gotchas

<!--
PROVENANCE TRAVELS WITH THE RULE IT JUSTIFIES. Keep the "learned <date>,
<where>" clause on any rule that looks arbitrary without it — that clause is
what stops the rule being tidied away by someone who cannot see why it exists.

DATED LEARNING IS NOT DATED STATE. "As of <date> this board fetches" is
PROVENANCE and belongs here. A log of what was found on a given date is STATE
and belongs in data/. The CONTRACT forbids the second in skills/, not the first.
-->
