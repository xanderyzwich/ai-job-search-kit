# Skill: Board — Indeed

**Load when:** sweeping Indeed.

**Overlay:** if the instance has `skills/boards/indeed.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/indeed.md`), not by routing. Mechanics of this one surface only.

---

## Capability — as of never probed

| | |
|---|---|
| listing page | **not probed** |
| individual JD | **not probed** |

No fetch capability on record either way. **Probe once at the start of the next sweep of this surface and write the result here with the date** — an absent row is not evidence that a browser is needed.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## URL pattern

```
https://www.indeed.com/jobs?q=<title+words>&l=Remote&fromage=7&sort=date
```

`l=Remote` + `fromage=7` (last 7 days) + `sort=date` gives a remote, recent, date-sorted view.

## Query behaviour

Qualifying the title with a seniority word returned essentially the same recycled pool as the bare title on the same day — the qualifier narrows the net without improving signal. Noise is medium-to-high either way; screen on comp and domain by hand rather than trying to filter it out via title wording.
