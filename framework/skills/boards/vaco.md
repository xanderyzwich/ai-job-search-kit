# Skill: Board — Vaco (staffing agency)

**Load when:** sweeping a Vaco job board, or any board on the `msts.network` /
Foundry platform — most of what follows is the PLATFORM's behaviour, not this
agency's.

**Overlay:** if the instance has `skills/boards/vaco.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

Addressed BY NAME. Shared sweep rules live in the board-strategy skill, if the instance has one.

---

## Posture: a staffing agency's public board is not its inventory

A recruiter at an agency may describe a concrete live req that is not on the
public board at all. Software roles can reach an office before they are posted,
or through a pool the public listing never shows. **For an agency this is the
normal shape, not an anomaly.** So the board is a contact surface first: the
useful question to a recruiter is "what roles are you working that aren't
posted", never anything about the public listings. Sweep the board only when the
local count for the searched area is material. The mechanics below make a sweep
cheap when it is worth doing.

---

## The surface — mechanics, verified 2026-11-04

```
https://jobs.vaco.com/api/requisitions/search?page=N&<filters>
```

**`/api/` is a lie: it returns server-rendered HTML fragments, not JSON** —
which is why it works with no browser. The same parameters work on the human
path `/home?<filters>`. Rows carry **Job Title · Industry · Location** and a
detail link `https://jobs.vaco.com/job/<id>/<slug>/en`.

**The reported board size is not the harvestable size.** A full page-by-page
census harvested fewer rows than the header reported. **The gap is
UNEXPLAINED** — paging drift, or rows the listing does not return. Do not quote
the reported total as a harvested figure.

### Parameters

| parameter | values | works |
|---|---|---|
| `keywords` | free text | **YES** — a two-word title phrase narrows the set |
| `job_type` | `direct hire` · `contractor` · `c2h` · `consulting` | **YES** |
| `location_center` + `lng` + `lat` + `location_distance` | place string, coords, miles | **YES** |
| `category_id` | integer | **YES** |
| `on_site` | `Hybrid` · `On-Site` · `Remote` | **FILTERS, RETURNS ZERO ON ALL THREE** |

**`job_type` partitions the board exactly — its four values sum to the reported
total.** That sum is how you prove a filter is real. Run it when adding one.

**An UNRECOGNISED parameter is ignored harmlessly** (`bogus_param=xyz` left a
keyword search unchanged). Only parameters the server knows can hurt you.

**`on_site` is dead across the whole board, including on their own frontend.**
Not a tooling artefact — `/home?on_site=Remote` shows the same no-results page
in a browser. The field exists in their form with three options and is
evidently populated on no requisition at all.

---

## The response contradicts itself

**A search matching nothing returns, in ONE response, in this order:**

1. *"Sorry, no jobs found for that search."* + search suggestions — **TRUE**
2. `Results : (1–25 of N)` — **FALSE**
3. a table of 25 job rows — **FALSE**, and not the unfiltered page 1 either

**The only trustworthy signal is the string `no jobs found`:**

```bash
curl -s "$API&$FILTER" | grep -qi "no jobs found" && echo "ZERO RESULTS"
```

It cost two wrong findings on 2026-11-04, one per reader, in opposite directions:

- **The machine trusted the COUNT.** the same total `N` came back for every `on_site`
  value, reported first as "the parameter is ignored" and then as "it poisons
  the query." Both wrong — it filters, and returns zero.
- **The human trusted the ROWS.** A zero-result query's fallback table still
  contained a real job that was then opened as if it matched. Verified
  afterwards: that job WAS in the fallback rows of that exact zero-result query.

**A page that reports failure in prose and success in structured output will
fool whichever one you happen to read.** Several other surfaces have no honest
empty state either (a dead req id returning plausible near-misses, a nonsense
phrase returning plausible jobs); Vaco is the one that admits it, and the
easiest to misread, because the admission is prose and the lie is data.

---

## Tested and rejected: bare `US` as a remote marker

Some rows render a location of just `US` instead of `City, ST, US` — a small,
consistent minority, enough to look like a deliberate marker for
national/remote. **It is missing data.** Bodies sampled from bare-`US` rows
mentioned remote no more often than city-located controls, most explicitly said
on-site or hybrid, and the titles were local work; samples that small are noise.
**Blank is just blank.** (Two sampled rows were the SAME posting under two ids
with an identical title — this board carries duplicate requisitions, like
Built In.)

**Consequence: the board has no remote signal at all.** `on_site` returns zero,
and location distinguishes cities from missing cities. The only way to know is
to read every body.
