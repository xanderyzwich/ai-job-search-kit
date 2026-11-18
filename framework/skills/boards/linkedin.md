# Skill: Board — LinkedIn (mechanics)

**Load when:** sweeping LinkedIn — classic search filters, the guest JD API, a geo-scoped metro pass, or reading profiles and people search.

**Overlay:** if the instance has `skills/boards/linkedin.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

**Addressed BY NAME** (`skills/boards/linkedin.md`), not by routing. Shared sweep rules live in the board-strategy skill, if the instance has one; this file carries only what is specific to this surface. Which filters, keywords and locations a given search uses come from the instance's profile and private overlay, not from here.

---

> **LINKEDIN HAS NO EMPTY STATE. ITS COUNTS MEASURE NOTHING.**
> Measured 2026-11-03 with pure-nonsense controls on the guest search API.
>
> | query | results | what came back |
> |---|---|---|
> | a nonsense two-word string | **10** | unrelated operator / technician roles |
> | a single repeated-letter string | **10** | unrelated engineering, recruiting, community roles |
> | `accordion tuner` | **10** | music-theory and instrument-technician roles |
>
> **The keyword IS applied** (`accordion tuner` genuinely returns music jobs)
> **but the result set never empties.** Every query fills the page and
> pagination fills more. **A LinkedIn count measures how many pages you
> requested, not inventory.** Never compare two queries by their counts, and
> never report "N results on LinkedIn" as a finding.
>
> This is the same fuzzy-fallback pattern some career sites show (a dead req id
> returns plausible near-misses rather than nothing). **Any board that cannot
> say "no results" cannot be used to measure.** Relevance decays silently down
> the list with nothing marking where it stopped being real.
>
> **What LinkedIn is still good for: the titles at the top.** As a vocabulary
> source it is excellent — a title census can surface a search string carrying
> unique inventory that nobody thought to try.
>
> **A control must share no tokens with the query it controls for.** A control
> built as nonsense-plus-the-real-query contains the real query and produces a
> confident, wrong conclusion. Same defect class as a substring match that
> fires on the wrong word.

---

## Capability — as of 2026-10-06

| | |
|---|---|
| listing page | **TEXT READ FAILS** — the whole-page read grabs the `<article>` and returns only the selected JD; the accessibility read gives ~4 viewport links, titles only, no company |
| individual JD | **guest JD API**, ~2.5s spacing |

Listings need the API or JS, never a text read. Parallel browser fetches 429.

## Capability — PROFILE reads, probed 2026-10-21 (signed in, in-app browser)

**A profile is a different surface from a listing and behaves differently.**
Probed across 43 page loads in one sitting; no authwall, no 429, session held.

| | |
|---|---|
| `/in/<slug>/` text read | **IDENTITY ONLY.** First ~400 chars give name, headline, location, current-company line, mutuals. Below that comes About, then Featured, then the full Activity feed *including other people's reposts in full* — Experience sits past a 12,000-char cut and never lands. |
| `/in/<slug>/details/experience/` | **THE WORK-HISTORY ENDPOINT.** Full list: title, company, employment type, start/end as `Mon YYYY`, computed duration, location. **No "Show all experiences" click required.** |

**Two page loads per person, ~3s apart, no screenshots.** The screenshot cost
that forces agent delegation for listings does NOT apply to profile reads; both
reads return text. Delegation is still worth it on page-text VOLUME alone (the
experience endpoint carries every role's full description), with the agent
returning structured rows rather than pages.

**Known gap: a long history ends in an unexpanded "Load more".** Seen on 2 of
22 profiles (roles older than ~10 years truncated). Clicking it is a page
interaction, not a read — out of scope for a read-only pass; record it as
`partial` rather than silently dropping it.

**`Mon YYYY` is the precision ceiling.** LinkedIn shows no day. Entries can
also carry overlapping or year-only (`2019 - 2021`) ranges; record what the
page says rather than reconciling it.

### Concurrent roles — read the WHOLE page, never a truncated prefix (added 2026-10-22)

**A person can hold several current roles at once, and the first one listed is
not necessarily the relevant one.** Seen repeatedly: a short fractional or
contract role listed first, with the person's own long-running desk or
venture(s) second, past a 700-char read. A single-value `company:` taken from
the top block files the wrong employer.

**THE RULE: do not cap an experience read at a few hundred chars.** Count every
`- Present` entry before writing an employer anywhere. The cheap way, which
returns only what matters instead of the whole verbose page:

```js
const t=document.querySelector('main').innerText.split('\n').map(s=>s.trim()).filter(Boolean);
const o=[];t.forEach((l,i)=>{if(/-\s*Present/.test(l))o.push(t.slice(Math.max(0,i-3),i+1).join(' | '))});o
```

**Two readings that are NOT concurrent employers**, so check before recording:
a **nested promotion** renders as one company header with several dated
sub-roles, each possibly `- Present` (one employer, not two); and **zero**
`- Present` entries is a real finding, meaning between roles, not a failed read.

**Why it matters:** a second concurrent role is usually self-employment,
consulting or fractional work, which says whether someone is a peer, a door, or
a read on pricing. **A title and an employer do not give you practice area**,
and here the page ordering actively points at the wrong one.

### Profile search — a third surface; page text has no hrefs (added 2026-10-22)

To find a profile from a name: `search/results/people/?keywords=<name>&network=["F"]`
for 1st-degree only; drop `network` to reach 2nd/3rd. **The page-text read
returns names, headlines and locations but NOT profile URLs** — pull the hrefs:

```js
[...document.querySelectorAll('a[href*="/in/"]')].map(a=>a.href.split('?')[0]).filter((v,i,a)=>a.indexOf(v)===i)
```

**The first result is the match; later ones are sidebar suggestions** (unrelated
people can fill positions 2-3). **Verify by loading the profile**, and treat a
first-name/legal-name mismatch (nickname vs formal name) as unconfirmed until
the person says otherwise.

**Re-probe once per SWEEP, not per listing**, and update the capability blocks
with the date. A surface's capability is stable within a sweep and not across
months. **A capability change is reported, not self-written**: an agent returns
it as `capability_delta` and a context that knows this repo's standards writes
it here.

---

## Classic search vs "AI-powered" search (verified live 2026-09-08)

LinkedIn showed a banner on `/jobs/search/` results: classic job search is being
gradually retired starting September 2026, with a "Try AI job search" button.
Two experiences coexist:

- **Classic search** (`/jobs/search/?keywords=...` and every `f_*` param below)
  — still fully functional as of 2026-09-08, re-verified 2026-09-10. `f_WT`,
  `f_SB2`, `f_TPR`, `geoId` and `sortBy=DD` all echo into the URL AND render as
  active filter chips, with per-listing salary still shown on cards. "Gradually
  retiring" means re-verify at the start of each sweep, not assume permanent.
- **New "AI-powered" / semantic search**
  (`/jobs/search-results/?origin=SEMANTIC_SEARCH_MODE_FROM_CLASSIC`) — **drops
  the salary/comp filter entirely**, along with the structured
  `f_WT`/`f_SB2`/`f_TPR`/`geoId` params (the URL carries only `keywords`,
  `origin`, `isOnboardingQuery`). Its filter bar: Date posted, ad hoc
  keyword-derived chips, Easy Apply, Experience level, Employment type, Company,
  Under 10 applicants, In my network, Verified — no workplace-type chip, no comp
  chip. Listings did not show salary at all. A user who says "the interface
  changed and salary is gone" has usually landed in (or been defaulted toward)
  this mode, not seen a change to classic search.

**Default to classic search and the `f_*` patterns below** — it is the only one
with a comp filter. Do not follow the "Try AI job search" prompt for sourcing
sweeps.

## Classic search URL pattern and filter parameters

```
https://www.linkedin.com/jobs/search/?keywords=<QUERY>&f_WT=2&f_TPR=<WINDOW>&sortBy=DD
```

- `f_WT=2` — remote (other workplace-type values exist; the guest API ignores it)
- `f_TPR=r3600` last hour · `r86400` last 24h · `r604800` last week · `r2592000` last month
- `f_SB2` — salary floor bucket. Corrected 2026-07-07 by reading the live filter
  panel directly (not inferred from result counts): fixed 20K-dollar steps —
  `1`=40K+ · `2`=60K+ · `3`=80K+ · `4`=100K+ · `5`=120K+ · `6`=140K+ ·
  `7`=160K+ · `8`=180K+ · `9`=200K+ (USD, annual).
  **A bucket exactly at the candidate's floor is too tight and silently drops
  in-scope roles just above it.** Use the bucket one step below the floor
  (`base_salary_floor_usd` in `profile.yml`) as the default, then apply
  `comp_range_rule` by eye per listing; a hit whose range top clears
  `comp_priority_threshold_usd` is a priority candidate.
- `f_E` — experience level: `5`=Director, `6`=Executive (and lower values). See
  below.
- `geoId=<id>` — geography; `103644278` is the United States.
- `f_JIYN=true` — "In your network" (see below).

**`f_SB2` filters on DISCLOSURE, not on comp.** It excludes every role that does
not post a salary. On a national remote search most tech employers disclose, so
it is a reasonable default; where disclosure is uncommon it silently deletes the
market (see metro sweeps).

### Query strategy

- **Filter on comp, use BROAD keywords — the title filter is largely
  redundant.** With a comp bucket set, a broad title search is a superset of the
  narrower seniority-title passes and also catches strong roles hidden under
  generic titles that no title-scoped search shows.
- **Always run the fully bare title term too.** Confirmed 2026-09-08 in a
  same-session test (same remote / comp / window / geo): a two-word qualified
  query returned 328 results; the bare two-word title returned 552; a bare
  sibling title returned 593 — and the bare runs surfaced genuinely new in-scope
  candidates the qualified run never showed. Adding ANY qualifier word excludes
  real candidates. Run the bare passes in addition to (not instead of) any
  topic-qualified pass. Expect heavier noise in bare results (the title word
  matching unrelated trades and specialist roles) — that is the cost of the
  wider net, not a reason to narrow it. (Counts here are page-driven; see the
  no-empty-state warning — the point is which listings appear, not the numbers.)
- **Query style:** short, unquoted, 3–5 word combinations outperform quoted
  exact phrases. Unquoted multi-word strings are scored as keywords, so
  different phrasings return genuinely different pools; quoted phrases collapse
  to a small, generic, repeat-heavy pool.
- **Experience-level filter, lane dependent.** Drop `f_E` for individual-
  contributor searches — it is too restrictive and misses roles labelled at the
  wrong seniority. For management-leaning searches, `f_E=5,6` tags roles by
  LinkedIn's internal seniority classification independent of title text, which
  gives a dramatically cleaner pool than title alone (observed: ~8 relevant vs
  100+ noisy without it) and can surface IC-sounding titles LinkedIn tags as
  Director-equivalent. Caveat: it cannot fix a keyword that is ambiguous across
  domains (a physical-infrastructure role matched a software-sounding keyword
  and the seniority filter) — read every hit's actual domain.
  Pattern: `...&f_WT=2&f_E=5%2C6&f_SB2=<n>&f_TPR=r604800&sortBy=DD`
- **Known low-yield shapes:** keywords that skew to hardware, vendor/consulting
  or infra/sysadmin roles; title+funding-stage combos (no better than the plain
  title); dropping the salary filter on a national remote search (floods with
  underpaid contract roles). LinkedIn is staffing/aggregator-saturated across
  every term — scan for direct employers regardless.

## Browser-automation mechanics (learned 2026-07-09)

- The jobs SPA soft rate-limits after rapid tab navigation (serves a ~1300-char
  shell). Reload once, or slow down.
- JD extraction that works: the same-origin guest endpoint
  `https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/<id>` fetched from
  page JS, tags stripped.
- Search-results lists are virtualized — scrollIntoView each card to render it.
- The safety layer BLOCKS JS results containing broad regex captures or long
  tokens; sanitize to short prose slices (strip URLs and 40+ char strings) or
  fall back to screenshots.
- **Login wall:** non-premium accounts get JD-body-blocked on ~60% of promoted
  listings. Hiring-manager-posted (non-promoted) and Easy Apply listings usually
  load fully; otherwise go to the company careers site directly.

## Network and connection-degree filters (tested 2026-07-07)

**`f_JIYN=true` ("In your network")** is a blended signal: it fires if *either*
a 1st-degree connection works at the company *or* a school alumnus does — not
degree-specific, and cannot be split in the URL. It is not limited to fresh
postings (a hit carried a "Reposted 1 week ago" label). A sanity check with a
tight title + comp + remote combination returned a handful of results all from
the one company with a known contact — a good sign the filter is real. Layer it
onto a normal title sweep as a fast pass.

**Caveat:** a "connections/alumni work here" hit does not always mean a real
internal employee. At a marketplace/gig-model company, the match turned out to
be a platform contractor, which LinkedIn's employer graph counts as "works
there". Check the actual profile before treating a single-connection hit as a
referral path.

**Company-first warm-connection lookup — the more powerful technique.** A job
listing's "People you can reach out to → Show all" opens People Search prefilled
with the company's numeric ID (`currentCompany=["ID"]`). That search takes a
real, independent degree filter: `network=["F"]` 1st only · `["S"]` 2nd only ·
`["O"]` 3rd+ · combine as `["F","S"]`. Grab a company's ID once (via any of its
postings, or its page's employee-count link), then reuse:

```
https://www.linkedin.com/search/results/people/?currentCompany=["ID"]&network=["F","S"]
```

This decouples "is there a warm path in" from "is there a fresh posting right
now" — check the company careers page separately for open reqs.

**Premium "Jobs where you're a top applicant" collection**
(`/jobs/collections/top-applicant/`, Premium-gated), tested 2026-07-07: it
echoes `f_WT`, `f_SB2`, `f_TPR` into the address bar but **silently ignores all
of them** (two controlled tests: an under-floor listing survived a salary floor;
a multi-day-old listing survived a past-hour window; counts and ordering
identical). No filter bar exists — it runs on a separate match-ranking backend.
Treat it as a skim-only discovery feed; its one otherwise-unavailable signal is
"Actively reviewing applicants". Check remote status and comp by eye.

**"Actively hiring" People Search filter (`activelyHiringForJobTitles`) — not
actually Premium-gated.** The gold Premium icon is an upsell nudge, not an
access gate. Controlled comparison: a bare `keywords=recruiter` returned 100+
results across 10 pages; adding `activelyHiringForJobTitles=["-100"]` dropped it
to exactly 2, both current recruiters. Layer it onto the company-first lookup:
`currentCompany=["ID"]&network=["F","S"]&activelyHiringForJobTitles=["-100"]`.
`-100` is the "any job title" code; a specific title appears to need an
autocomplete-selected value from LinkedIn's internal title taxonomy rather than
free text — untested.

## Finding recruiters messageable for free (Open Profile) — tested 2026-07-08

There is no search filter or reliable badge that bulk-identifies recruiters who
can be messaged for free. The small gold "in" badge next to a name does NOT
reliably indicate Open Profile: a confirmed-free recruiter showed no badge, and a
confirmed InMail-credit recruiter also showed none. Badge visibility looks like
an individually controlled privacy setting, so its presence is not guaranteed for
true positives and its absence proves nothing.

**Refinement:** Open Profile is itself a Premium-only feature, and recruiters
are more likely than the general population to have enabled it. A second test
confirmed a badge-bearing recruiter came back "Premium · Free message". Among
recruiters, badge-present is a decent prioritisation signal (check those first),
not a guarantee; badge-absent can still be Free.

**The only reliable check:** open the profile and click **Message** (shown on
nearly all 2nd/3rd-degree profiles once you have InMail credits). The compose
header tells the truth: **"Premium · Free message"** = Open Profile, costs
nothing; **"Premium · Use 1 of N InMail credits"** = draws down the monthly
allowance. **The InMail allowance is account-specific and has been misrecorded
before — verify it live in LinkedIn, never trust a figure written in a skill.**
Spend credits deliberately on strong non-Open-Profile targets; do not hesitate
on confirmed Free ones.

Workflow: run `keywords=<role/recruiter query>&activelyHiringForJobTitles=["-100"]`
(or the company-first variant) to build a shortlist, then open each profile's
Message box one at a time to sort Free vs InMail before drafting outreach. No
way found yet to skip the per-profile check.

## Geo-scoped metro sweeps and the guest API (added 2026-09-10)

Both generalize to any metro.

**1. NEVER comp-gate a metro sweep.** On a metro query, `f_SB2=6` cut 73 results
to 4, and all 4 survivors were staffing agencies quoting hourly rates, because
agencies disclose and direct employers in that metro often do not. `f_SB2`
filters on disclosure, not comp, and disclosure correlates with state
pay-transparency law and with remote-tech hiring. On a national REMOTE search the
bucket default is right; on a metro search it silently deletes the market.
Harvest un-gated, then chase comp per employer.

**2. The guest API beats DOM harvesting for volume, and needs no auth.** The
authenticated results list is virtualized and the scroll-to-render loop is slow
and unreliable (two `Runtime.evaluate` timeouts on a frozen renderer). This
endpoint, fetched from a tab already on `linkedin.com`, returns plain
server-rendered cards:

```
/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=<q>&location=<city, state, country>&distance=25&f_TPR=r2592000&sortBy=DD&start=<n>
```

- **10 cards per call**; page with `start` (0, 10, 20 …). Stop when a page adds
  no new ids.
- Response begins with `<!DOCTYPE html>` followed by bare `<li>` elements.
  **Do not wrap it and hand it to `DOMParser`** — the nested doctype makes the
  parse silently return zero nodes. Split the raw string on
  `data-entity-urn="urn:li:jobPosting:` and regex each chunk.
- Per-chunk classes: `base-search-card__title`, `base-search-card__subtitle`
  (company), `job-search-card__location`, `job-search-card__salary-info`, and
  `<time datetime>` for the post date. **Allow ~1200 chars of lookahead** — the
  company name sits after a ~330-char anchor tag, so a 300-char cap matches the
  title and silently returns empty companies.
- **Limitations:** the guest endpoint does not honor `f_WT`, so workplace type
  is absent and must be read per req; and it returned 151 unique where the
  authenticated UI claimed 73, so treat its count as a superset needing its own
  filtering, not a corrected total.

**3. Re-verify classic search at the start of each sweep** (filters echo back as
live chips) — the announced retirement may take effect without notice.
