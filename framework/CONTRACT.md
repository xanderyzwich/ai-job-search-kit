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

`private/` is organized into five subdirectories, plus a small set of root files
that are pure structured or verified data rather than methodology. The organizing
principle: root files are canonical facts, `skills/` is methodology, `data/` is
working state, `feedback/` is external input, `resume/` and `scripts/` are
artifacts and tooling. If a file mixes methodology with dated state, it's in the
wrong place — split it.

```
private/
├── profile.yml              structured facts (see schema below)
├── experience_summary.md    verified source of truth
├── job_tracker.csv          application log — the ONLY hand-edited application
│                            record; every other view of it is generated
│
├── skills/                  filled-in methodology, one file per concern, plus
│                            CONVENTIONED SUBDIRECTORIES whose files are
│                            addressed by name rather than by routing (one per
│                            job board, one per ATS vendor). The MECHANICS of
│                            each surface ship in framework/skills/boards and
│                            /ats; a private file of the same name is an
│                            OVERLAY holding only this search's filters,
│                            results and decisions, and its header points at
│                            the framework file —
│                            resume/lane strategy, search criteria, outreach and
│                            screen-call patterns (a communications/ subdirectory
│                            is a reasonable grouping), any domain-specific
│                            positioning notes. Methodology only: nothing in
│                            skills/ carries dated state or snapshots. Mirrors
│                            framework/skills/ in concern (small, focused, loaded
│                            on demand) but contains this search's real content, not the
│                            generic pattern (for boards and ATS vendors,
│                            only the overlay). One exception to on-demand loading:
│                            session_init.md always loads first, unconditionally —
│                            see framework/skills/session-continuity.md for why.
│
├── data/                    working state, separated from methodology — the
│                            session log (dated diary, newest first), a small
│                            mutable open-threads file read at session start,
│                            dated snapshots with as-of headers, the pending
│                            outreach queue, per-company call briefs, and
│                            generated views (e.g. application_history.md,
│                            rendered from job_tracker.csv, never hand-edited)
│
├── scripts/                 tooling for the data layer. Which scripts get
│                            installed is bootstrap.py's COPIES; what each one
│                            does is its own docstring, indexed by the map
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
| `private/skills/*.md` | The filled-in version of the framework's methodology, one file per concern: which resume leads with what, actual board filters and saved queries, outreach and screen-call patterns, any domain-specific positioning. Methodology only — state (logs, queues, snapshots) lives in `data/`. | `framework/skills/*.md` — same concern, generic version. The mapping is by concern, not filename; a private instance may use different names (e.g. `resume-lane-strategy.md` ↔ `resume_strategy.md`) |
| `private/job_tracker.csv` | Application log, and the ONLY hand-edited application record. Column schema below. Every human-readable view of it (history tables, summaries) is generated by script rather than maintained in parallel — two hand-maintained files describing the same applications will eventually disagree. | `framework/templates/tracker_schema.csv` |
| `private/data/session_log.md` | The dynamic log: dated, chronological session entries, newest first. Read fresh from the live repo each session (top entry), never baked into static context. | none — starts empty, grows with use |
| `private/data/open_threads.md` | Small, mutable statement of what's currently open and due. Overwritten (not appended to) at every session close, and read first at every session start — so open state never depends on which log entry happens to be on top. | none — starts empty |
| `private/skills/session_init.md` | The one skill that loads every session unconditionally rather than on demand: directory map, startup checklist, tool notes. Meant to be stable, safe to load once into a persistent context feature and mostly forget about. The public root `SESSION_INIT.md` checks for this file and loads it if present. | `framework/templates/session_init.md` |

## Optional / generated (not required for the framework to function, but expected to exist once in use)

| Path | Purpose |
|---|---|
| `private/data/dashboard/application_history.md` | GENERATED from `job_tracker.csv` by a script in `private/scripts/` — human-readable submitted/closed/vetted tables plus summary counts. Never hand-edited; fix the tracker and regenerate. |
| `private/data/dashboard/funnel_report.md` | GENERATED by the daily-log tool at the Friday weekly close: the funnel report (response/advance rates and their splits) captured to disk so the weekly measurement is committed, not just printed. Rewritten each weekly close; never hand-edited. |
| `private/data/dashboard/` | Every rendered view the candidate reads, and nothing else. **Committed, unlike the assistant's own working views**, because the search gets checked from a phone through a web view of the repository when the machine is off, and a file in the ignored `temp/` never leaves the machine that made it. Its `README.md` is generated by scanning the directory, so a view added here needs no list edited. Never hand-edit a view: fix the record and regenerate. |
| `private/data/archive/` | Session-log entries older than roughly three weeks, one file per month, moved by the daily-log tool at close. Keeps the live log readable without losing history; nothing here is ever edited after the move. |
| `private/data/handoff.md` | The baton between harnesses. **`STATUS:` is the only line any tool reads** — `OPEN` means unconsumed and must be acted on, `CLEAR` means nothing pending and the body below is the last handoff kept for shape. Consumed with the daily-log tool, never by hand-editing the status. |
| `private/data/hubspot_watch.md` | Per-company board watch with title-based repost detection. A standing recurring check that runs when search work runs, **not automatically at session start** — init is read-only orientation and must not fire side-effecting checks. |
| `private/data/star_stories.md` | The story bank: CONTENT, not methodology. How to build a story — the beats, the question bank, what each question tests — lives in the screen-prep skill. A story here is a finished artifact to draw on under pressure, not a worked example of the format. |
| `private/data/resume_decisions.md` | Dated history of what changed in the resume, when, and on whose advice. **Not methodology** — the current per-lane strategy lives in the resume-strategy skill. This file answers "why is it this way" after the reasoning has left memory. |
| `private/data/scoring_decisions.md` | The same split for scoring: dated history of what changed in the match/gap procedure, when, and on what evidence. **Not methodology** — the live steps, formula and gate registers stay in the scoring skill. **Both files exist because a methodology file that accumulates dated narrative stops being loadable**: each was created when a size warning exposed the drift, and in both cases the size was the symptom rather than the problem. |
| `private/data/resume_platform_copies.md` | Inventory of every platform storing its OWN copy of the resume, with last-confirmed dates. **A stored copy drifts from the canonical build unless refreshed deliberately**, and this exists because a platform auto-attached a cached stale resume to new applications. |
**A WRITE-ONCE RECORD IS ANNOTATED, NEVER REWRITTEN.** A dated stack rank or
one-off study states what was true the day it was written, so repointing its
references at a successor would assert it had cited something that did not yet
exist. When a path it names later moves or dissolves, the file gains a
`<!-- moved-refs ... -->` block below its title — `old/path -> new/path (why,
date)`, one per line — and **the body is not touched**. The reference check
treats an annotated path as resolved, so the record stays both honest and
checkable; **exempting the whole directory instead would hide genuinely new
breakage in it.** The annotation's right-hand side is itself verified to exist,
because a note claiming a file moved somewhere it is not is worse than the dead
reference it was meant to explain.

| `private/data/sweeps/` | Procedurally generated search output — the sweep-effort ledger `sweeps.csv` and its archive, and any per-sweep stack-rank file. **The tracker is the durable per-sweep record**: every vetted role is a row carrying its `sweep_id`, its rank and its flags, so a stack rank can be re-rendered from it and a per-sweep rank file is optional. **Apply queues are DEPRECATED (2026-11-16)**: they belonged to the apply-agent flow, which is retired because it was slower and costlier than the owner applying himself; existing queue files are kept as history. **Separated because it grows without bound**: a data layer where forty generated files bury ten live-state ones is one nobody browses, and browsing it from a phone is how the search gets checked in the evening. |
| `private/data/probe_logs/` | One file per board or ATS holding the dated PROBE HISTORY behind that surface's skill: measurements, withdrawn claims, how each rule was found. **It exists because a skill holds learnings, not history**; the skill states the current rule and this file keeps the account. Loaded by nothing; read only to learn how a rule was found. |
| `private/data/analysis/` | Dated one-off studies — comp analyses, lane explorations, runway math, interview-day records, proposals. Written once and referenced later, never updated in place. Same reason for the split as `sweeps/`, different lifecycle: these accumulate by decision rather than by process. |
| `private/data/README.md` | GENERATED by `framework/scripts/build_data_index.py`, which lifts every description in it from THIS FILE's rows rather than restating them — one place defines a directory's purpose. It also **checks conformance**: anything on disk with no row here is reported as undocumented, and anything with a row but no file is reported as missing. Describes the layout only; `ls` answers what is inside. |
| `private/data/companies/*.md` | One glanceable brief per company with a live thread: contacts and relationship state, open roles and their gates, gaps to name proactively, next actions. Built to be read mid-phone-call. **A `## Scheduled` block holds every live commitment and deadline for the thread, one parsed line each** (`- <WHEN> | <KIND> | <WHO> | <NOTE>`, where `<WHEN>` may be `TBD` for a stage that exists but has no date) — an interview loop spans several people, so the loop lives here rather than on any one contact record. Live items only: a held stage leaves the block, a cancelled one is removed and the reason goes in the log. |
| `private/data/assessments/*.md` | One reference card per automated coding-assessment platform, written AFTER a real sitting and carrying only what is true of that platform and false of others. **These are DATA, not skills: no agent sits an assessment, so nothing here is executed** — they are read by the candidate before going in. Platform-independent preparation stays in the screen-prep skill. Write a card only for a platform with measured history; inventing guidance for an unused one gives it the standing of guidance paid for in failed assessments. |
| `private/data/contacts/*.md` | One record per contact whose value is NOT tied to a single employer — an agency recruiter who spans clients, a peer, a community contact. **A contact who IS the company stays in that company's brief**, read in context; the test is whether their value survives if the company goes away. Each record carries YAML frontmatter (`name`, `company`, `role`, `owed_by`, `last_contact`, `next_contact`, `next_action`, `acquired_via`, `linkedin`, `email`, `phone`, `channel`, `note`, `referral_type`, `referral_state`, `referral_cost`), referral provenance recorded at BOTH ends so a hub's yield is visible without a hand-kept tally, and a dated contact log newest-first. **`referral_type` names WHAT KIND of help this person can give, because the kinds have different economics and were being managed identically:** `internal` (an employee who can file a referral at ONE employer — a one-shot favour that is spent when used), `agency` (a recruiter with a book of reqs across many clients — not spent but ACTIVATED, and their inventory is frequently not on any public board), `peer` (no placement power), `own_employer` (inside the company being left — a reference or a future colleague, never a referral), `none`. **`referral_state` is `never_offered` · `live` · `informal_lead` · `listed_on_application` · `spent` · `dead`**, so an offer that was made and never used is distinguishable from one already cashed and from one whose employer has nothing to point it at. **`referral_cost` records what using it costs THEM**, per the cost-not-outcome rule — the lens that decides whether a favour is worth spending and when it has to be repaid. **`channel` is free text and unparsed: how the last real exchange travelled, because a reply should use the same one.** **What a contact's employer has open right now is deliberately NOT frontmatter: it rots in days, and a stale answer that looks authoritative is worse than none.** That join is computed by the view. **`last_contact` is a DATE, never a duration** — elapsed days are computed by the index, so nothing in the file goes stale by sitting still. **`next_contact` is the SELF-IMPOSED follow-up only**; a booked meeting or a hard deadline goes in the same `## Scheduled` block the company briefs use, because a scalar cannot hold a multi-stage loop and the second booking would overwrite the first. **Frontmatter stays flat `key: value` scalars** — the parser splits on the first colon, so a nested list reads as present-but-empty and a `HH:MM` line becomes a garbage key, both silently. |
| `private/data/*_snapshot.md` | Dated state with an explicit as-of header (market/layoff context, employer research, anything that rots). Snapshots live here so methodology files stay timelessly true. |
| `private/data/pending_outreach.md` | The outreach queue: connection requests sent, messages queued for acceptance. State only — the how-to lives in `skills/`. |
| `private/data/network_roster.md` | The known-humans roster: one row per person in the candidate's own network who has NO contact record yet, carrying current employer, title, start date, location, full prior-employer history with dates, and a relationship note the source platform cannot supply. **Employer is the join key for referral-first search**, so a known human whose employer is unrecorded is a referral that cannot be seen — this file exists to make that pool visible without paying for a full record per person before anyone is engaged. **Promotion rule, mirroring `pending_outreach.md`: a row graduates to `data/contacts/<first-last>.md` when the person is actually engaged, and comes OUT of this file** — a name in both places is two owners for one fact. **AUTHORED, not generated, and deliberately NOT under `data/contacts/`**, because the contact-index builder globs `data/contacts/*.md` and would render a roster as a junk contact row in the index and the calendar. Also the right home for the negative result: someone job-seeking, between roles, or outside the candidate's field is recorded as such, so they are never mistaken for an unexplored door. |
| `private/data/sweeps/sweeps.csv` | The search-EFFORT ledger, one row per board sweep: `sweep_id, date, board, query, lane, screened, already_known, minutes, rows_created, signal, provenance, notes`. The tracker records what a sweep produced; this records what it cost, which is the only way a board can be judged on yield per unit of effort rather than on raw volume. `screened` (listings actually looked at) and `already_known` (of those, how many were already tracked) are **unrecoverable once the tab is closed** — the tracker keeps only survivors, so nothing downstream can reconstruct either number. Machine-managed by `sweep.py`; `provenance` says whether a row was recorded live or reconstructed after the fact. |
| `private/data/employer_ats_registry.md` | Company → ATS → verified board token, appended as each is confirmed, so a board can be pulled in seconds instead of re-discovered. **Tokens live here; a board's QUIRKS graduate to `skills/boards/<name>.md` once that board is actually worked** — the registry answers "where is it", the skill answers "what goes wrong with it". |
| `private/data/rituals.yml` | Last-run stamps for non-daily rituals (weekly review, resume release, and so on), machine-managed by the daily-log tool, which warns at session start when a cadence has elapsed. A ritual may carry `anchor: <weekday>` instead of a rolling cadence; the weekly review uses `anchor: friday`, coming due each Friday, running at that day's end-of-day `close`, and committed separately as `weekly-review: <date>`. A mid-session checkpoint (`close --mid-day`) deliberately never runs or stamps it, because the review's judgment half is in-session work. |
| `private/resume/build_record.yml` | GENERATED by the resume renderer on every build: per-lane timestamp, output name, and content-file hash — the mechanical answer to "is any platform-stored copy older than the last build." |
| `private/scripts/*.py` | The installed tooling. **Which scripts land here is `bootstrap.py`'s COPIES; what each does is its own first docstring line, indexed into the context map** — this row deliberately does not list them, because the list it used to carry was two scripts out of date. The one behaviour worth stating at contract level is the daily-log tool's commit discipline: fold the day's working entries into the log, archive old ones, regenerate views, and make or amend a single daily commit — and on a due Friday a bare `close` runs the Friday-anchored weekly review as its own `weekly-review:` commit ahead of the daily one, while `close --mid-day` deliberately skips it. |
| `private/temp/context_map.md` | GENERATED at session start by `framework/scripts/build_context_map.py` (invoked from the daily-log tool's `open`): every skill's Load-when header (routing), every script's first docstring line (tooling), plus the ripple map, materialized into gitignored `temp/` so "what to touch when" is in context from the first moment. A view, never a source — rebuilt each session, never hand-edited. |
**EVERY VIEW THE CANDIDATE READS LIVES IN `private/data/dashboard/`**, whose
`README.md` is generated by scanning the directory — a web view renders it on
arrival, turning the folder into a menu instead of a listing. Add a view to the
folder and it appears there; nothing maintains a list.

**WHERE A GENERATED VIEW IS WRITTEN IS DECIDED BY WHO READS IT, and every one
states its audience in its own header.** A view the ASSISTANT reads to orient
itself — what skills exist, who the search knows — belongs in the gitignored
`temp/`: it is rebuilt every session, it is worthless the moment it is stale,
and committing it adds a daily diff nobody reads. A view the CANDIDATE reads
belongs in `data/`, committed, because the search gets checked from a phone
through a web view of the repository when the machine is off, and a file in
`temp/` never leaves the machine that rendered it. **Any link inside a
committed view is computed relative to that view's own directory** — a wrong
relative link does not fail, it renders as a link to nothing, and a web reader
is one tap from a 404 instead of a brief.

| `private/data/dashboard/contact_index.md` | GENERATED at session start by `framework/scripts/build_contact_index.py` (invoked from the daily-log tool's `open`) from the frontmatter of `data/contacts/*.md`: what needs a decision, time since last contact, and who referred whom. **Elapsed days are computed here so the records carry only dates.** A view, never a source — never hand-edited. |
| `private/data/dashboard/referral_map.md` | GENERATED alongside the contact index by `framework/scripts/build_contact_index.py` from the same contact frontmatter (`referral_type`, `referral_state`, `referral_cost`) and committed with the other candidate-facing views: who can open a door, at which employer, whether the offer is still live, and what using it costs them, grouped by kind of help. Records lacking `referral_type` are listed as unclassified rather than dropped. What an employer has open is deliberately not here; it rots in days. Never hand-edited: fix the contact record and regenerate. |
| `private/data/dashboard/calendar.md` | GENERATED at session start by the same script **and COMMITTED** (unlike the other rendered views, which live in the gitignored `temp/`) — the search is read from a phone through a web view of the repository when the machine is off, and a file in `temp/` never leaves the machine that made it. Internal links are computed relative to its own directory so they resolve in that web view. Built from four sources: the `## Scheduled` blocks of `data/contacts/*.md` and `data/companies/*.md`, the `next_contact` field of each contact record, any line in the open-items file's hard-dates section that LEADS with a bold date (that section stays prose by design, so anything else in it is simply not an event), and `rituals.yml` for the cadence chores the daily-log tool runs. **Ritual dates render in their own trailing section and never mix with the rest** — a tool's chore listed beside a person's commitments reads as something owed and makes the real items harder to see. Sections: overdue first, then this week, then upcoming, then **stages that are real but undated** — the ones a purely chronological view has nowhere to put and therefore loses. Lines that do not match the block grammar are reported under `DIDN'T PARSE` rather than dropped. A view, never a source — never hand-edited; fix the block and regenerate. |
| `private/resume/resume_content.yml` | Authored single source every resume lane renders from: the per-employer bullet pool, lane titles/summaries/ordering, and a two-layer skills ledger — `skills` (group→item→children tree of on-resume tech, each node optionally tagged `depth`/`years`/`aliases`) plus `context_ledger` (off-resume tech: evaluated-not-adopted, honest-gap, tooling-only). The renderer prints names only, dropping every tag. Also the match/gap source of truth: a JD's stack terms resolve against both ledger layers, never from memory. Bullets and ledger facts trace to `experience_summary.md`. | `framework/templates/resume_content.yml` |
| `private/resume/*.docx` / `.pdf` | Generated resumes, one pair per lane, built by `private/resume/build_resume.py` (installed from, and kept identical to, `framework/scripts/build_resume.py`) from `resume/resume_content.yml`. Optional content keys (all in the template, commented): `identity.phone`/`email`/`linkedin`/`linkedin_url` for live links, `{text, link_text, url}` bullets, omittable lane `summary`/`competencies`, lane `dormant`, and a `format: text` paste lane with `inherit`. |
| `private/resume/site_extension.py` | Optional. Instance-specific output the generic builder must not carry (e.g. a static-site page). If present beside `build_resume.py` and it defines `write_site(content, lane_key, content_path)`, the builder calls it once per lane after the normal outputs; it returns the written Path or None. Absent means the builder does nothing extra. Not installed by bootstrap; the instance writes it. | none (instance-specific) |
| `private/feedback/*.md` | External input: feedback received on a resume or approach, a template shared by someone else, written up with enough context (who, when, on what) to still make sense read cold later. Optional — none need exist; create one only when feedback actually arrives. Shape: `framework/templates/feedback.md` (a free-text record of the feedback plus an actionable takeaways list). |
| `output/*.pdf` (repo-root sibling, also gitignored) | Generated cover letters and one-off deliverables. Not part of the contract since these are per-application artifacts, not standing state. |

---

## `profile.yml` schema

```yaml
identity:
  name: string
  middle_name: string               # optional, for forms with a separate middle-name field
  legal_name: string                # optional, full legal name for forms/attestations that
                                    # require it rather than the preferred display name
  email: string
  linkedin: string
  github: string                    # optional, profile URL for forms that ask
  website: string                   # optional
  resume_url: string                # optional, where the resume or portfolio is hosted,
                                    # for forms with a link/URL field
  phone: string
  location: string
  address: string                   # optional, only if a form needs a street address

application_defaults:
  authorized_to_work_us: boolean
  requires_sponsorship: boolean
  work_authorization_type: string    # the exact option to pick from an ATS dropdown
                                     # (e.g. "US Citizen", "Permanent Resident", "H1B").
                                     # authorized_to_work_us and requires_sponsorship are
                                     # consistent with SEVERAL dropdown options, so neither
                                     # answers the question a form actually asks. Without
                                     # this key a session must either guess a legal
                                     # attestation or leave the field blank; the instance
                                     # that added it had left it blank five times first.
  desired_salary_usd: number         # what to type in a "desired salary" field
  salary_ask_rule: string            # optional: how to derive the number for a salary ask
                                     # from a posting's stated range (read by scoring and
                                     # application-prep skills; desired_salary_usd is the
                                     # fallback when no range is posted)
  salary_ask_divergence: string      # optional: what to do and record when the number
                                     # actually entered differs from salary_ask_rule
  current_salary_usd: number         # optional: for forms that ask for current compensation
  gpa_claimed: string                # optional: answer for GPA fields; note whether it
                                     # is verified against a transcript
  eeo_policy: string                 # the standing instruction for demographic questions
  submission_review_required: string # standing rule on owner review before any
                                     # application is submitted; binds every session
  reasons_for_leaving:               # per employer, the stated reason if asked
    <employer_key>: string

constraints:
  remote: string                    # e.g. "fully remote only"
  relocation: string                # optional: relocation policy in prose, including any
                                    # places that are exceptions
  base_salary_floor_usd: number
  target_salary_band_usd: string    # optional: preferred band above the floor ("low-high")
  housing_consequence_threshold_usd: number  # optional: comp below this has a
                                    # household-level consequence worth flagging
  comp_priority_threshold_usd: number  # optional: roles whose range reaches this are
                                    # ranked ahead of otherwise equal roles
  comp_range_rule: string           # optional: how a posted range is judged against the
                                    # floor (e.g. whether the top or the bottom counts)
  floor_review: string              # optional: notes on when and why the floor is revisited
  comp_flex_tier: string            # optional: how sub-floor roles are handled, if at all
  contract_tier: string             # optional: how contract/hourly offers are converted
                                    # to an annual figure and judged
  accept_and_continue: string       # optional: whether accepting an offer ends the search
  lateral_ok: boolean
  no_relocation_to: [string]        # list of states/regions, if any
  relocation_reason: string
  travel: string

role_criteria:
  seniority: [string]
  level_avoid: string               # optional: title level words the owner will not submit to; harvest drops them before scoring
  scope: string
  domain: string
  title_is_secondary_to: [string]

lanes:                              # OPEN-ENDED. Name the lanes this search
                                    # actually runs; two is not a fixed number.
  <lane_key>:
    label: string
    org_size: string
    titles: [string]
    ceiling: string                 # optional: the scope boundary this lane
                                    # will not cross, and why
    ordering: string                # optional: how roles rank INSIDE the lane
    resume: string                  # optional: which resume lane is sent
    boundary: string                # optional: the hard edge of what this lane
                                    # covers (e.g. which kinds of team it does not open)

linkedin_open_to_work_titles: [string]
```

Any framework skill or script that needs a personal value reads it from here at
runtime. If you're extending the framework and find yourself wanting to hardcode a
number, add a key to this schema instead.

## `job_tracker.csv` column schema

```
date_applied, response_date, company, role, salary_range, location, remote,
job_url, application_status, cover_letter_sent, linkedin_dm_sent, dm_recipient,
hiring_manager, source, lane, resume_version, notes, found_via,
sweep_id, tech_fit, mgmt_fit, hard_reqs, mgmt_reqs, nice_reqs, peak_stage
```

**`response_date`** is when the company responded (rejection, screen invite,
etc.), left blank until something happens. **`dm_recipient`** is who an
outreach DM was actually sent to (may be a recruiter); **`hiring_manager`** is
the identified hiring manager for the role, if known, which may be the same
person or someone different from `dm_recipient`.

**`source`** is where the role was found or how it arrived: a board name
(`linkedin`, `wellfound`, `indeed`, `wttj`, ...), `referral` (a warm contact
pointed at it), `recruiter` (inbound outreach), or `direct` (found on the
company's own site). **`found_via`** sharpens `source` to the specific
discovery point: the board listing URL where the role was first seen (which
may differ from `job_url` when the JD lives on the company's ATS), a search
query, a newsletter, or a person's name for referrals. URL preferred, short
text allowed, blank when it would only repeat `source`. **`lane`** is which
lane the application ran in. **The values are whatever `profile.yml` `lanes`
names** — an instance running IC and people-leadership lanes uses `ic`/`pc`; one
that also pursues first-line engineering management adds `em`. **The schema does
not fix the count**, and a reader that enumerates lane values rather than
deriving them from `profile.yml` will go stale the first time a lane is added.
**`resume_version`** identifies which resume build was submitted (a filename
or a date tag, e.g. `ic_2026-07-01`). These exist for funnel analysis:
response rate by source, discovery point, lane, and resume version is the
difference between "volume isn't working" as a feeling and as a measurement —
including which specific places keep turning up roles worth applying to.

**`application_status` values:** `researching` (identified, not yet applied) ·
`skipped` (vetted, decided not to apply — keeps the judgment on record so the
same role isn't re-evaluated from scratch) · `applied` · `dm_sent` (outreach
sent to a hiring manager or recruiter) · `phone_screen` · `interview` ·
`offer` · `declined_by_us` (withdrew after applying) · `declined_by_them` ·
`closed_no_response` (applied, the posting later came down, and no reply ever
arrived — a real submission that is no longer pending, and distinct from both
`declined_by_them`, which requires an actual rejection, and `skipped`, which
means never applied at all).

**`peak_stage`** is the FURTHEST stage an application ever reached —
`phone_screen`, `interview`, `offer`, or blank for never advanced. It exists
because `application_status` is current state and the two cannot share one
field: a terminal value overwrites an advancing one, so **every screen and
interview that ends in a rejection erases itself**, and an advance count built
on live status decays toward zero exactly as a search progresses. The deepest
results vanish first, because they are the ones most likely to have concluded.

It also makes rejections readable. A rejection at the résumé screen and a
rejection after a full interview loop are the same `application_status` and
diagnose opposite problems — one says the resume is not getting you into the
room, the other says the room is not converting. Outcome and depth are
orthogonal, which is why this is a separate column rather than a new status
value: adding `declined_after_interview` to the enum would conflate them and
force a migration of every existing rejection.

**It only ever ratchets upward**, raised automatically from
`application_status` by the daily-log tool. Nothing is hand-maintained: edit
the status exactly as before. Lowering it requires a deliberate hand edit,
because silently losing a high-water mark is the bug the column exists to
prevent. **Do not try to derive this on read instead of storing it** — both
obvious derivations fail. Notes prose says "interview" about automated video
screeners, scheduling mail, interview prep and negations like "never
interviewed"; a walk of version-control history keys on company plus title,
which changes when a row is retitled mid-process and then counts one
application as two.

**`sweep_id`** links the row to the search effort that produced it, keyed to
`private/data/sweeps/sweeps.csv` (`<board>-<YYYY-MM-DD>`). Without it the tracker
records what was found and never what it cost: "167 LinkedIn rows" could be
three sweeps or thirty, and a board cannot be judged on yield per unit of
effort. Written automatically by `sweep.py end`; blank is legitimate for a
row that did not come from a sweep (a referral, an inbound recruiter).
**`<board>-unknown` is a reserved form** meaning the board is known and the
sweep is not — rows that predate the ledger, or a sweep nobody opened. It is
a label, never a sweep: readers must exclude it from per-sweep rates, since
counting it would attribute rows to a sweep that has no screened count.

**`tech_fit`** and **`mgmt_fit`** are the per-dimension match scores. **Both
use one formula** — `hard_match_pct + 0.5 × nice_match_pct`, uncapped — applied
to two independent requirement sets: the technical one (stack, systems,
architecture, scale) and the management one (hiring, performance and career
development, cross-functional partnership, standards ownership, span of
control). They live in columns rather than only in prose so the tracker can
answer "what cleared the bar and never got applied to", which is the single
most common way a good role is lost: a stack rank gets worked top-down and the
day ends.

**The 0.5 is an exchange rate and it should be stated as one:** matching 10% of
preferred exactly offsets missing 5% of required. Full match on the required
set alone scores 100, which is the bar.

**A dimension the posting does not ask about is `N/A`, never `0`** — the same
rule the preferred list already uses. A posting with no management requirements
has a blank `mgmt_fit`, and that is not a failing score.

**THE BAR IS PER DIMENSION. THERE IS NO COMPOSITE.** *Full match on the
requirements is viable* is a claim about one requirement set, so two sets need
two readings. Averaging them hides the shortfall that matters: a role scoring
122 technical and 80 management is not "101 and viable", it is strong on one
half and short on the other, and the short half is the one that decides it.

**Rank by `min()` of the dimensions present.** Selection, not blending — both
numbers stay visible, nothing is averaged away, and no weighting constant gets
invented. For a posting with no management requirements `min()` is just
`tech_fit`, so a history scored before the second dimension existed stays
comparable and needs no rescoring.

**THE SCORE RANKS. IT DOES NOT GATE.** Gates are a separate register —
requirements that are historical facts a candidate cannot acquire, location,
and the comp floor. A low score on either dimension is a named gap to be stated
plainly, not an exclusion. **Do not let a dimension score become a gate**: it
would be the only score-gate in the system, and it would fire hardest on the
dimension with the thinnest data.

**`hard_reqs`** and **`mgmt_reqs`** are the requirements THEMSELVES, one list
per dimension — pipe-delimited, each item prefixed `+` matched or `-` missed:

```
+BS/CS or equivalent | +6 yrs engineering | +Java named | -applied cryptography
```

**A score without its requirements is not readable**, and a count was never
enough to make it readable. A vague posting scores HIGH precisely because it
asks for little that can be missed — the count tells you a score came from two
requirements, but only the list tells you *which two*, and that is what decides
whether the score means anything. The case that forced this: an employer whose
every posting shares one identical boilerplate required block, so the hard-match
percentage is 100% board-wide and carries no information. A count cannot show
that. A list shows it at a glance.

**The count is derivable from the list, so it is no longer stored.** Any reader
that sorts on a dimension score must show **the count** beside it and make
**the list** reachable — a flag, a detail view, the row itself. *(Softened
when the first reader was migrated: a full requirement list does not fit a
summary line, and a rule that cannot be followed gets ignored rather than
obeyed. The count in the summary and the list one keystroke away is what the
rule was actually protecting.)*

**Legacy rows hold a bare integer** where the list had not been adopted yet.
A reader distinguishes them trivially and must not treat an integer as a
one-item list. They were not backfilled: the requirements of a posting scored
months ago are not recoverable from a count, and inventing them would be worse
than leaving the row honest about what it knows.

*(A `tech_named_reqs` column counted how many hard requirements named a
specific technology. It was removed once the lists replaced it — the list shows
that directly, and a heuristic standing in for information nobody stored stops
earning its column the moment the information is stored. An instance still
carrying the column in historical rows can leave it; nothing reads it.)*

**`nice_reqs`** is how many preferred/nice-to-have items the posting named,
and **0 is a meaningful value, not a blank.** Where the composite weights
preferred matches at half, a posting that names none has a hard ceiling equal
to its requirement match — so a perfect match sits exactly on a 100 threshold
and one miss falls under, while a vague posting with a long preferred list
clears it easily. Any screening threshold must bend for these rows or it
systematically discards the cleanest matches in the file.

---

## Why this split exists

The framework should read correctly with `private/` deleted entirely — every
sentence in `framework/` and the public root should still parse as general guidance,
not become a dangling reference. That's the test for whether something belongs in
`framework/` or `private/`: if removing your real data breaks the sentence, the
sentence has a personal fact in it that should have been a variable.
