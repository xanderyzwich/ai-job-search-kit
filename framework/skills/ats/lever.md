# Skill: ATS — Lever (public postings API)

**Load when:** reading a `jobs.lever.co/<slug>` board for discovery, JD harvest or req counts.
Application filling is retired; the owner applies themselves.

**Overlay:** if the instance has `skills/ats/lever.md`, read it too — it holds that search's filters, verdicts (for example "do not sweep") and results.

---

## Capability — as of 2026-11-17

| | |
|---|---|
| listing page | **text OK, no browser** — one JSON request returns the whole board, JD bodies included |
| individual JD | **in the listing payload** — no per-job fetch needed |
| liveness | **unverified** — a listed posting is a stronger signal than Greenhouse, but the check is still the employer's apply page |
| remote signal | `workplaceType` (`remote` / `hybrid` / `onsite`) plus `categories.location` free text |
| pay signal | `salaryRange` when the employer fills it; otherwise only the body text |

Verified on two boards: one small and fully remote, one with mixed field and engineering roles.

**Re-probe once per SWEEP, not per listing**, and update this block with the date. A capability change is reported, not self-written: an agent returns it as `capability_delta` and a context that knows this repo's standards writes it here.

---

## The call

```bash
curl -sS "https://api.lever.co/v0/postings/<slug>?mode=json"
```

`<slug>` is the path segment in `jobs.lever.co/<slug>`. Public, unauthenticated, one request, a JSON array. An unknown slug returns an error body, not an empty array. Confirm identity with a few titles before trusting a guessed slug.

## Fields per posting

- `text` is the title; `id` is a UUID; `hostedUrl` and `applyUrl` are the links; `createdAt` is epoch milliseconds.
- `categories` holds `location`, `commitment` and often `team` or `department`. Vocabulary is the employer's own: histogram `categories.location` and `workplaceType` across the whole board before filtering.
- `workplaceType` is the structured remote flag. `country` is a code and says nothing about where a remote employee may live.
- `descriptionPlain` and `description` hold the opening text; `lists` is an array of `{text, content}` sections (duties, requirements, benefits) that the main description does NOT include; `additionalPlain` is the closing block, often the pay and legal text. **Concatenate all three** or requirements and pay are lost.
- `salaryRange` is `{min, max, currency, interval}` and `salaryDescriptionPlain` its text. Both are absent when the employer does not use the field.

## Rules

1. **Pay is often only in the body.** Some employers leave `salaryRange` empty and state a US range in `additionalPlain` or a list. Search the concatenated text for a dollar range before recording "no pay posted".
2. **A tiered or location-adjusted band is one sentence, not a field.** Read it for the candidate's location tier.
3. **`createdAt` can be years old.** Old dates mean an evergreen req or a long-lived board, not a stale one; they are not a liveness signal either way.
4. **Remote evidence is `workplaceType` plus the location string; the body may add a geography rule.** A "remote" label with a region suffix (`Remote-EU`, `Remote-North & South America`) is not US-open by default.
5. **Dedup on the posting UUID, then on company and title.** A same-title match with a different UUID is a possible re-post; flag it, do not discard it.
6. **Field and territory roles share the board with engineering.** Filter by team and title family first, then read location.
