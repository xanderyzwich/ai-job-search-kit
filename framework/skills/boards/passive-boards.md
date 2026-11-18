# Skill: Board — Passive boards / reverse-recruiting marketplaces (background lead generators)

**Load when:** evaluating or working a passive board or reverse-recruiting marketplace (background lead generators).

**Overlay:** if the instance has `skills/boards/passive-boards.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/passive-boards.md`), not by routing. Mechanics of these surfaces only.

---

## Capability — as of never probed

| | |
|---|---|
| listing page | **not probed** |
| individual JD | **not probed** |

No fetch capability on record either way. **Probe once at the start of the next sweep of this surface and write the result here with the date** — an absent row is not evidence that a browser is needed.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

Set up once, run alongside active outreach, don't require per-application effort. Verified 2026-07-08 unless dated otherwise.

- **Hired / LHH (myportal.lhh.com, under Adecco/LHH)** — reverse recruiting, no fee.
  - Profile setup has a "Practice Area" field with generic categories (Engineering & Construction / Innovation & Strategy / IT & Digital) — **IT & Digital is correct** for software engineering. The desired-salary field wants a single number, not a range.
  - **Confirmed UI bug (search screen):** after setting sidebar filters (Remote Jobs toggle, Practice Area, State, City), do NOT click the top "SEARCH" button — it silently wipes every sidebar filter back to the full unfiltered catalog (1247 jobs on the observed day). Correct flow: set each filter control directly, then click elsewhere to close any open dropdown — the count and list update live without ever touching Search. The freetext keyword field also appears non-functional (typing a title and clicking Search resets to the full catalog). The Practice Area field requires selecting an option from its autocomplete dropdown (type "IT", click the "IT & Digital (N)" checkbox) — freetext alone doesn't apply it.
  - Observed inventory 2026-07-08: Remote + IT & Digital = only 4 jobs total, all contractor IT-project-management/QA roles plus one mis-tagged listing — nothing in senior software IC or engineering-leadership lanes. The staffing-agency model looks weighted toward generalist contract/perm placements; worth rechecking periodically but don't expect much senior software inventory.
- **Underdog.io** — free, but invite-only: no direct signup, only an application at underdog.io/candidates/apply. Most selected candidates hear back within 1-2 business days if picked for a weekly cohort; only a small percentage make it. No cost either way, just a waiting game.
- **Himalayas** — correction: NOT free. Browsing is free but full registration (saved profile, alerts) requires a $9/mo tier. Equivalent value exists free elsewhere.
- **We Work Remotely** — correction: NOT a free board for candidates anymore (earlier info was stale/wrong). Job-seeker onboarding offers only two paid tiers: "WWR" at $2.95 first month then $14.95/mo with a **12-month commitment**, or "TopAccess Bundle" at $29.95/mo (also 12-month commitment, bundling several other boards' access). No genuine free tier found despite multiple web sources claiming one exists. A 12-month lock-in on a job board is not worth it; do not re-recommend this as free.
- **Nerdii (nerdii.co)** — a paid application service, not a recruiter: candidates pay $50 per interview scheduled plus a success fee of 10 days' salary on hire; employers don't pay. Cold outreach (2026-08-13) was templated — generic flattery, no company or role named, a scheduling link with a stale month parameter reused across a mass campaign. Not a scam, but the same category as Himalayas/WWR: a paid job-seeker-facing product, not a lead.
- **Y Combinator's Work at a Startup** — see `framework/skills/boards/yc-jobs.md`; free and directly YC-run.
- **Welcome to the Jungle** (absorbed Otta) — free to browse/apply, curated tech/startup postings with comp filters, strong US/EU presence.
  - **"Jobs matches"** (welcometothejungle.com/en/jobs-matches) is NOT a manual search; it is a pre-computed match feed built off the saved preferences panel (title band, seniority, remote, location, salary floor). Once preferences are set, the "New matches" tab surfaces a high-precision feed — the highest signal-to-noise of any board tried so far. Repeatable routine: revisit "New matches" every few days, scan cards for comp band and posted date (both shown inline), open only the ones worth a closer look. Criteria persist on the "Your preferences" panel.
- **Remote100K** — correction: NOT a profile-based passive board. The homepage states "Apply directly, no account required" — there is no login/register screen, it is a browse-and-apply curated listing feed (apply via each employer's own link). It is a "check back occasionally" board, not a "set up once" one. It also carries a sponsored third-party "Auto Apply" banner that is NOT part of Remote100K and should be skipped — mass auto-apply bots run against a quality-over-volume approach, and several charge a fee.
  - **Repeatable check routine:** click the category chip once (it's a toggle — a second click deselects it and silently reverts to the unfiltered feed, easily mistaken for the filter not working). Sort "Most Recent." Listings show salary band and remote scope inline. Screen out postings tagged remote for one other country only (unless work-authorized there) — several high-comp listings are country-restricted remote with non-USD comp.

**General lesson:** multiple SEO/content-mill sites (via web search) confidently described Himalayas and We Work Remotely as free for job seekers, and both turned out to have a real paywall once actually visited live. Don't trust "is X free" claims from search results without checking the live signup flow.
