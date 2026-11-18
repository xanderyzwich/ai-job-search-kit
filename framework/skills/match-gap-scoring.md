# Skill: Match / Gap Scoring

**Load when:** scoring a job description against the candidate, or an agent is told to score a batch for a sweep.

**Pairs with:** `sweep-pipeline.md` and `stack-rank-presentation.md`. **The numbers live in `private/profile.yml`** (`base_salary_floor_usd`, `comp_priority_threshold_usd`); read them there and never copy a figure into this file. Gates and calibration specific to one candidate belong in the instance's own scoring skill.

---

## Step 0 — Already decided?

**In a delegated sweep skip this step:** the coordinator already deduped against the tracker at sweep start, and a scoring agent must not load the whole tracker. Run it for a single-posting check. Match the JD against the tracker by `job_url` first, then by normalized company + title. The title key is not unique: read every hit. Any existing status stops the scoring; return the company, title, status and the row's `notes` verbatim — that is usually the actual answer.

## Step 1 — Pay tier, and stop early if it is Bad

Judge by the range TOP, never the bottom.
- **Priority** — top at or above `comp_priority_threshold_usd`: in scope and flagged Priority on the row (a tag and, where `profile.yml` states an ordering rule, an input to it — never an extra gate).
- **Standard** — top at or above `base_salary_floor_usd` but below the threshold: in scope, judged on fit.
- **Bad** — top below the floor: STOP. Return company, title, tier "Bad", one-line reason. Score nothing else; it never enters a stack rank. A pay exception is a deliberate owner override, not a scoring outcome.
- **Unknown** — comp not disclosed: proceed. A strong result everywhere else is itself the signal to find the real number.

## Steps 2-3 — Hard and nice-to-have match

List every hard requirement the JD names (not preferred) and mark each matched or not against the candidate's skills ledger, applying documented reframes only where the JD is not rigid about the literal technology. `hard_match_pct` = matched / total. Do the same for items the JD frames as preferred: `nice_match_pct`, or N/A when it names none (N/A is not 0, except in the formula below).

## Step 4 — Composite

`tech_fit = hard_match_pct + 0.5 * nice_match_pct`, N/A counted as 0 for this formula only. Uncapped; report the raw number. If the JD named no preferred items, record `nice_reqs = 0` so downstream tools can relax the floor for the structural cap at 100.

**The same formula runs again over a second requirement set** where the posting has one (for example management duties), recorded as `mgmt_fit`. A set the posting does not ask about is N/A, never 0. The bar is per set: do not average; rank by the minimum of the sets present.

**Write the result to the tracker columns**, not only the row's note: `tech_fit`, `mgmt_fit`, `hard_reqs`, `mgmt_reqs`, `nice_reqs`. `hard_reqs` and `mgmt_reqs` hold the requirements THEMSELVES, pipe-delimited, each prefixed `+` matched or `-` missed — not a count. A score that exists only in prose cannot be queried.

## Step 5 — Alignment

A lookup against the candidate's alignment register, matched by business practice rather than only by name. Good, bad or neutral. A rating only, unless the candidate has declared a specific employer excluded.

## Step 6 — Flags

Location and remote clarity (read the employer's own work-arrangement sentence; a multi-city posting proves nothing about remote), lane fit.

## Evidence, agents and the working bar

- **The evidence set is the candidate's whole verified record** (`experience_summary.md` and the resume ledgers), not only the skills ledgers. A requirement met by verified work is matched even if no ledger names the technology.
- **Rating agents are text-only:** they read the JD file from `temp/<sweep_id>/` and return the row; they do not browse.
- **The working-bar floor lives downstream** (in `backlog.py`'s admission floor), not in the scorer. Score honestly; let the threshold act later.

## Gates are not gaps

A gate is a property of systems the candidate has or has not operated (for example a scale class or a clearance), not a learnable technology, so no reframe applies. Gates are declared in the instance and stop a role outright; gaps lower a score. Keep them in separate registers.

## What to return (one tight row, not a cover letter)

Company and exact title · pay tier with a one-line reason · itemized hard requirements and percentage · itemized preferred items and percentage · composite with inputs · alignment tag · flags · the requirement lists · one-line recommendation. If a vague JD inflated the score, say so on the row.
