# Skill: ATS — Rippling (ats.rippling.com)

**Load when:** reading an `ats.rippling.com/<slug>` board for discovery, JD harvest or req counts.
Application filling is retired; the owner applies themselves.

**Overlay:** if the instance has `skills/ats/rippling.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

---

## Capability — as of 2026-11-17

| | |
|---|---|
| listing page | **text OK, no browser** — public JSON board list |
| individual JD | **fetches** — HTML page whose embedded `__NEXT_DATA__` holds the full posting; there is no per-job JSON endpoint |
| liveness | **unverified** — the list shows what is posted, not what accepts applications |
| remote signal | per-location `workplaceType` (`REMOTE` / `HYBRID` / `ONSITE`) on the list |
| pay signal | **body text only** — the structured pay field is empty |

Verified on one tenant.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A capability change is reported, not self-written: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## Board list

```bash
curl -sS "https://ats.rippling.com/api/v2/board/<slug>/jobs?page=0&pageSize=100"
```

Returns `{items[], totalItems, totalPages}`. Each item carries `id` (UUID), `name` (title), `url`, `department.name` and `locations[]` with `name`, `country`, `state` and `workplaceType`. **The default page size is 20**, so a bare call silently returns a fifth of a 100-req board; raise `pageSize` or walk `totalPages`, and compare against `totalItems`.

## Per-job JD

`/api/v2/board/<slug>/jobs/<id>` and a `job-posts` variant both 404. Fetch the HTML page `https://ats.rippling.com/<slug>/jobs/<id>`, read the `<script id="__NEXT_DATA__">` tag, and parse `props.pageProps.apiData.jobPost`:

- `description.company` and `description.role` — HTML bodies; concatenate both.
- `createdOn` — posted date; `department.base_department`, `workLocations`, `employmentType`.
- `payRangeDetails` — present but empty.

The list page HTML also embeds its first 20 items in `__NEXT_DATA__`, which is a fallback if the API path changes.

## Rules

1. **Pay is only in the body.** Search the concatenated description for a "Salary Range" style sentence; an empty structured field is not "no pay posted".
2. **A slug can exist and be empty.** An employer's careers page may link a Rippling slug that returns zero items while the live board is on another ATS. Pull both and compare counts before believing either.
3. **Locations are a list.** A req can carry a state-specific remote location (`Remote (Texas, US)`) beside the general US one. Render the whole list; a state-bound remote role is not open anywhere.
4. **Department names are the employer's own.** Roles with engineering titles can sit under other departments (infosec, quantitative science). Histogram departments before filtering on one.
5. **Slugs are not company names.** Derive the slug from the careers-page link, not by guessing.
