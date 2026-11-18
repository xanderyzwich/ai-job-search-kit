# Skill: Board — Wellfound

**Load when:** sweeping Wellfound.

**Overlay:** if the instance has `skills/boards/wellfound.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/wellfound.md`), not by routing. Mechanics of this one surface only.

---

## Capability — as of never probed

| | |
|---|---|
| listing page | **not probed** |
| individual JD | **not probed** |

No fetch capability on record either way. **Probe once at the start of the next sweep of this surface and write the result here with the date** — an absent row is not evidence that a browser is needed.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## URL shape and filters

```
https://wellfound.com/jobs?role=<role-slug>&remote=true&jobType=full-time&salaryMin=<N>
```

- Requires login.
- **There is no "Individual Contributor" job-type filter in the current UI** (Job Types are only Full Time / Contract / Internship / Cofounder). Search by title in the role box and read the JD; the "Required experience" min-years slider under Filters is the closest available proxy for seniority.

## Query behaviour

**Query style is the opposite of LinkedIn's.** An exact quoted phrase (for example `"Staff Software Engineer"`) works and returns a manageable, relevant pool. The bare phrase without the qualifier word and without quotes returns a *different and non-overlapping* set the exact phrase misses entirely. Run both per session; they are complementary, not redundant.

## UI quirks

- Once a job's "Learn more" panel is open, "Apply on website" reliably opens the real external application in a new tab (usually Greenhouse, or the company's own careers page proxying Greenhouse).
- Clicking a second listing's "Learn more" while a modal is already open silently no-ops. Close the open modal first, every time.

## "Featured" status

A free, opt-in Wellfound program, not a paid upsell: once a profile is accepted, startups can message the candidate directly for up to 4 weeks without an application; it auto-expires, is renewable anytime and can be opted out of in profile settings. While featured, the primary-role field locks and can't be changed without contacting support. Because outreach becomes profile-driven rather than resume-driven during this window, the profile's own description text and "Open to roles" tags carry more weight than usual — check periodically that they are not left generic for the duration.

## What the board is good for

Strong for funded startups; shows salary/equity upfront; gives direct founder/hiring-manager access. Series A-C is the sweet spot.
