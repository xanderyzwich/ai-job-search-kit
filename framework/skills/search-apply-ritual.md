# Skill: The Search & Apply Ritual

**Load when:** evaluating a new job board, running a board sweep, vetting
candidate roles, submitting an application, or doing the weekly pipeline
review — the ordered runbook that sequences the other skills.

---

This file owns the ORDER of the pipeline; each step's substance lives in
the skill that owns it. (The session-boundary rituals — init and
end-of-day — live in the private session_init, which always loads.)

## Evaluating a new board (before it earns a place in the rotation)

A new board is a **go/no-go decision, not a sweep**, and the two get conflated
because both start by typing a query. The search ritual below already says sweep
and vet are different modes; this is that same rule one level up. Evaluating a
board asks "is this channel worth returning to," which is answered by five
cheap aggregate measurements. Sweeping it asks "what is in it right now," which
is answered per-listing and costs an order of magnitude more. **Do the first
one, decide, and only then consider the second.**

The failure this prevents, measured: one first-pass evaluation ran 55 minutes
across 122 tool calls, reading ~238 result cards and opening ~35 individual
job-detail pages — and **not one detail page contributed to the verdict.** The
verdict was already determined by four facts visible in the first few minutes.
The cost came from a brief that asked for board mechanics, multiple query
sweeps, AND per-listing extraction in one pass, with no gate between them.

### The five measurements (all card-level — open NO detail pages)

Run the smallest number of queries that produce these, using the board's own
best filters:

1. **Inventory size.** The total relevant pool with the right filters applied.
   This is the single most decisive number and it is usually available from one
   query. If the whole relevant pool is small enough to read end to end, the
   board is not a volume channel, and that conclusion is already reached.
2. **Poster concentration.** How much of that pool comes from one or two
   posters. A pool that looks adequate but is a third one staffing firm's
   evergreen reposts is not the size it appears to be.
3. **Freshness spread.** Sort by date, then read the top date AND the tail date.
   A board can be fresh at the top and carry postings over a year old below,
   which makes an unsorted or relevance-sorted read actively misleading.
4. **Comp visibility.** What fraction of cards show a wage at all, and roughly
   where the visible ones sit against the floor. A board where most listings
   post nothing cannot be screened on comp without opening everything — which
   is itself a finding about the board's cost.
5. **Provenance.** Is this original inventory, or a mirror of listings that
   already appear on channels in the rotation? A mirror can still be worth
   using — for metadata the original lacks — but it must not be counted as new
   reach, and applications generally belong on the source instead.

Also capture, only because it is nearly free and expensive to rediscover: does
searching require an account (never create one to find out), do the filters
persist in the URL or only in session state, and does an individual posting
render without JavaScript. That last one determines whether future passes can
skip the browser, which is the largest available speedup on any board.

### The gate

Stop here and decide, explicitly, before any per-listing work:

- **NO-GO** — record the verdict and the numbers behind it, and stop. A
  documented no is a real deliverable; it stops the board from being
  re-evaluated from scratch in three months.
- **CONDITIONAL** — the board is worth a narrow, named use (one geography, one
  kind of metadata, one cadence) and nothing broader. Write the condition down,
  because an unqualified "keep" quietly becomes a weekly obligation.
- **GO** — only now sweep it, as a separate task with its own scope.

**Budget steps 1 through the gate at roughly a quarter hour of tool work.** If
it is running long, the usual cause is enumerating the board exhaustively —
every option of every dropdown, every unexplained UI marker — rather than
enumerating what a good query needs. An unexplained badge or an unreachable
advanced-search page is a footnote, not a blocker; note it and move on.

### If the work is delegated

The gate has to live in the brief, because a competent worker handed a
three-part brief will complete all three parts thoroughly and correctly. Ask
for the five measurements and the recommendation, and say explicitly that no
detail pages should be opened. Then decide, and issue the sweep as a second
instruction if it earned one. The judgment about whether to spend an hour is
the delegator's to make, not the worker's to infer.

### What the deliverable is

A verdict, the five numbers supporting it, and the mechanics needed to re-run
the board later — filter defaults that must be changed, traps that make counts
lie, the fastest access path. Not a candidate list; that is the sweep's output.
Board mechanics belong in the instance's own filled search-criteria file,
stated generically enough that another board on the same platform benefits.
Dated inventory findings do not belong in a skill file at all.

## The search ritual

1. **Load the criteria.** This repo's `search-criteria.md` for the
   constraint logic; the private instance's filled version for the actual
   board filters, tier rules, and skip rules; `profile.yml` for the hard
   constraints (floor, location, travel).
2. **Sweep boards in the private file's priority order.** Collect
   candidates without evaluating deeply yet — sweep and vet are different
   modes, and mixing them makes both worse.
3. **Tracker check per candidate** (application-tracking skill): prior
   activity at the organization, duplicates, answers already given.
4. **Vet against hard constraints first** — location, travel, comp floor —
   then lane-route it (resume-lane-strategy) and make the honest gap read.
   For the tech match/gap, resolve EVERY stack term the JD names against the
   two-layer skills ledger in `resume/resume_content.yml` — the `skills` tree
   (Layer 1: on-resume items with per-node `depth` and `aliases`, matched on
   name or any alias)
   and `context_ledger` (Layer 2: off-resume items tagged evaluated-not-adopted,
   honest-gap, or tooling-only). Never call match or gap from memory: depth is
   decisive (a decade of Python tooling is not production depth) and a near
   name is not a match (Aurora is MySQL, not Postgres). The ledger, not recall,
   is the source of truth for whether something is a match, a caveated match,
   or a gap. Add the one-line ownership/stability note (employer-risk methodology).
5. **Log every vetted role**, including the noes: `researching` or
   `skipped` with the fit note, so the judgment is on record and the role
   is never re-evaluated from scratch.
6. **Decide timing now, not later.** Same-day application matters on
   boards that badge early applicants; a role worth applying to is worth
   applying to today or deliberately queuing with a reason.

## The apply ritual

1. **Re-check the tracker and the posting** — still open, not already
   applied, no contradiction with answers given elsewhere.
2. **Lane → resume** (resume-lane-strategy), **verify what the ATS actually
   attached, and refresh the stored copy if it's behind.** Platforms cache
   stale resumes and auto-attach them; the stored file on the platform is a
   second copy of the resume and it drifts. This step is where that gets
   fixed — not in a release-day sweep of every platform at once. The
   instance's platform-copies inventory records WHICH systems are behind the
   current build; the refresh lands the next time you submit through one,
   because that's the only moment a stale stored file can do damage. Check it
   every time, and update the inventory's confirmed date when you do.
3. **Cover letter triage** (its own skill); if writing, the private
   styles file chooses the approach and the human-writing gate runs before
   anything is final.
4. **Forms from the canonical config.** Every standing answer — work
   authorization, sponsorship, comp, EEO policy, reasons for leaving —
   comes from `profile.yml`, not memory. Knockout questions get true
   answers; transferability arguments live in freeform fields and
   conversations, never in inflated dropdowns.
5. **Check the instance's platform notes** for the ATS in play (autofill
   quirks, fields that silently drop, dashboards to confirm submission).
6. **Submit, then log the row immediately** with `source`, `lane`,
   `resume_version`, and notes capturing anything unrecoverable later: req
   IDs, unusual questions and the answers given.
7. **If a warm contact touches this company**, the sequencing rules in the
   warm-outreach skill apply — apply first, then message, and close the
   loop with anyone who helped.
8. **Views regenerate at close**; don't hand-edit the history file.

## The weekly review ritual

Several of this system's rules are "re-verify if stale" rules, and stale
things don't announce themselves — so once a week, one bounded pass owns
all the clocks:

1. **Run the funnel report** (application-tracking skill has the
   interpretation guidance and the latency caveat).
2. **Compare the resume build record against the platform-copies
   inventory** — any platform confirmed before the last build timestamp
   is serving a stale resume.
3. **Sweep the pending-outreach queue for age.** Every item older than a
   couple of weeks gets an explicit decision — nudge, retire, or keep
   waiting with a reason — rather than another week of silence by default.
4. **Check dated snapshots** (market context and the like) against their
   as-of headers; anything past its shelf life gets refreshed or marked
   unreliable before it misleads a vetting decision.
5. **Scan open threads for passed dates** — anything that was due and
   didn't happen becomes a today-item, not an artifact.
6. **If the instance has an application-aging policy**, apply it here;
   if it deliberately doesn't (a legitimate choice), the funnel report's
   no-response counts still get read with age in mind.

This review is ANCHORED to Friday's daily close. The daily-log tool tracks it
with an `anchor: friday` stamp: it comes due every Friday and STAYS due if a
Friday is missed, surfacing at the next `open` rather than resetting a rolling
clock. Running `close` on a due Friday performs the measurable part for you — it
runs the funnel report, writes `data/funnel_report.md`, stamps the ritual, and
makes its OWN `weekly-review: <date>` commit, separate from the daily `log:`
commit so the week's measurement reads as its own event in history. The judgment
steps above (staleness sweeps, the passed-date scan) are done in-session before
that close. A weekly ritual with no record of running is indistinguishable from
one that doesn't exist, and a stamp the tooling checks is better than a record
someone must read.

## Releasing a new resume version

Not a weekly event, but it belongs in this file's jurisdiction because its
ripple crosses the pipeline: other places store their own copy of the resume,
and every stored copy is a mirror that drifts. One auto-attached a stale
cached file to live applications before this rule existed.

Two things always happen at release: set the new `resume_version` tag for all
subsequent applications, and note the date so the funnel's before/after read
has a clean starting line. What happens to the mirrors depends on which kind
they are, and the instance's inventory should separate them:

- **Submission-system copies** — each ATS or board that stores a file and
  attaches it to applications. A release marks these stale in the inventory
  and stops there. The refresh happens at submit time for that one system
  (apply ritual, step 2), because that's the only moment a stale stored file
  can actually reach an employer. Walking all of them on release day spends
  real effort on systems the search may never touch again, and the effort
  expires the next time the resume changes.
- **Content mirrors** — a professional-network profile's own experience
  section, a personal site listed on applications. These get refreshed at
  release, because nothing will ever prompt it: they're read continuously by
  people the candidate never talks to, and there's no submit event to hang a
  check on. They also fail differently. A submission-system copy is merely
  old; a content mirror is retyped prose, so it contradicts the resume on
  facts — titles, employment date ranges, present-vs-past tense — while
  looking perfectly current. Before drafting one, check the field's character
  limit: a capped field turns a release into a selection problem rather than
  an append, and discovering that after writing the copy wastes the draft.
