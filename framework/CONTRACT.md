# Private Data Contract

This is the interface `framework/` expects. Nothing in this repo requires knowing
whose job search it is, only that a `private/` directory exists alongside it, is
gitignored, and provides the files listed below in the expected shape. This document
describes the shape without containing anyone's actual data, and every filename here
is generic on purpose — using someone's real name in these paths would defeat the
point of this contract by leaking identity into the one document that's supposed to
describe the system in the abstract.

If you're setting this up for yourself: copy each template out of `framework/templates/`
into `private/` under the name listed here, then fill it in.

---

## Required files

| Path | Purpose | Template |
|---|---|---|
| `private/profile.yml` | Structured facts: identity, comp floor, location constraints, role criteria, lane definitions, title lists. The one file every generic reference to "the candidate's floor" or "the candidate's constraints" resolves against. | `framework/templates/profile.yml` |
| `private/experience_summary.md` | The verified source of truth for every role, claim, and number. Everything else defers to this file; if a document and this file disagree, this file wins. Exists specifically to prevent claim drift across sessions — a resume bullet or cover letter line should never introduce a fact that isn't traceable back here. | `framework/templates/experience_summary.md` |
| `private/job_search_skill.md` (or its decomposed equivalents under `private/skills/`) | The filled-in version of the framework's methodology: your actual lane assignments, your actual search history and session notes. | `framework/skills/*.md` |
| `private/resume_strategy.md` | Which resume leads with what, and why, for your specific lanes. | `framework/templates/resume_strategy.md` |
| `private/search_criteria.md` | Your actual board filters, saved queries, and lane-tagged search results. | `framework/templates/search_criteria.md` |
| `private/job_tracker.csv` | Application log. Column schema below. | `framework/templates/tracker_schema.csv` |
| `private/SESSION_INIT.md` | Personal overlay: current positioning and open threads. Loaded alongside the public root `SESSION_INIT.md`, which stays generic. | `framework/templates/session_init_overlay.md` |

## Optional / generated (not required for the framework to function, but expected to exist once in use)

| Path | Purpose |
|---|---|
| `private/resume_ic.docx` / `.pdf` | Current IC-lane resume, built by `framework/scripts/build_resume.py` from `profile.yml` + `experience_summary.md`. |
| `private/resume_lane_a.docx` / `.pdf` | Current Lane A resume, same build path, different ordering. |
| `output/*.pdf` (repo-root sibling, also gitignored) | Generated cover letters and one-off deliverables. Not part of the contract since these are per-application artifacts, not standing state. |

---

## `profile.yml` schema

```yaml
identity:
  name: string
  email: string
  linkedin: string
  location: string

constraints:
  remote: string                    # e.g. "fully remote only"
  base_salary_floor_usd: number
  lateral_ok: boolean
  no_relocation_to: [string]        # list of states/regions, if any
  relocation_reason: string
  travel: string

role_criteria:
  seniority: [string]
  scope: string
  domain: string
  title_is_secondary_to: [string]

lanes:
  lane_a: { label: string, org_size: string, titles: [string] }
  lane_b: { label: string, org_size: string, titles: [string] }

linkedin_open_to_work_titles: [string]
```

Any framework skill or script that needs a personal value reads it from here at
runtime. If you're extending the framework and find yourself wanting to hardcode a
number, add a key to this schema instead.

## `job_tracker.csv` column schema

```
date_applied, company, role, salary_range, location, remote, job_url,
application_status, cover_letter_sent, linkedin_dm_sent, dm_recipient,
referral_source, notes
```

---

## Why this split exists

The framework should read correctly with `private/` deleted entirely — every
sentence in `framework/` and the public root should still parse as general guidance,
not become a dangling reference. That's the test for whether something belongs in
`framework/` or `private/`: if removing your real data breaks the sentence, the
sentence has a personal fact in it that should have been a variable.
