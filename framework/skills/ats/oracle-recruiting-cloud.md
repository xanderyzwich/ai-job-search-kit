# Skill: ATS — Oracle Recruiting Cloud (Candidate Experience) <!-- leak-scan: allow -->

**Load when:** sweeping or reading any careers site hosted on Oracle Recruiting <!-- leak-scan: allow -->
Cloud — `*.fa.*.oraclecloud.com/hcmUI/CandidateExperience/...`, or a branded
careers host whose HTML or redirect chain mentions `oraclecloud.com`.

**Overlay:** if the instance has `skills/ats/oracle-recruiting-cloud.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results. <!-- leak-scan: allow -->

**Addressed BY NAME** (`skills/ats/oracle-recruiting-cloud.md`), not by routing. <!-- leak-scan: allow -->
Company-specific state stays in the private instance's per-company files.

---

## The headline: the SPA has a public JSON API. Do not browse it.

The Candidate Experience UI is a JS-rendered SPA — a plain fetch of a job URL
returns nothing, which is why sweeps of these boards used to need a live browser
and cost a session. **The SPA's own backend is an unauthenticated REST endpoint
that returns the full board as JSON, including whole JD bodies.** No browser, no
extension, no rate limiting observed. Discovered 2026-10-14; a full board sweep
plus JD reads took under two minutes.

**This skill is vendor-scoped, not employer-scoped.** Treat any careers site
whose HTML or redirect chain mentions `oraclecloud.com` as covered here.
Fingerprint first, then reuse: a branded hospitality careers host that
fingerprinted as Oracle Recruiting Cloud was searchable with this card on <!-- leak-scan: allow -->
2026-10-21, with no new capability.

**The one input you need is the site number** (for example `CX_1009`). It is in
the careers URL and **it changes** — one board moved `CX_1` → `CX_1009` within
two days. If a call returns nothing, re-read the site number off the live
careers URL before concluding the board is empty.

## Search — list requisitions

```
GET https://<host>/hcmRestApi/resources/latest/recruitingCEJobRequisitions
  ?onlyData=true
  &expand=requisitionList.secondaryLocations
  &finder=findReqs;siteNumber=<CX_n>,limit=200,sortBy=POSTING_DATES_DESC
```

`expand=requisitionList...` is **not optional**: without it the response carries
`TotalJobsCount` but an empty `requisitionList`, which reads exactly like "no
results" and will make you report a live req as closed. Found the hard way.

Useful `finder` terms, comma-separated inside the single `finder` value:

- `keyword=<text>` — also the liveness test: `keyword=<req id>` returns that one
  req, or `TotalJobsCount: 0` if it is gone.
- `selectedCategoriesFacet=<id>` — the real discipline filter.
- `selectedPostingDatesFacet` — partitions by posting date.
- `facetsList=CATEGORIES;LOCATIONS;WORKPLACE_TYPES` — returns facet blocks on the
  response item (`categoriesFacet`, etc.).
- `limit` / `offset`, `sortBy=POSTING_DATES_DESC`.

**Getting a category id:** the bare `categoriesFacet` returns only the TOP TEN
categories by count, and on a board dominated by non-technical roles the
technology category may not be in the top ten. Run any narrowing keyword first
(`keyword=software`) and read the id off that response.

Each requisition carries `Id`, `Title`, `PostedDate`, `PrimaryLocation`,
`PrimaryLocationCountry` (filter by country code locally), and
`WorkplaceTypeCode` — `ORA_REMOTE` / `ORA_HYBRID` / `ORA_ON_SITE`. **The
workplace code is the board's claim, not the JD's**; read the JD before trusting
it.

## Detail — the full JD, including the pay range

```
GET https://<host>/hcmRestApi/resources/latest/recruitingCEJobRequisitionDetails
  ?onlyData=true&expand=all
  &finder=ById;siteNumber=<CX_n>,Id="<req id>"
```

The finder name is `ById` (not `findReqDetailById`) and **the id must be
quoted inside the finder string**. `ExternalDescriptionStr` is HTML — strip tags
and unescape entities. There is no salary field: the pay range lives in the
description prose, so grep the text for a currency sign. **No hit means no range
posted**, which is itself a finding.

## Large boards: partition the pull

A large retail or service employer's board can hold on the order of 10,000+
requisitions, almost all store roles (measured 2026-11-13). Page size caps at
200 and **`offset` stops returning rows at 10,000**, so a full pull has to be
partitioned with `selectedCategoriesFacet` and `selectedPostingDatesFacet`.
Further quirks measured on that board:

- Sort options other than posting date descending are ignored.
- `WorkplaceTypeCode` was **null** on list and detail items there, so only the
  facet says on-site.
- The detail text is entirely in `ExternalDescriptionStr`; the responsibilities
  and qualifications fields are null.
- The keyword search matches description text, so generic terms are inflated by
  retail boilerplate.
- An employer's marketing careers URL may return 403 to scripts while
  redirecting people to the real Oracle-hosted site; probe the redirect target. <!-- leak-scan: allow -->
- **An empty result is not evidence of nothing new; retry.** A watcher script
  that diffs the finder against a seen-list should retry before reporting zero.

## Two JD-reading rules this ATS makes necessary

1. **Check for a PERM / labor-certification notice before celebrating a perfect
   stack match.** Tells, seen together on one posting: a do-not-interview style
   hashtag tag, an "Apply to <Legal Entity Inc.> ... or submit your resume to
   `<mailbox>@<company>.com`" block, a street-address location line, and
   requirements written as a fixed "Bachelor's plus five (5) years" recital of
   exact technologies. These postings exist to satisfy a filing requirement for
   someone already in the seat. They are the best-matching reqs on a board and
   they are not open roles.
2. **The workplace-type tag and the JD's own location language routinely
   disagree.** Read the JD line ("This is a hybrid role and would require to be
   near one of our three US office locations", "allows periodic telecommuting
   from anywhere within the <metro> area") and let it override the tag.
