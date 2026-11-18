# Skill: Board — Eightfold-powered company boards

**Load when:** sweeping an Eightfold-powered company careers board — any employer
whose careers site runs Eightfold (classic) or Eightfold PCSX.

**Overlay:** if the instance has `skills/boards/eightfold.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

**Addressed BY NAME** (`skills/boards/eightfold.md`), not by routing. This file carries only what is specific to this surface.

---

## Capability — as of 2026-10-12

| | |
|---|---|
| listing page | **FETCHES, anonymously** (verified on a PCSX board, 2026-10-12) |
| individual JD | **FETCHES, anonymously**, full HTML in the response |

**TWO API GENERATIONS LIVE ON THIS PLATFORM. Try both before concluding a board
is closed.**

| | endpoint | verified |
|---|---|---|
| classic | `/api/apply/v2/jobs?domain=<domain>&start=<n>&num=10&query=<q>&location=` | 2026-09-10 |
| **PCSX** | `/api/pcsx/search?domain=<domain>&query=<q>&start=<n>` | **2026-10-12** |
| PCSX detail | `/api/pcsx/position_details?position_id=<id>&domain=<domain>&hl=en` | 2026-10-12 |

**`domain=` IS MANDATORY ON BOTH, AND OMITTING IT RETURNS 403, NOT AN ERROR
MESSAGE.** A probe that hit the classic endpoint with `q=` instead of
`query=` and no `domain=` read the 403 as "the board blocks anonymous access"
and wrongly concluded the surface needed a browser. **It did not. A 403 here means a malformed request far more often than a
block** — re-send with `domain=` before drawing any conclusion.

**PCSX field names, which differ from the classic shape:** the employer's own
requisition number is **`displayJobId`** (this is the number a referral
conversation needs, not the internal `position_id`), and the full JD HTML is in
**`jobDescription`**. Filters are `filter_<name>=`.

**Rate limiting is real on PCSX.** A burst of detail calls returned
`429 "Please try again later"`. **~2.5s spacing with backoff ran clean.**
Search pages are 10 rows on both generations.

**A company on this platform may run an INTERNAL hub on a separate host that
you can never reach.** One employer's internal career hub redirected to its
corporate employee tenant; the public board was on a different host. **Do not
conclude a platform is closed from the internal host's sign-in wall** — find the
public one.

**Probe once at the start of each SWEEP and update this block with the date** —
an absent row is not evidence that a browser is needed, and this block is the
standing proof of that.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## The site's own "Remote" filter is not the remote signal

On this platform the board's remote facet and remote fields can hide most of the
remote inventory. PCSX boards expose `filter_include_remote` and
`filter_work_site`; the same caution applies. The pattern that worked on a PCSX
sweep was to **not filter on either**, narrow by `profession`, and then grep the
JD text for the remote language.

Measured on one classic-API board, the facet and the field were wrong in opposite
directions:

- The "Remote, <country>" location facet returned only a small fraction of the
  remote reqs, all in one org.
- The `work_location_option` field said **`onsite`** for a req whose own location
  list included `<country> - Remote`, and `remote_local` for reqs whose only
  locations were hub cities.
- The **reliable signal was the `locations` array containing the literal string
  `<country> - Remote`.** On that test the location-string filter found many times more remote reqs
  than the facet, most of them in engineering or data roles.

So: never conclude "this company has few remote roles" from an Eightfold remote
facet. Enumerate and filter on the location strings instead.

## How to enumerate

The board is a JS SPA, but its JSON API is directly fetchable from a tab already
on the domain, which sidesteps pagination-by-clicking entirely.

```
/api/apply/v2/jobs?domain=<domain>&start=<n>&num=10&query=<q>&location=&sort_by=relevance
```

- **`num` is capped at 10 regardless of what you pass.** Page with `start`.
- **An EMPTY `query` does not mean "everything"** — it falls back to a
  personalized/location-scoped set (a handful of results). Use a
  stopword like `query=a` or `query=the` to get the true board total; both
  return the whole board as match rows, deduping to fewer unique reqs (the
  surplus is locale duplicates).
- **Always pass `location=` explicitly to clear it.** Omitting it lets the
  session's saved location filter leak into the API call, which is what
  produced misleading small-result reads.
- **Comp is not a field.** It lives in the `job_description` HTML on the
  per-job endpoint `/api/apply/v2/jobs/<numeric id>?domain=<domain>&isPcs=true`.
  Strip tags and regex for a currency amount of five or more digits.
- **Read the remote sentence, not just the tag.** A JD that says candidates may
  work "from anywhere in the country" is genuine national remote with no state
  roster and no hub requirement.
- **Watch for the geo-comp caveat.** A JD line such as "This compensation range
  will vary based on location" means a posted top-of-band is a high-cost-metro
  number, not a number for every location. Treat the band as clearing a floor,
  never as a predicted offer.
