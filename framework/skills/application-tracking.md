# Skill: Application Tracking

**Load when:** logging an application, checking status on a previous
application, or reviewing overall search progress.

**Depends on:** `private/job_tracker.csv` for the actual log; schema documented
in `framework/CONTRACT.md`.

---

## Why track at all

A search running across many roles and many weeks loses information fast
without a structured log: which recruiter was contacted, whether a cover
letter was sent, what stage an application reached, whether a follow-up is
due. The tracker is the one place this state lives outside of memory or
scattered notes, and it should be the source checked before assuming an
application's status rather than reconstructing it from recollection.

## What to log, and when

Log immediately after the action, not at the end of a session from memory.
Memory-based logging loses exactly the details, an exact recruiter name, a
specific answer given to a screening question, that matter most if the
application resurfaces later.

At minimum, every logged application should capture: date, organization,
role, whether a referral or warm contact was involved, whether a cover letter
was sent (and where the file lives, if generated), and current status.

## Reading the tracker before acting

Before applying to an organization, check the tracker for prior activity
there. A second application to the same organization without checking can
create a confusing duplicate record, or worse, contradict answers already
given in a prior application (a different desired salary, a different
answer to a repeated screening question).

## Status hygiene

Update status as it changes rather than only logging the initial application.
A tracker that only ever shows "applied" for every row loses its value as a
progress signal; the useful information is in the transitions (applied →
screening → rejected, or applied → no response after N weeks).

## Volume is not the lever

If a tracker shows a high application volume with a very low conversion rate
to any later stage, that's a signal to revisit strategy, which lanes are being
targeted, whether cold applications versus warm introductions are the right
mix, rather than a signal to increase volume further. The tracker's aggregate
pattern matters as much as any individual row.
