# Skill: Board — State workforce boards (Geographic Solutions "Virtual OneStop")

**Load when:** sweeping a state workforce board (Geographic Solutions 'Virtual OneStop').

**Overlay:** if the instance has `skills/boards/state-workforce.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/state-workforce.md`), not by routing. Mechanics of this platform only.

---

## Capability — as of never probed

| | |
|---|---|
| listing page | **not probed** |
| individual JD | **not probed** |

No fetch capability on record either way. **Probe once at the start of the next sweep of this surface and write the result here with the date** — an absent row is not evidence that a browser is needed.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

Most US state workforce boards run on this one platform (first evaluated 2026-08-19 on one state's board — the mechanics below are the PLATFORM's, so they should transfer to other states). **Tier: two stars — a metro-local channel only, never a remote one, and monthly at most.** Dated per-metro inventory, comp observations and verdicts belong in a per-metro analysis note, not in this skill.

Why remote fails on these boards: the statewide remote pool is tiny and staffing-spam-dominated. Measured on one state: 76 de-duplicated remote software listings statewide, **25 of them one firm's evergreen entry-level postings**, up to 71 weeks old.

**Guest search is fully open — no account needed, and don't create one.** Entry `.../vosnet/Default.aspx`. Every filter, facet and sort works as a guest; only Apply is gated (its handler is `ConfirmRegistration()`), so assume applying forces registration. Reading any JD does not. **Because the board is a mirror, the right move is always to take the detail page's `Job #:` — the employer's own ATS req ID — and apply on the employer's site instead.**

**Set three things before reading a single card, every time:**
1. `Job De-Duplication:` -> **Enabled**. Defaults OFF and pads counts ~30%.
2. `Sorted by:` -> **Post Date - Most recent first**. Fresh at top, but the tail runs past a year old, and relevance sort blends them.
3. `Work Site Options` -> uncheck **Onsite** to isolate remote.

## Mechanics

- URLs are half-linkable — keyword+location encode into one opaque encrypted `enc` blob, but **filters never enter the URL**, so a saved link replays the query and silently loses every filter. Not hand-constructible.
- Detail pages (`.../vosnet/jobbanks/jobdetails.aspx?enc=...`) are server-rendered and **plain-fetchable, session-independent**. The LIST page is a JS shell with zero cards (they arrive from `POST /vosnet/Handlers/jobsearch.ashx`). **NOT YET VERIFIED outside a browser:** the container proxy 403s the domain, so this came from an in-page cookieless fetch. Confirm with a real request before building a fetch pipeline.
- Page size forces from 10 to 50 via the page's `CardList` object (`pageLen(50)`) — 5x less pagination. It throws a mustache `drawPager` error when called; the 50/page setting still sticks on the next refetch (confirmed 8/21).
- **Browser BACK from a detail page silently CLEARS the Work Site filter** (de-duplication and sort survive) — measured 8/21. Standing pattern: collect the detail URLs from the list first (stash them, e.g. sessionStorage), then walk the details without ever returning to the list page.
- `enc=` detail URLs are session-encoded tokens — they don't survive as durable references. **Job # + employer is the durable identifier**; re-find via keyword search when needed.
- **No years-of-experience filter at all, and Salary tops out at a six-figure bracket (100K+)** — a higher floor cannot be filtered for. Comp screening is manual on these boards.
- **Provenance labelling is the platform's one real edge over commercial boards.** Every card names its source as `<Category> - <Name>` (Corporate, Recruiter, National Labor Exchange, Private Job Board, Job Distributor, Preferred Employer, Government, ...) and there is a `Source` facet. A recruiter posting renders the employer as **"Not Available"** — the hidden-employer case. ~24% of listings carry a posted employer wage, better than Indeed or LinkedIn.

## Four traps, all measured

- Result counts are **O*NET occupation-expanded, not keyword matches** (3,365 for a plain `software engineer` query statewide on one state). Never quote them as posting counts.
- **The Occupation facet is broken** by mis-mapping — a principal software engineer classified "Instructional Coordinators", a lead Java engineer as "Chief Executives". Don't filter on it.
- **Facet counts disagree with filtered results** — Work Site said 72 remote, filtering returned 81 (76 de-duped). Facets compute against the base query.
- The detail page's **"Position range in <MSA>" box is an imputed BLS regional estimate, NOT employer comp** — easy and costly to misread. And the worksite field is employer-entered and sometimes flatly wrong (a "- REMOTE" title flagged Onsite), so the remote filter under-counts; supplement with a keyword sweep for "remote".

**H-1B/PERM prevailing-wage notices are a distinct noise class here**, more visible than on commercial boards: plain title, a precise odd annual figure (cents on the amount), sometimes a `***` title suffix or "[Multiple Positions Available]", and a deliberately minimal years bar. They read as well-paid senior roles and are not.

## Added 2026-08-31 after the first complete sweep of this platform

(100% of a statewide-remote pass, 100% of a 379-row metro pass, plus a skill-keyword pass.)

- **A title query and a skill-keyword query are NOT redundant on this platform** — a distinct claim from `software engineer` vs `software developer`, which remain 85-90% redundant. A skill-keyword statewide-remote query surfaced two employer VP-level reqs the title-scoped search missed entirely, one of them the best-fit find of the sweep. **Run a skill-keyword pass, not only title passes.**
- **A fresh search from the top search bar silently RESETS the sort to Relevance**, while de-duplication survives. Re-apply the sort after every new search.
- **The Work Site filter fails in a second way:** the filter-div redraw triggered by changing de-duplication or sort resets BOTH worksite boxes to unchecked, which is no filter rather than the intended one. Reliable order: set de-duplication and sort first, let them settle, then **set Remote positively** instead of unchecking Onsite, and verify the checkbox state via `filterContent`.
- **The Employer facet is broken exactly like the Occupation facet.** Four selected employers returned `recordsFiltered: 5` and rendered zero rows, and its value list is corrupted (one entry was literally `"Software Engineer (Remote)<employer name>"`). Never filter on Employer. Employer-name keyword search through the top bar works and bypasses the occupation modal.
- **Salary UNIT fields are unreliable, not just the BLS "Position range" box.** One req rendered a range "Per Biweekly" while its body gave the same figures as an annual range — a naive read inflates it 26x. Always reconcile the displayed range against the description body.
- **Headline counts contradict the rendered set even after facets apply** ("69 jobs" vs 58 rendered vs a facet reading "(58) Remote"). Trust the rendered row count.
- **Best access pattern found: `fetch()` the detail pages from inside the list page and parse with `DOMParser`.** It never navigates, so the BACK-clears-worksite trap cannot fire, and it pulled 27 detail pages cheaply. Target `divCompensationHours` and never touch `divCOLDet` / `divPnlCOL`, which structurally guarantees no BLS estimate is mistaken for employer comp. Coordinate clicking is unreliable (the page re-renders between screenshot and click) and the renderer froze on roughly a third of screenshot calls.
- `pageLen(100)` works but silently renders ZERO cards after some facet changes; recover with `pageLen(50)` then `page(1)`.
- **A "Remote" work-site tag on this platform is a HYPOTHESIS, not a fact — CONFIRM ON THE EMPLOYER'S OWN POSTING before logging a role as remote or spending any effort on it.** Measured 2026-08-31: **six of six** "remote" finds, pulled from the employers' own careers sites, were all HYBRID (stated in-office days per week; in one case the primary location was a different STATE than the board showed). The earlier note that the worksite field "under-counts" was the less dangerous half: **it over-reports too, and over-reporting manufactures a remote pipeline that does not exist.** Comp, by contrast, matched the employer postings exactly on all six, which is what makes the cards feel trustworthy.
- Corollary, and the reason for the tier line above: a full sweep of one state's board on 2026-08-31 produced **zero verified remote roles.** Sweep these boards for metro-local inventory or not at all.

## Keyword breadth runs the other way here

The "10+ years behind a plain title" pattern that justifies broad keywords on LinkedIn is real but RARE on these boards — one clean instance in ~35 JDs read, and it was clearance-gated. Stated years track title seniority tightly, because both dominant plain-title noise classes (H-1B notices, recruiter req mills) state deliberately minimal experience floors and so structurally cannot hide a 10-year requirement. **The LinkedIn finding is NOT contradicted** — it was measured on a comp-filtered national pool where a plain-titled senior role was invisible to every title-scoped search, and still governs there. Also: `software engineer` and `software developer` are 85-90% redundant on these boards. Run one, not both.
