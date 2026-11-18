# Skill: Board — Jobspresso / Remotive / Dynamite Jobs

**Load when:** sweeping Jobspresso, Remotive or Dynamite Jobs.

**Overlay:** if the instance has `skills/boards/jobspresso-remotive-dynamite.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME (`framework/skills/boards/jobspresso-remotive-dynamite.md`), not by routing. Mechanics of these surfaces only.

---

## Capability — as of 2026-08-17

| | |
|---|---|
| listing page | browser (all three) |
| individual JD | **Remotive and Dynamite Jobs fetch fine**; Jobspresso needs the browser |

Oldest row in the set — re-probe before trusting it.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A surface's capability is stable within a sweep and not across months. **A capability change is reported, not self-written**: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

Remote-first aggregator boards. **Learned 2026-07-22 (Jobspresso specifically):** listing/search pages on these are frequently JS-rendered SPAs — direct `web_fetch` and RSS feeds often return empty or stale/archived content, and web search only indexes individual job pages (sometimes old/expired ones), not the live listing feed. A real sweep for current postings needs browser automation, not fetch/search alone. Individual job-posting URLs on Remotive and Dynamite Jobs fetch fine directly via `web_fetch` — this is a listing-page rendering problem specifically, not a problem with every page on these boards.
