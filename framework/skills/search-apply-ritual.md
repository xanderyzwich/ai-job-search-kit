# Skill: The Search & Apply Ritual

**Load when:** running a board sweep, vetting candidate roles, or
submitting an application — the ordered runbook that sequences the other
skills.

---

This file owns the ORDER of the pipeline; each step's substance lives in
the skill that owns it. (The session-boundary rituals — init and
end-of-day — live in the private session_init, which always loads.)

## The search ritual

1. **Load the criteria.** This repo's `search-criteria.md` for the
   constraint logic; the private instance's filled version for the actual
   board filters, tier rules, and skip rules; `profile.yml` for the hard
   constraints (floor, location, travel).
2. **Sweep boards in the private file's priority order.** Collect
   candidates without evaluating deeply yet — sweep and vet are different
   modes, and mixing them makes both worse.
3. **Tracker check per candidate** (application-tracking skill): prior
   activity at the organization, duplicates, answers already given.
4. **Vet against hard constraints first** — location, travel, comp floor —
   then lane-route it (resume-lane-strategy) and make the honest gap read.
   Add the one-line ownership/stability note (employer-risk methodology).
5. **Log every vetted role**, including the noes: `researching` or
   `skipped` with the fit note, so the judgment is on record and the role
   is never re-evaluated from scratch.
6. **Decide timing now, not later.** Same-day application matters on
   boards that badge early applicants; a role worth applying to is worth
   applying to today or deliberately queuing with a reason.

## The apply ritual

1. **Re-check the tracker and the posting** — still open, not already
   applied, no contradiction with answers given elsewhere.
2. **Lane → resume** (resume-lane-strategy), and **verify what the ATS
   actually attached**. Platforms cache stale resumes and auto-attach
   them; the stored file on the platform is a second copy of the resume
   and it drifts. Check it every time.
3. **Cover letter triage** (its own skill); if writing, the private
   styles file chooses the approach and the human-writing gate runs before
   anything is final.
4. **Forms from the canonical config.** Every standing answer — work
   authorization, sponsorship, comp, EEO policy, reasons for leaving —
   comes from `profile.yml`, not memory. Knockout questions get true
   answers; transferability arguments live in freeform fields and
   conversations, never in inflated dropdowns.
5. **Check the instance's platform notes** for the ATS in play (autofill
   quirks, fields that silently drop, dashboards to confirm submission).
6. **Submit, then log the row immediately** with `source`, `lane`,
   `resume_version`, and notes capturing anything unrecoverable later: req
   IDs, unusual questions and the answers given.
7. **If a warm contact touches this company**, the sequencing rules in the
   warm-outreach skill apply — apply first, then message, and close the
   loop with anyone who helped.
8. **Views regenerate at close**; don't hand-edit the history file.
