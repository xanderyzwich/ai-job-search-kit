# Skill: Board — MyGreenhouse (cross-company Greenhouse search)

**Load when:** sweeping MyGreenhouse's cross-company job search. The Greenhouse
boards-API and embed-frontend mechanics belong to the Greenhouse ATS skill, if the instance has one.

**Overlay:** if the instance has `skills/boards/mygreenhouse.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME, not by routing. Apply/form-filling notes are out of scope here.

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

## The surface

URL: `https://my.greenhouse.io/jobs/search` (needs a signed-in session). It
searches every Greenhouse-hosted employer at once, and applications prefill from
the MyGreenhouse profile (Quick Apply), which is why it is fast. Filters live in
the URL, so a search can be re-run by link:
`?query=<terms>&location=United%20States&lat=<lat>&lon=<lon>&location_type=country&country_short_name=US&date_posted=past_five_days&work_type[]=remote`.

- `date_posted` options: within 1 / 5 / 10 / 30 days (`past_five_days` seen).
- A salary filter exists (stepped thresholds from the low tens of thousands up),
  but it likely drops postings with no pay shown, so leave it off on a first look.
- Location takes effect only after clicking Search.
- **Results load by infinite scroll and need real wheel scrolling (the
  `computer` scroll action); a programmatic scrollTo does not trigger loading.**
- Results are ranked by Greenhouse's AI relevance, so quality falls off after the
  first ~40 cards (interns, solutions engineers, QA).
- A broad title term returns far more cards than a technology term, and the
  technology term is noisier (adjacent stacks, security, DevOps). Prefer the
  title term.
- Known traps on submit: stale saved email, stale auto-attached resume,
  persisted EEO answers.

## Reading the search without a browser tool (learned 2026-11-17)

- **The search page needs the owner's signed-in session.** A plain fetch or an agent without that session cannot read `my.greenhouse.io/jobs/search`.
- **A "Save page" can produce a 0-byte HTML file.** Check the file size before parsing; an empty save is not an empty result set.
- **A console snippet that copies anchor text and hrefs works.** Run it in the owner's signed-in tab after the results have loaded, and paste the output back; it avoids both the save problem and the scroll-loading problem.
- **Suggested job URLs can be fetched by id through the public per-job API** (`boards-api.greenhouse.io/v1/boards/<token>/jobs/<id>`). That returns title and content but no status, so it enriches and never confirms the req is open.
