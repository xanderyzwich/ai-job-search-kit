# Skill: Board — YC Jobs (Work at a Startup)

**Load when:** sweeping YC Jobs / Work at a Startup.

**Overlay:** if the instance has `skills/boards/yc-jobs.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/yc-jobs.md`), not by routing. Mechanics of this one surface only.

---

## Capability — as of 2026-11-12 (first probe, headless curl, no browser)

| | |
|---|---|
| listing page | **fetchable, structured.** `https://www.ycombinator.com/jobs/role/software-engineer` returns HTTP 200 with the whole listing embedded as JSON in the `data-page` attribute (`props.jobPostings`). Parse that, not the HTML. Each posting carries title, location, `salaryRange`, `equityRange`, `minExperience`, `visa`, `skills`, `lastActive`, `createdAt`, company name/batch/one-liner and the job URL. |
| individual JD | **fetchable.** `https://www.ycombinator.com/companies/<co>/jobs/<id>-<slug>` returns 200 with `props.job.description` and a `JobPosting` ld+json block. |
| `workatastartup.com` | 406 with an empty body to a plain curl; not needed, the ycombinator.com pages carry the same data. |
| applying | the apply link goes to `account.ycombinator.com/authenticate`, so **a YC / Work at a Startup account and login are required to apply.** Not tested. |

**THE LISTING IS A CAPPED SAMPLE, NOT THE WHOLE BOARD.** One URL returns 26 to 50 postings. `?page=2` returns the SAME postings as page 1 (36 of 36 overlap), so there is no pagination, and repeating the same URL returns the same set. Coverage comes only from varying the path, not from paging: `/jobs/role/software-engineer/<location>` (remote, new-york, chicago, san-francisco, seattle, austin, los-angeles, india), `/jobs/location/remote`, and the other `jobRoles` slugs. `?remote=true` does not filter (on-site postings come back). **Do not report a count from one page as the size of the board**, and do not read an end of paging as an end of results, because paging does not exist here. Whether the cap hides roles that no combination of role and location surfaces is UNKNOWN.

`lastActive` (for example "10 days") is the board's own freshness signal, but liveness still needs the employer's system, as everywhere else.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## URL and character of the board

```
https://www.ycombinator.com/jobs/role/software-engineer?remote=true
```

Free, directly YC-run, low scam risk. No seniority filter without a profile. Companies are almost by definition early-stage and funded, so the pool skews to small engineering orgs where technical leadership is thin.

## Logged-in filtered search cannot be reproduced headlessly

After creating an account, `workatastartup.com/companies` offers a far better filtered search than the public ycombinator.com pages (filters observed: role family, remote only, years-of-experience band, has salary range, job type). A signed-out request for the same filtered URL (sent with an `Accept: text/html` header, without which the host returns 406) returns the generic home page (`HomeV2Page`) with no filtered result list, so **the filtered result set cannot be reproduced headlessly.** Workflow: the candidate saves or pastes the result list (company names or `ycombinator.com/companies/<slug>` links), and each company's public job pages are then fetched and scored. A pasted result set is a point-in-time snapshot, not something the tooling can regenerate.
