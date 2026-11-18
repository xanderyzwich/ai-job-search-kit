# Skill: Board — PE / Growth-Equity Portfolio Boards

**Load when:** sweeping a PE or growth-equity portfolio job board (Getro- or
Consider-hosted, or a custom page). Getro API mechanics are in `getro.md`.

**Overlay:** if the instance has `skills/boards/pe-portfolio.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME. Shared sweep rules live in the board-strategy skill, if the instance has one. This file carries only the mechanics of the surface.

---

## Capability — as of never probed

| | |
|---|---|
| listing page | **not probed** |
| individual JD | **not probed** |

No fetch capability on record either way. **Probe once at the start of the next
sweep of this surface and write the result here with the date** — an absent row
is not evidence that a browser is needed.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## What counts as a board

Consolidated job boards run by PE/growth-equity firms across their portfolio
companies. A firm either has a real live board or it doesn't. These do NOT count:
a generic corporate "careers" page for the firm's OWN hiring; a plain
portfolio-company DIRECTORY (logos/links, no jobs aggregation); a board scoped to
internships or gated behind account signup. Several well-known firms with strong
software portfolios have no aggregator at all.

Per-board counters (total jobs seen, relevant found) and the stack rank change
every sweep and belong in the instance's tracker file, not here.

## Platforms

Most boards are one of: **Getro** (see `getro.md`), **Consider**, or a custom
page (for example a shared-engineering-arm WordPress listing). Vanity domains can
redirect to the platform URL and fail to fetch directly; use the platform URL
(`consider.com/boards/vc/<firm>/jobs`).

## Methodology limit

Every Getro/Consider board front end is a JS-rendered SPA. Search-engine-indexed
job-detail pages fetch fine individually, but a board's own search/filter UI does
not respond to fetch — so a "no matches found" from a fetch/search-index sweep is
NOT proof a board has nothing; it means that method couldn't see it. Prefer the
JSON API where one exists (Getro's, or a board's own search endpoint), otherwise
a live browser session driving the board's own filters. Some Consider boards are
fully client-rendered and resist keyword filtering even in a browser; there,
read the unfiltered company-grouped listing (each company shows a few sample
postings plus a "N matching jobs" count) and try the facet's dropdown-select
behaviour (it may require picking a suggested option rather than free-typing)
before falling back to manual scroll.

## Live-browser sweep method (settled 2026-08-31)

- **Consider boards:** the query lives in the URL as `?titlePrefix=<terms>` and
  survives navigation — no clicking, no typing. Confirm it applied by the
  "Title: … / Clear filters" chip and the corrected count. It matches at **any
  word boundary in the title**, so it is effectively a substring query and
  **single words strictly beat phrases** ("Platform Engineer" → nothing;
  "Platform" → "Platforms Engineer"). **For any company showing more than 3
  matches, use `/jobs/<company-slug>?titlePrefix=X`** — the per-company form
  returns that company's matches ungrouped and complete, bypassing the grouped
  view's 3-samples cap. Slugs come from the "All jobs at X" href. Never use the
  ROLES facet (predefined skill tags only; it silently returns "no matches found"
  for a free-typed title). `?q=` and `?filter=<base64>` are Getro params and get
  silently stripped on Consider.
- **Getro boards (front end):** fresh full-page `navigate` per query to
  `?filter=<base64 JSON>&q=<query>`. Typing into the search box and pressing
  Return sometimes silently no-ops in an already-hydrated session. The location
  filter blob `{"searchable_location_option":["remote"]}` (base64
  `eyJzZWFyY2hhYmxlX2xvY2F0aW9uX29wdGlvbiI6WyJyZW1vdGUiXX0%3D`) was confirmed
  reusable across every Getro board tested. Verify: the dropdown label flips to
  "Remote" and the count drops.
- **Two recall limits that must be recorded, never reported as "empty":**
  (1) Getro's "Load more" hard-caps around **40 cards** and then vanishes, so a
  query returning far more than 40 is **under-swept**; (2) Getro's matching is
  fuzzy and inconsistent — 3-word generic queries degrade into loose OR sorted by
  recency, while some 2-word phrases AND-match to zero. **A zero on a Getro board
  is not evidence of absence.** Single words caught reqs phrase queries missed.
- **Stale-render trap.** After a `javascript_tool` call, a fresh `navigate` can
  update the tab URL while the SPA does not re-render — `get_page_text` then
  returns the PREVIOUS query's results. `get_page_text` echoes the URL it
  actually read: **cross-check it against the tab URL every time, and
  `location.reload()` if they disagree.**
- **Comp trap, the most dangerous thing on these boards.** On Consider,
  **"Salary range USD X - Y" is employer-posted; "Similar jobs pay USD X - Y" is a
  Consider market estimate with no employer basis.** Via a Consider board's API
  the same distinction is `salary.isOriginal` true/false. Estimates are not even
  directionally reliable (one showed a range well off the employer's own posted
  band). Tier an estimate as **Unknown**, never as a posted range.
- **Read zone banding, not the headline top.** Aggregator and employer-site bands
  can differ materially at the top; some employers disclose only statutory
  states, so an out-of-those-states offer is **unbanded**; some publish
  deliberately wide "national" bands that geo-adjust downward; a lowest "all
  other US" zone is what most locations get.
- **A "Remote" card is not a remote req, and a non-remote card is not a
  non-remote req.** Workday slugs leak the real tag (`Remote-<City>`,
  `<City>-HQ`) even when the card says "United States." In the other direction,
  some employers' cards carry no Remote tag at all, so a remote-filtered sweep
  silently drops all their jobs — the remote filter is a recall tradeoff, not
  free. Hub-city residence requirements (hybrid-style "flexible" policies) can hide behind a
  "Remote" card; verify before applying.
- **Some Consider boards expose their own API that allows COMPLETE
  enumeration** — `POST /api-boards/search-jobs` with an `x-csrf-token` scraped
  from the inline `"csrfToken"` in `document.scripts`; `grouped:false`,
  `size:200`, cursor paging pulled a whole board in about one request per 200
  jobs with salary objects attached. When a board offers this, filter locally instead
  of guessing keywords.
- **Reader quirks:** iCIMS serves the req inside an iframe
  (`document.body.innerText` came back at 116 chars) — read
  `document.querySelector('iframe').contentDocument.body.innerText`, or fetch the
  Getro sibling listing, which carried the full req; and `javascript_tool` refuses
  output containing query-string-looking text ("[BLOCKED: Cookie/query string
  data]"), firing on the code text as well as page text, so strip `?…` from URLs
  and page results in ~500-char slices.
- **Session flakiness:** screenshots occasionally time out ("renderer may be
  frozen") mid-session; closing the tab and opening a fresh one in the same tab
  group resolved it each time.
- **Cadence:** three days is too short for the small boards (measured on one
  run: a small board swept three days earlier produced no new rows while the
  large boards did). Re-sweep small boards weekly at most; large ones reward returning sooner
  because they have never been fully swept. Aggregator listings can read closed
  while the employer reposts similar reqs under new ids; check the employer's own
  careers page.
