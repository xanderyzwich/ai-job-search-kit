# Skill: ATS — Ashby (posting API and embedded board data)

**Load when:** reading any `jobs.ashbyhq.com` board for discovery, JD harvest or req counts —
the rendered page is useless to a text fetch and the JSON endpoint below is not.
Application filling is retired; reading and harvesting is unaffected.

**Overlay:** if the instance has `skills/ats/ashby.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

---

## The board is fully readable from code — use the posting API, not the page

**`jobs.ashbyhq.com/<org>` renders client-side, so a text fetch of it returns the job title and nothing else** (observed 2026-10-23: a title and employer name, no location, no band, no requirements — which reads exactly like an auth wall or a blocked request and is neither). **Do not conclude an Ashby board is unreachable from that.**

The public posting API returns everything, unauthenticated:

```bash
curl -sS "https://api.ashbyhq.com/posting-api/job-board/<org>?includeCompensation=true" \
     -H 'accept: application/json'
```

`<org>` is the slug in the board URL — `jobs.ashbyhq.com/<org>/<uuid>` gives `<org>`. Verified working 2026-10-23: HTTP 200, ~60KB, 5 jobs.

**Per job:** `title`, `location`, `jobUrl`, `applyUrl`, `descriptionHtml` (the FULL posting — strip tags and score it), plus `compensation` when the org publishes bands and `includeCompensation=true` is passed.

```python
import json, re, urllib.request
org = "<org>"
u = f"https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true"
jobs = json.load(urllib.request.urlopen(u))["jobs"]
for j in jobs:
    body = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", j.get("descriptionHtml") or ""))
    print(j["title"], "|", j.get("location"), "|", j.get("jobUrl"))
```

**One link is never the board.** A lead that arrives as a single posting URL from a contact may sit on a board with several roles, one at a materially better level than the one sent (a five-role board in the observed case). Whenever a contact forwards an Ashby link, pull the whole board — one request, and the forwarder saw only what they happened to notice.

**This makes Ashby a SEARCH surface, not just an apply surface**, which is the test that matters: an ATS is only a place to find work if it can be read across or enumerated without a browser. Ashby passes per-org.

## When the posting API is dark, the board page embeds the data (verified 2026-11-17)

An Ashby board can be publicly listed while `api.ashbyhq.com/posting-api/job-board/<slug>` returns nothing or 404. **An API miss does not mean the company is off Ashby.** A plain fetch of `https://jobs.ashbyhq.com/<slug>` returns static HTML (~100KB) carrying `window.__appData` JSON with `jobBoard.jobPostings` (title, team, location, `workplaceType`, compensation summary). Per-job pages `jobs.ashbyhq.com/<slug>/<uuid>` carry `__appData.posting` (full JD, compensation tiers) and a JSON-LD `datePosted`. No browser needed.

- **Slug variants are real.** Try the hyphenated form (`<two-word-name>` as `two-word-name`) and the bare form; a bare slug can be an unrelated company that returns a healthy count. Confirm identity by titles.
- **`workplaceType` and `isRemote` can be null** and then mean "unstated", not onsite. Do not drop or keep on a null; read the body.
- **The compensation field is often empty.** Pay then sits in the JD body, frequently tiered by metro with an "all other locations" tier. Search the body for a dollar range before recording "no pay".
- **Primary location can disagree with secondary locations.** A req listed as onsite in one city with a secondary `Remote (North America)` entry is onsite-primary; the secondary entry alone is weak remote evidence.
- **Residency sentences hide in the body.** A req labelled Remote can still say team members must live within commuting distance of a named hub. Search the JD body for "commuting distance", "must live" and "hub" before treating a Remote label as open.
- **A global remote label is not US eligibility.** `Remote, Global` and `Remote, AMER` name no country; employment eligibility is for the application form or a recruiter.
- **Board moves happen.** A company can leave Greenhouse for Ashby; the old board 404s and old ids are dead. Ashby ids are UUIDs, so id-based dedup against Greenhouse ids cannot match; dedup on normalised title.

## Capability — as of 2026-10-06

| | |
|---|---|
| application form | **mostly** text-readable (~1.1K chars) |

Inputs are named by **placeholder, not label**, so ref→label needs order inference or a lookup. The read tools were refused on this domain once while `javascript_tool` still worked — that script is the fallback.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

## Form-reading quirks (read-side relevance)

- Ashby renders some fields lazily as the page scrolls; `read_page`'s interactive-element scan can skip a field entirely (an Email field never appeared in one scan). Do not rely solely on `read_page`/`find` for completeness on multi-section progressive-render forms; finish with a full top-to-bottom scroll and screenshot pass.
- Ashby forms are short and often omit whole sections (across two forms: no work history, education, salary, cover letter or disability self-identification). Absent sections are normal. Required fields can appear in unusual places (pronouns required in Personal information rather than the EEO block; middle name required on a legal-name field).
- Location pickers vary in kind: one was a CITY autocomplete offering decoy same-name cities in other states, another a STATE-only picker. Read which kind you are in.
