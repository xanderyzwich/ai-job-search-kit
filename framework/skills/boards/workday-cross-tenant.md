# Skill: Board — Workday cross-tenant search and tenant CXS API

**Load when:** running a company-independent Workday search, or reading and
sweeping any Workday tenant's listings (`*.myworkdayjobs.com`).

**Overlay:** if the instance has `skills/boards/workday-cross-tenant.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

**Addressed BY NAME** (`skills/boards/workday-cross-tenant.md`), not by routing. Browser mechanics live in `search-apply-ritual.md`.

---

## Capability — as of 2026-11-17

| | |
|---|---|
| listing page | **text OK** — 20 jobs with location, type, date, req ID |
| individual JD | **fetches** — tenant CXS per-job GET (2026-11-17, verified on a tenant) |
| application form | **not readable anonymously** — Apply sits behind a per-tenant account |

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## Cross-tenant search (confirmed 2026-10-05)

Workday has no global job search, but a Google x-ray covers every tenant at
once: `site:myworkdayjobs.com "Fully Remote" "<title or stack term>"` with
`&tbs=qdr:w` (past week). "Fully Remote" is Workday's own remote-type label, so
it filters well. Google returns 10 per query; run several terms. **Run it in the
browser (google.com), not a WebSearch tool, which ignores `site:`.** Then read
each JD from the tenant's own JSON API instead of the JS-rendered page.

## The tenant CXS API works without a browser (verified 2026-11-17)

- **Search:** `POST https://<host>/wday/cxs/<tenant>/<site>/jobs` with JSON body
  `{"appliedFacets":{},"limit":20,"offset":0,"searchText":"<terms>"}`. Page by
  `offset`; page size is 20.
- **Read one job:** `GET https://<host>/wday/cxs/<tenant>/<site>/job/<location>/<slug_reqid>`
  (`Accept: application/json`), using the `externalPath` the search returns. If
  fetching from a browser, navigate to the posting first so the call runs from
  that origin.
- **The requisition ID is in the path** (the trailing `_<reqid>` segment), so
  tracker dedup can match on it.
- Read `jobPostingInfo` for title, location, `remoteType`, `postedOn`, and
  `jobDescription` with its pay text.

## What cannot be read without an account

Only the listing and JD side is open. The application form is behind a
per-tenant sign-in (Apple, Google, or email+password, no guest path), so its
fields, required questions and any comp prompts are unreadable and unverifiable
from a sweep. Accounts are per-tenant; a login at one employer's Workday never
carries to another. The Workday form-filling notes are not part of this framework.
