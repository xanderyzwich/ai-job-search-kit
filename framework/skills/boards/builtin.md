# Skill: Board — Built In (builtin.com)

**Load when:** sweeping Built In, or reading any Built In card, band, date or apply control.

**Overlay:** if the instance has `skills/boards/builtin.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/builtin.md`), not by routing. This file carries the mechanics of this one surface: how it is read, and the ways its data lies.

---

## Capability — as of 2026-10-06

| | |
|---|---|
| listing page | **text OK** — 25 cards with company, title, salary, location, level |
| individual JD | **fetches** (9/28; corrects an 8/17 'browser-only' entry) |

Highest-volume board and no browser needed at either level. **The 8/17 -> 9/28 reversal is the standing warning**: a stale row forced a browser onto the board that least needed one for six weeks.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## URL and data shape

```
https://builtin.com/jobs/remote/dev-engineering?search=<QUERY>
```

- Comp bands are shown inline on cards, the pool is senior-heavy, staffing-firm noise is low. A logged-in account can save job alerts.
- The listing's `ld+json` is entity-encoded (`ld&#x2B;json`) under `@graph`, an `ItemList` of 25 cards per page. Job pages carry a full `JobPosting` block (`baseSalary`, `datePosted`, `validThrough`, body).
- `currency` lives inside `baseSalary` as `currency`, not `salaryCurrency`. A regex for the wrong key left the field blank on over half of one sweep's records. **A blank currency is a gap, not a USD** — a non-USD band can pass a naive floor check.

## Depth

The board is far deeper than "roughly 8 pages". One broad query returned 1,000+ distinct postings across 40+ pages and had not ended. Eight strings run to exhaustion produced 2,367 distinct postings. Title strings outside the recorded title family (for example `manager`, `lead`) contributed 649 postings on their own.

Marginal yield, however, sits in the tail, not the top: a shallow page 1-2 re-sweep eleven weeks after a full sweep found mostly already-tracked rows (18 of 26 companies). **Dedup before fetching any JD**, or most of the acquisition cost is spent on rows already in the tracker.

## Title vocabulary — measured behaviour of the search

A nonsense-string control returned 0, so the counts below are real; queries were paginated to exhaustion.

- **Built In collapses word order, the comma form and the Sr/Senior abbreviation.** `software engineering manager` = `manager, software engineering` = `manager of software engineering`, and `senior manager software engineering` = `sr manager software engineering` return identical sets. Run one of each collapsed group, never both. `engineer` and `developer` are likewise synonym-mapped.
- Different head nouns do NOT collapse (`engineering manager` vs `software development manager` vs `engineering lead`), and each contributes unique postings. Rank candidate strings by marginal contribution, not by raw count.
- **Never compare a capped query with an exhausted one.** A "two queries cover 92%" claim was produced exactly that way (full-depth against 3-page-capped) and was wrong; re-measured at equal depth the lane was larger and the best supplementary strings had been buried.
- **Count the titles you get back** (a title census). That is how you find strings you did not think to ask for.

## Liveness: `validThrough` is NOT a death signal

A lapsed `validThrough` is consistent with a dead posting but does not imply one. Disproved on 2026-11-11: a batch of roles whose Built In window had lapsed were live on the employers' own boards and accepted applications. `validThrough` is Built In's own listing lifecycle; employers keep reqs open past it. Closing a backlog on a lapsed window alone was an error and had to be reopened.

- The removal banner *"Sorry, this job was removed at ..."* is Built In dropping the listing — a stronger signal, but still Built In's state, not the employer's.
- **The only authority is the employer's own application system.** HTTP status and page size are worthless.
- Headless employer-board check: Greenhouse `boards-api.greenhouse.io/v1/boards/<token>/jobs`, Ashby `api.ashbyhq.com/posting-api/job-board/<slug>`; match the req by TITLE. Built In pages expose no external apply link without a browser.
- **Treat the Greenhouse API as an accelerator, not a dependency** (2026-10-14): it worked from a browser session on one run and returned `CONNECT 403` from the egress proxy on the next. When blocked, read the employer's rendered posting and say which source the answer came from.
- Greenhouse returns live reqs with req ids, `first_published` and real `application_deadline` values in one unauthenticated request, which also settles the post-date question this board is unreliable about.

## Six ways a fetch lies — one root cause

**Never accept a response on its status, its size, an exact string match, or an empty parse. Validate on STRUCTURE.**

1. **An empty parse ended pagination.** Rate limiting after ~350 requests returned empty pages, the loop read that as end-of-results, and 437 postings were silently dropped (queries reported 0 when a direct probe returned 25). **An empty result must be RETRIED, never terminal.** Stop on 3 consecutive all-duplicate pages, not 1.
2. **`len(response) > 5000` as the validity test.** Degraded pages pass it; 41% of 474 "no band" records were wrong (195 recovered on a clean re-fetch). Accept a JD page only if it carries a `JobPosting` block or the removal banner.
3. **A missing `validThrough` read as "removed".** 23 of 104 such rows had a live-window page. Same cause as 2: a degraded page parses as a page with nothing in it.
4. **The company regex missed 42%** (310 of 742 records had `company: None`). Take the company from the JD body when the structured field is empty; never write a tracker row without one.
5. **Bodies cut at 9,000 characters — the footer is where the restrictions live.** One employer's state-exclusion list sits **below the Apply button**, so scoring agents gated on residency without ever seeing it. Do not cap the body, or keep the tail as well as the head.
6. **Exact-string dedup missed `(Remote)` and `(gh <id>)` suffixes**, so an already-applied role ranked first. Dedup on **normalised company + title** as well as the Built In id, and **never normalise away a team qualifier** (two reqs with the same title and different team parentheticals are different reqs). **Generic titles repeat across many reqs at large employers — a title match there is not a duplicate.**

## Where Built In's data lies

- **Card tags and JD bodies disagree on remote/hybrid.** A card's tag, the JD's own location line and the company profile's office policy can all disagree. Verify in the body.
- **Pay-zone fine print.** Zone-based floors, hub-state vs other-state bands and city-of-residence pricing all appear. A zone-banded or OTE band is not a number for the candidate's location: a headline can be materially lower in the candidate's zone, and a top figure can include incentive pay.
- **The card band can understate the JD's real comp.**
- **THE CARD BAND CAN BE WELDED ACROSS PAY ZONES.** Built In has rendered a range that no zone pays — one zone's floor joined to another zone's ceiling and presented as a single band. The top of it can belong to a zone the candidate can never be in. On any zone-banded employer the card band is an envelope, not a band; **the band does not enter a score or a stack rank until the employer's own zone table has been read** and the row matching the candidate's address found.
- **Company policy surfaces in JDs** — application caps per period and excluded states. Worth reading for. Residency exclusion lists can sit in the footer (see failure 5).
- **Date defects.** Built In post dates are stale, and one defect hid a closing window: a posting badged "Be an Early Applicant" with an old post date and NO deadline was, on the employer's ATS, a repost whose applications closed within weeks. Verify the deadline on the employer's ATS before queueing anything from this board.
- **The company-profile sidebar can describe a DIFFERENT COMPANY of the same name** (different country, size and business). The pay band and JD text were correct and only the company data wrong, which is the dangerous shape — it sits in the panel a quick stability read would trust. Verify the employer on its own site before using Built In's profile.
- **Band hygiene:** reconcile currency, and never treat a headline figure as location-specific.

## The apply control

- **"Easy Apply" means the application NEVER REACHES THE EMPLOYER'S ATS.** A card tagged Easy Apply routes to Built In's own hosted proxy form; `?handler=ApplyRedirect` just bounces back to the listing with no handoff. Applying there files with Built In, not the company.
- **The href shape does not tell you where it goes.** The same `?handler=ApplyRedirect` href navigates correctly out to the employer's ATS (Jobvite, Ashby, Greenhouse observed) when there is no badge. **The EASY APPLY badge is the discriminator, not the URL.** Scan the listing visually and search the page text for "easy apply" before clicking.
- **Never click an Apply control on this board without checking the badge first.** If the account is signed in, Easy Apply also submits whichever resume is stored on the Built In profile, so it can bypass a review-and-submit gate and send the wrong resume lane.
- **Apply on the employer's own form, always.** Built In's own form can error; when it does, go to the employer's board (often Greenhouse) rather than retrying Built In's form.
- **A redirect can land on the employer's generic careers index rather than the req** (the employer's own detail route was itself broken). **That is a STOP, not a puzzle to solve.** Do not reconstruct an ATS URL from a numeric id that merely has the right shape; filling a form that cannot be proven to be the req is worse than not applying.
