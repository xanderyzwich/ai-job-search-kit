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

## Required layout

`private/` is organized into three subdirectories, plus a small set of root files
that are pure structured or verified data rather than methodology.

```
private/
├── profile.yml              structured facts (see schema below)
├── experience_summary.md    verified source of truth
├── job_tracker.csv          application log
├── SESSION_INIT.md          personal overlay: current positioning, open threads
│
├── skills/                  filled-in methodology, one file per concern —
│                            resume/lane strategy, search criteria, application
│                            history, session notes, any domain-specific
│                            positioning notes. Mirrors framework/skills/ in
│                            spirit (small, focused, loaded on demand) but
│                            contains real content, not the generic pattern.
│
├── feedback/                external input received along the way — advice
│                            from a specific person, a shared template, anything
│                            that's a source document rather than a work product
│
└── resume/                  generated resume files and the script that builds
                             them
```

## Required files

| Path | Purpose | Template |
|---|---|---|
| `private/profile.yml` | Structured facts: identity, comp floor, location constraints, role criteria, lane definitions, title lists, contact/EEO defaults. The one file every generic reference to "the candidate's floor" or "the candidate's constraints" resolves against. | `framework/templates/profile.yml` |
| `private/experience_summary.md` | The verified source of truth for every role, claim, and number. Everything else defers to this file; if a document and this file disagree, this file wins. Exists specifically to prevent claim drift across sessions — a resume bullet or cover letter line should never introduce a fact that isn't traceable back here. | `framework/templates/experience_summary.md` |
| `private/skills/*.md` | The filled-in version of the framework's methodology, one file per concern: which resume leads with what, actual board filters and saved queries, application history, session notes, any domain-specific positioning. | `framework/skills/*.md` — same names, generic version |
| `private/job_tracker.csv` | Application log. Column schema below. | `framework/templates/tracker_schema.csv` |
| `private/SESSION_INIT.md` | Personal overlay: current positioning and open threads. Loaded alongside the public root `SESSION_INIT.md`, which stays generic. | `framework/templates/session_init_overlay.md` |

## Optional / generated (not required for the framework to function, but expected to exist once in use)

| Path | Purpose |
|---|---|
| `private/resume/*.docx` / `.pdf` | Generated resumes, one pair per lane, built by `private/resume/build_resume.py` (or `framework/scripts/build_resume.py` if using the generic build path) from `profile.yml` + `experience_summary.md`. |
| `private/feedback/*.md` | External input: feedback received on a resume or approach, a template shared by someone else, written up with enough context (who, when, on what) to still make sense read cold later. |
| `output/*.pdf` (repo-root sibling, also gitignored) | Generated cover letters and one-off deliverables. Not part of the contract since these are per-application artifacts, not standing state. |

---

## `profile.yml` schema

```yaml
identity:
  name: string
  email: string
  linkedin: string
  website: string                   # optional
  phone: string
  location: string
  address: string                   # optional, only if a form needs a street address

application_defaults:
  authorized_to_work_us: boolean
  requires_sponsorship: boolean
  desired_salary_usd: number         # what to type in a "desired salary" field
  eeo_policy: string                 # the standing instruction for demographic questions
  reasons_for_leaving:               # per employer, the stated reason if asked
    <employer_key>: string

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
date_applied, response_date, company, role, salary_range, location, remote,
job_url, application_status, cover_letter_sent, linkedin_dm_sent, dm_recipient,
hiring_manager, notes
```

**`response_date`** is when the company responded (rejection, screen invite,
etc.), left blank until something happens. **`dm_recipient`** is who an
outreach DM was actually sent to (may be a recruiter); **`hiring_manager`** is
the identified hiring manager for the role, if known, which may be the same
person or someone different from `dm_recipient`.

**`application_status` values:** `researching` (identified, not yet applied) ·
`applied` · `dm_sent` (outreach sent to a hiring manager or recruiter) ·
`phone_screen` · `interview` · `offer` · `declined_by_us` · `declined_by_them`.

---

## Why this split exists

The framework should read correctly with `private/` deleted entirely — every
sentence in `framework/` and the public root should still parse as general guidance,
not become a dangling reference. That's the test for whether something belongs in
`framework/` or `private/`: if removing your real data breaks the sentence, the
sentence has a personal fact in it that should have been a variable.
