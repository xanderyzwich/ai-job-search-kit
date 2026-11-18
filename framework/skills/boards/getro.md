# Skill: Board — Getro (PE / VC portfolio job boards)

**Load when:** sweeping any PE or VC portfolio job board on the Getro platform
(vanity domains whose pages carry a `__NEXT_DATA__` payload and an
`api.getro.com` backend).

**Overlay:** if the instance has `skills/boards/getro.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME. Shared sweep rules live in the board-strategy skill, if the instance has one.

---

## No browser is needed: Getro has a plain JSON API (proven 2026-11-09)

Browser-era notes about Getro ("Load more" capping at ~40 cards, stale SPA
renders, JS tool refusing output) describe the FRONT END only. The JSON API
underneath answers anonymously.

```
POST https://api.getro.com/api/v2/collections/<network_id>/search/jobs
Content-Type: application/json
Accept: application/json          <-- OMIT THIS AND YOU GET 406 WITH AN EMPTY BODY
Origin: https://<the board's domain>

{"page": 1}
```

**A 406 means the Accept header is missing, NOT that the endpoint is wrong.** A
404 means the collection id is wrong. The two are easy to confuse.

### Getting the `network_id`

It is in the board page's own Next.js payload — no guessing:

```bash
curl -sS <board-url>/jobs | python3 -c "
import sys,re,json
d=json.loads(re.search(r'<script id=\"__NEXT_DATA__\"[^>]*>(.*?)</script>',sys.stdin.read(),re.S).group(1))
print(d['props']['pageProps']['network']['id'])"
```

### Pagination and filters — measured, not assumed

- **20 jobs per page, hard.** `per_page`, `size` and `limit` are all accepted
  and all **silently ignored**. `page` works. A board of ~1,600 jobs = ~81 requests.
- **`{"query": "<text>"}` works** and narrows the count. **`{"filters":{"q":…}}`
  does NOT** — it returns the unfiltered count and looks like it worked.
- **`{"filters":{"seniority":["director"]}}` works.**
- **`{"filters":{"work_mode":["remote"]}}` works.**
- Response is `{"results":{"jobs":[…],"count":N}}`.

**A full pull of ~1,600 returned ~1,585 unique ids** — about 1.3% lost to churn
between page requests. **Expect a small shortfall; do not read it as an error,
and do not read the count as exact.**

## What the records carry

Each job object has: `title` · **`seniority`** · **`work_mode`** ·
`compensation_amount_min_cents` / `_max_cents` / `_period` / `_offers_equity` ·
`locations` · `searchable_locations` · `skills` · `url` · and
**`organization.head_count`**, `organization.stage`, `organization.name`.

**Compensation is structured and only about a third of rows have it** (547 of
1,585 on one board carried real cents). **`compensation_public` was TRUE on every
row and means nothing**; read the cents field, not the flag.

### Two fields that look authoritative and are not

1. **`organization.head_count` is a coarse bucket, not a number.** Only values
   2-6 appeared across a whole board. Roughly ascending with size, but at least
   one large, well-known company sat in the smallest bucket, which is wrong by
   any reading. **Use it to rank candidates for a closer look; never use it as an
   org-size gate on its own.**
2. **`seniority` can disagree with the JD.** A "Manager, Software Engineering"
   req was tagged `director` while its JD asked for three years managing a
   development team — a first-line role. **Treat `seniority` as a hint for
   bucketing, never as the lane decision.**

## Method: pull the whole board and classify locally

**Do not sweep by title query.** A title query bakes the lane into the fetch, so
a sweep run under one lane strategy can never find roles of another lane later —
they were never fetched. Measured on ONE board: a title-query sweep logged one
manager-shaped row; the full pull found nine, three of them US-remote with
published bands.

**A whole-board pull costs ~81 requests and about a minute.** There is no reason
to pre-filter by title.

**Also avoid the `work_mode: remote` filter for recall.** Some employers' jobs
carry no remote tag at all (one employer's 87 jobs had none), so a remote filter
silently drops all of them. Pull everything, classify locally, and the filter
costs nothing.

### What the pull does not solve

Classifying a complete pull by title is still classifying by title. Where the
real filter is org shape rather than title, a small engineering org may give the
same job any of several titles, and a title pass will miss them. That needs a
company-first pass: select small orgs on `organization` data and independent
headcount, then read every leadership req regardless of title. `head_count` is
too coarse to drive that by itself.

## Front-end notes (only if the API is unavailable)

- Typing into the search box and pressing Return sometimes silently no-ops within
  an already-hydrated session; a fresh full-page navigation to a constructed URL
  is reliable. State lives in the URL as `?filter=<base64 JSON>&q=<query>`; the
  location filter blob decodes to `{"searchable_location_option":["remote"]}` and
  is reusable across Getro boards. Obtain it once from the UI dropdown, then swap
  only `q=`.
- "Load more" hard-caps around 40 cards, so any query returning far more is
  under-swept; matching is fuzzy (3-word queries degrade to loose OR, some 2-word
  phrases AND-match to zero). **A zero on a Getro board is not evidence of
  absence**; single words catch reqs phrase queries miss.
- Stale-render trap: after a JS-tool call a fresh navigation can update the tab
  URL while the SPA does not re-render, so page text returns the PREVIOUS query's
  results. Cross-check the URL the page-text tool echoes against the tab URL
  every time and reload if they disagree.
