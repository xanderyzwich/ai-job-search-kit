# Skill: ATS — Greenhouse (boards API and embed frontend)

**Load when:** a sweep, harvest or scoring agent reads a Greenhouse board for discovery, JD harvest or req counts (public boards API, embed frontend).
Addressed by name, not by routing. Application filling is retired; the owner applies themselves.

**Overlay:** if the instance has `skills/ats/greenhouse.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

---

## Capability — as of 2026-10-06

| | |
|---|---|
| application form | **text OK** — full JD plus every field label incl. custom questions and EEO, ~11K chars |

`boards-api` JSON **truncates at about 50K chars through a page read — fetch it directly**.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## Boards API — JD harvest path (confirmed 2026-10-02)

When a company wraps its own careers UI around a Greenhouse board (numeric job ids in its own URLs), the JD body often lazy-renders and is invisible to page-text and accessibility-tree reads. Skip the page:
`https://boards-api.greenhouse.io/v1/boards/<token>/jobs/<id>` returns the full JD, including any salary sentence, as plain fetchable content, and `.../jobs?content=true` lists the board. The token is usually the company slug; a 404 means a different token or a different ATS, not that the job is gone. Text-only, no browser needed.

**Token and per-id lookup.** For a company whose careers site proxies Greenhouse, hit `.../boards/<token>/jobs/<gh_jid>`. A full JSON body does NOT prove the req is open (see Liveness below: the per-id API has no status field and returns closed reqs). Find `<token>` from an apply URL's `gh_jid` and by trying company-name variants; the token is not always a guessable variant (one board used `<name>jobs`, another `<name>technologies`, not the bare name). A web search for `"job-boards.greenhouse.io" <company>` surfaces it fast when guessing fails. The full-list endpoint `.../boards/<token>/jobs` returns every req but can exceed the fetch size cap for large employers and truncate (alphabetically) — verify individual reqs by id rather than trusting a truncated list.

**Do not infer the ATS from URL parameters.** A `gh_jid` parameter on an apply link LOOKS like Greenhouse, but one employer's application ran on its own careers portal, not a Greenhouse form (no MyGreenhouse autofill; the forms had no cover-letter field). Open the form.

**Token collision is real and silent.** `boards-api.greenhouse.io/v1/boards/<short>/jobs` can return 200 with a plausible req count for a DIFFERENT company that owns that token. **A 200 with a plausible count is not identity.** Pull 5 sample titles and locations before accepting a guessed token. Two other vendors failed the same way the same day (a SmartRecruiters slug resolved to an unrelated company; a Recruitee subdomain returned a demo board with a req titled "Senior Marketer (Sample)").

**A token can 404 because the company moved ATS**, not because the token is wrong; check Ashby and Lever for the same slug before concluding the board is gone.

## Discovery: the embed frontend is fully browserless (measured 2026-11-06)

**Plain `https://job-boards.greenhouse.io/<token>?keyword=<text>` returns SERVER-RENDERED HTML to a plain fetch** — department and team groupings, job titles, locations, **job ids**, and a count line. **No truncation on any filtered query**, which is the whole problem with `/v1/boards/<token>/jobs` (a large board's full list can be too big to read). A filtered keyword fetch beats both the full-board API and the browser for inventory: no department ids, no pagination walk, no browser lock.

`?page=N` works too and returns a different set, but the unfiltered board came back as plain text with no count line and no visible pagination targets. **Prefer keyword queries over paging.**

**`job-boards.greenhouse.io/<token>` IS NOT UNIVERSAL.** On one employer it returned a client error; on another it 302'd to the employer's own careers domain, a JavaScript shell ("Loading job openings…") unreadable browserless.

**`job-boards.greenhouse.io/embed/job_board?for=<token>` worked on both**, with a count line, department groupings, titles, locations and job ids — and **`&keyword=<text>` works on it too.**

> **Use the embed form by default.** It is the same path used to reach a form behind a branded page, and it is also the robust path for READING a board. The plain `/<token>` URL is the special case, not the rule.

Registry tokens were verified against `boards-api.greenhouse.io`, which is a DIFFERENT HOST from the frontend. An API token working says nothing about whether the plain frontend path resolves. In the measured cases the tokens were correct; only the path was wrong.

**Keyword matching is on CONTENT, not titles** (confirmed on three boards): `?for=<token>&keyword=Java` returned jobs none of whose titles contained "Java". Treat every keyword result as a superset.

**`/departments` truncates on large boards too** — on large boards the response is cut short. **The embed count line is the cheapest reliable total; the API gives only a floor.**

**Browser discovery (earlier finding, superseded for discovery by the keyword fetch above).** On a large employer the board-list API truncates alphabetically, so senior engineering titles (Principal/Senior/Staff/Technical Lead) sort past the cut and never appear; web-search snippets are stale and surface long-closed reqs. A browser on the live careers board returned the full rendered list with no truncation, then filtering by department + location and clicking a role gives its `gh_jid`; on one run this surfaced open reqs the API and search both missed. Division of labour at the time: browser discovers, per-id API verifies/enriches, web search is the no-browser fallback. Also watch for board-vs-API disagreement (a req can be API-open but not listed on the public board — trust the public board for what a referrer actually sees). The browser remains the only liveness check.

## Liveness: the frontend serves closed requisitions (measured 2026-11-06)

**Reqs confirmed closed in a live browser were still returned by browserless keyword searches, and one still served a FULL job description page including its salary band.** The browser, on the same URLs, shows *"The job you are looking for is no longer open."* The two views can also disagree on board totals.

**What this test did not settle:** whether the browserless copy is STALE or whether its search simply MATCHES MORE THAN THE TITLE. The superset behaviour is real — a keyword search returned a role whose title contained neither search word — so differing counts between the two views are explained by matching; only the closed reqs appearing is not. One fetch cannot separate the two.

**The operational rule is the same either way:**

> **SWEEP BROWSERLESS. VERIFY IN THE BROWSER.**
> Keyword-fetch the board for inventory and scoring. Then, immediately before preparing any application, load that req's apply form in the browser. It is the only surface that has been right every time.

**The per-id JSON API is worse than the frontend here** — it returned full objects for closed reqs and **carries no status field at all**, so it cannot express closure even in principle. A full JSON body does not mean the req is open. It can enrich a suggested URL but never confirm the req is open.

**Stale-URL and "removed" calls need a second source.** A tracker-saved apply URL can 404 or silently point at the wrong sibling req (two open reqs with near-identical titles existed side by side; the right one was confirmed only by cross-checking comp and travel language against the scoring notes). An aggregator's "this job was removed" status was checked against the employer's own open-roles listing, searched by keyword and not just browsed, before marking closed. Do not act on a single source for either a stale-URL fix or a closed-job call.

## Forms hidden behind branded pages (read-only relevance: locating the live req)

A careers-site posting can render the full JD with no apply button or form anywhere (confirmed by a full scroll and an `all`-filter accessibility read), or hide the form in an IFRAME so `get_page_text` returns zero fields. Navigating to the plain `job-boards.greenhouse.io/<token>/jobs/<gh_jid>` URL may redirect back to the branded page. The form lives at
`job-boards.greenhouse.io/embed/job_app?for=<token>&token=<gh_jid>` — go straight there rather than concluding the form is broken or missing.

## Location fields lie

- **`location.name` is the employer's own vocabulary, not a remote flag.** Filtering one large board on `location.name` containing "remote" or "united states" returned **zero** reqs; its labels were `Hybrid`, `Distributed`, `In-Office` and a single `Remote` — `Distributed` was its word for remote. **Always histogram `location.name` across the whole board before filtering on it;** a filter written against another employer's vocabulary returns zero and reads exactly like "no matching reqs."
- **`location.name` is work style, not geography.** The real place is in `metadata[]` under **`Job Posting Location`** (a `multi_select` list), alongside **`Career Site Department`**. On one board **those style labels said nothing about country or metro** — most of the Hybrid reqs were not US at all. Filtering on style alone cannot answer "is this open to someone in my city." Read both fields, and prefer `metadata` for geography.
- **The same employer spells one city two ways.** `Austin, US` and `Austin, TX` both appeared, as did `San Francisco, US` and `San Francisco, CA`. A matcher testing only `, US` loses a large share of the board and a state-code matcher loses the rest; either failure looks exactly like a thin board. Match on both forms plus bare state names.
- **`Job Posting Location` is an ARRAY.** Reading it as a string loses every location after the first: `['Austin, US', 'Lisbon, Portugal', 'London, UK', 'New York, NY']` recorded as "Austin" turns a four-city, three-country req into a single-city one, and it propagated into downstream write-ups before being caught. It also breaks comp reasoning (a missing band was wrongly explained by one jurisdiction's pay-transparency exemption when the req also listed another). **Always render the whole list, and never explain a missing band by the first element.**
- **A missing band is not evidence of anything.** On one board, two reqs listing two high-disclosure jurisdictions posted no range at all while others published a full multi-jurisdiction table. Do not infer tier, geography or a disclosure exemption from a band's absence — infer only that the number is not on the posting.
- **A "remote" style still carries a metro list.** The `Distributed` reqs named an **Available Locations** block in the JD body (a list of US metros plus Canada) with no "must reside" sentence anywhere, plus "compensation may be adjusted depending on work location." The structured field is a hint; the geo gate lives in the JD body and must be read there.
- **Check whether hybrid cadence is stated at all.** In a pull of technical JDs from one board, none named a day count (measured on one run). The absence is the finding: cadence cannot be applied from such a posting and is a question for a human, not something to infer.

## Cross-board passes — rules for pulling many tokens at once (learned 2026-11-17)

- **Histogram location per board, never once for all.** Each board's `location.name` vocabulary differs (`Remote - USA`, `Remote United States | <zone>`, `United States - Remote`, bare `Remote`, `Distributed`); one regex written for one board misreads the next. Metadata fields (`Job Posting Location`, region) carry geography where `location.name` carries style.
- **A bare `Remote` or `Remote - Global` names no country.** Hold those reqs in a separate list for a JD-body read; counting them as US-open and dropping them are both wrong.
- **`updated_at` is not a posting date.** A bulk touch can stamp hundreds of reqs on one day, so a recency filter over a board can pass or fail it wholesale. Check the date histogram before using it.
- **Tracker ids from aggregators never match Greenhouse ids.** A Built In or LinkedIn row carries its own id, so id-based dedup finds only rows saved from the employer's own URL. Match on company and title as a second key, and treat a same-title, different-id req as new but flagged, not as a duplicate.
