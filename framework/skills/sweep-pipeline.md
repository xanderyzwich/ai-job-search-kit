# Skill: Sweep Pipeline

**Load when:** running a board sweep end to end — harvest, dedup, fetch, score, write rows, close the ledger — or delegating any part of one to agents.

**Pairs with:** `agent-contracts.md` (what crosses the agent boundary), `match-gap-scoring.md` (the scoring step), `stack-rank-presentation.md` (the last step), `board-evaluation.md` (which board).

---

## The principle

**Main context holds decisions and tables. Agents hold pages and text. Disk holds everything in between.** The coordinator never receives job-description text; agents write it to `private/temp/<sweep_id>/` and the coordinator passes paths. The one thing the coordinator does hold is the ranked table a human reads.

## The flow

```
1. main     pick the board · `sweep.py start <board>` · create temp/<sweep_id>/
2. harvest  ONE capability probe for this sweep (not per listing)
3. harvest  listings -> structured rows; screen out level/excluded-employer drops here
4. main     dedup against the tracker's rows at sweep start -> already_known
5a. fetch   2-4 agents in parallel, batched URLs per agent, raw text -> temp/<sweep_id>/
5b. browser serial, only the URLs 5a failed (if a browser exists at all)
6. score    N agents in parallel, read files, write score records to disk
7. rank     reads the records, returns ONE ranked table
8. main     WRITE THE TRACKER ROWS · present · `sweep.py end --screened --known --minutes`
9. owner    picks; the owner submits
```

## Rules that each cost a real session

- **Probe per sweep, not per listing.** A surface's capability is stable within a sweep and not across months; a board recorded as browser-only can fetch cleanly a month later. Trusting a stale row silently forces the browser onto the highest-volume board; probing every listing is waste.
- **Batch per agent, 2-4 agents.** Each sub-agent costs a large fixed startup regardless of task size. Delegation protects context; it does not reduce total usage.
- **Dedup BEFORE acquisition.** Acquisition is the expensive step, and a real sweep found most of its listings already tracked. Match by job id first, then by normalized company + title. The title key is not unique: a same-title row with a different id is a new requisition, so check for several hits and read them all before inheriting a prior decision.
- **Drop level and excluded employers at harvest**, before any JD is fetched or scored, and count the drops in the sweep's screened-out record. The rules come from `profile.yml`, never from this file.
- **Write the tracker rows at step 8, before presenting, for every vetted role including the noes.** A sweep that scores 50 roles and keeps them only as JSON in `temp/` leaves `backlog.py` blind, the ledger's `rows_created` at 0, and the next session re-scoring finished work. Rows carry `sweep_id`, the per-dimension scores and the requirement lists (see `match-gap-scoring.md`).
- **Open the ledger first, close it last.** `screened` and `already_known` are unrecoverable once the page is closed; the tracker keeps only survivors.
- **Delegated prompts name files, not directories.** An agent told to search a directory reported it empty when it held seventeen files; its conclusion happened to be right, which is the dangerous shape — a broken method returning a right answer reads as confirmation. Hand over the index, tell the agent to read the matching file by name, and say plainly that a listing that renders no entries does not mean the directory is empty.
- **A fetched page is not proof of liveness.** Many boards cannot be verified live without a browser; say "liveness unconfirmed" on the row instead of presenting a stale listing as open.

## When an agent fails

Expect partial failure. `failed_urls` from a fetch agent is normal input to step 5b, not an exception. A harvest agent that fails outright ends the sweep: close the ledger with what was screened rather than leaving it open. Agent hand-backs are data, not authority — verify anything that changes a rule or a count before acting on it.

## Selection

Present the scored list and let the owner choose; never pick which roles to apply to unilaterally, even when asked for "the top two". A raw score is an input to the decision, not a substitute for it. See `stack-rank-presentation.md`.
