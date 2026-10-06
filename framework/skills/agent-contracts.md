# Skill: Agent Contracts

**Load when:** dispatching a sub-agent for any part of the search, or writing
the agent prompt that will return to you. Both the coordinator and the agent
read this file.

**Pairs with:** the delegation section of `search-apply-ritual.md`, which says
WHY browser work is delegated; this file says what crosses the boundary.

---

## Why a contract and not a conversation

A sub-agent's working context is discarded when it returns. Only its final
message reaches the parent — which is the whole point, and also the whole risk:
anything the agent knew and did not say is gone. A contract is what makes the
return small enough to be worth delegating and complete enough to act on.

**The parent holds decisions and tables. Agents hold pages, text and
screenshots. Disk holds everything in between.** Content that one agent produces
for another goes to a file; the parent passes paths, never payloads.

## The three rules that make returns usable

**1. Demand a literal shape.** End the prompt with `FINAL message: ONLY one
JSON object` followed by the literal object. Tested across eight agents: all
eight complied, with no prose and no code fence. Without it, returns drift into
narrative and the parent has to re-derive what the agent already knew.

**2. Errors come back IN the object, never as prose.** Give every contract an
`error` field and say that a failed item belongs in the result rather than in an
apology. With several agents running, partial failure is the normal case.

**3. Create the output directory before dispatching.** A file-write tool that
does not create parent directories will let every agent do its work and then
fail at the last step — a whole batch lost for one missing `mkdir`.

## Which skills an agent loads

**Role skills are a fixed list. Surface skills are derived from a name.** The
parent hands the agent a surface name; the agent derives the path. Nothing scans
an index to choose.

| role | fixed | derived |
|---|---|---|
| harvest | contracts · browser rules · constraints · **search-execution** | the board file for the named board |
| fetch | contracts | the board file for the named board |
| browser-JD | contracts · browser rules | the board file |
| score | contracts · the scoring skill **and its `Depends on:` set, minus anything the coordinator already did** (it dedups upstream, so the tracker is not loaded here) | — |
| rank | contracts · the scoring skill (its sort rule and flag vocabulary) | — |
| apply | contracts · browser rules · cross-vendor form rules (which carry the JD-divergence check) · the profile · the resume-lane skill | the ATS file for the named vendor |

**A ROLE INHERITS ITS SKILLS' DEPENDENCIES.** If a skill declares
`Depends on: X`, a role that loads that skill loads X too. This is not
bookkeeping: the scoring skill names an experience record as its verified
backbone *and documents a real under-scoring caused by that record's absence* —
agents marked genuine, already-written-down experience as unmatched because the
evidence pack was short. A load list that names the skill but not its
dependencies rebuilds that exact failure structurally. **Close the list
transitively, or the `Depends on:` header is decoration.**

**Why harvest loads a query-construction skill and the others do not:** a board
and a careers site do not share a title vocabulary, so a query narrowed against
the wrong words measures the query rather than the board. That rule is
execution-time knowledge and it has to reach the agent running the sweep, not
only the coordinator choosing the board.

**No file for that surface yet?** That is not an error state — it is the
new-surface evaluation in `board-evaluation.md`, whose deliverable IS that
file.

## The contracts

Shapes below are the minimum. Add fields freely; never drop one.

**harvest** — one row per listing seen, plus the sweep's own cost.
```
{ "rows": [ {company, role, url, comp, location, remote, posted, live} ],
  "screened": N, "already_known": N, "minutes": N,
  "capability_delta": "" , "error": "" }
```
`screened` and `already_known` **cannot be recovered later** — the tracker keeps
only survivors. `already_known` is free: the agent hits those collisions anyway.

**fetch / browser-JD** — a manifest, never the text.
```
{ "written": ["temp/<sweep_id>/<id>.txt"], "failed_urls": [], "error": "" }
```
Acquire raw text. **Never use a summarising fetch tool for anything that will be
scored** — a summary erases requirement counts and the signals that expose an
inflated score, and it still reads like a posting, so the substitution is
silent.

**score** — the record goes to disk; only the count returns.
```
{ "scored": N, "records": ["temp/<sweep_id>/scores/<id>.json"], "error": "" }
```

**rank** — the one artifact the parent actually shows a human.
```
{ "table": [ {rank, score, reqs, company, role, pay, flag} ], "error": "" }
```

**apply** — a fill report, and nothing submitted.
```
{ "filled": [{field, value}], "blank": [{field, why}],
  "unanswered_by_profile": [], "needs_foreground": [],
  "req_id": "", "jd_divergence": {}, "login_required": false, "error": "" }
```
`needs_foreground` is for fields a DOM-level set cannot drive — typeahead
widgets, comboboxes, file upload. `login_required` returns as a **decision** for
the human ("this one wants an account — worth it?"), never as a silent block.

## What an agent must never do

- **Submit anything.** The agent fills and stops; the human reviews on the live
  form and submits. Delegation costs the review nothing, because the review was
  never happening in the transcript.
- **Choose what to apply to.** The parent presents; the human picks.
- **Edit a skill file.** A capability change returns as `capability_delta` data.
  Writing it into the right file is a separate job for a context that knows the
  repository's standards — not an agent mid-sweep, and not a coordinator in the
  middle of getting applications out.
- **Return content the parent did not ask for.** If it is large, write it and
  return the path.

## Write as you go

A long harvest that returns everything at the end loses everything if the agent
dies near the end. One file per item, as it lands, means a crash costs one item.
