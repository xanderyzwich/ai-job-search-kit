# Skill: Board Evaluation

**Load when:** a new job board is being considered, or an existing one is being
re-judged on whether it still earns a place in the rotation.

**Pairs with:** `search-apply-ritual.md`, which runs the sweep once a board has
earned its place. This is the rarer, separate question of whether it should.

---

**Split out on 2026-10-06.** It had lived inside the sweep runbook, but it is a
different moment with a different reader: the runbook is read constantly, this
is read when a board is added. Its deliverable also changed — it now produces
that board's own file, from `framework/templates/skill_surface.md`, rather than a section
appended to a growing one.

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

### Map the board's vocabulary before trusting any one keyword

**A first look at a new board, or at an employer's own careers site, starts
with no keyword at all, or with the full title family run side by side:
engineer, developer, software, application, architect, systems, platform.**
Record the hit count per term. Narrow only after you know which words this
board actually uses.

The reason: titles are an employer's vocabulary, not the candidate's, and one
missing word makes a whole inventory invisible while the search looks like it
worked. Two first looks on the same day, one at a single-keyword board and one
at an employer site, show the failure. One employer titled nearly all of its
software engineers "Systems Engineer", so a search for "software" returned one
real engineering req out of roughly twenty. A board searched only for
"architect" looked tiny, but nobody had checked whether "engineer" or
"developer" held more. The keyword picks the result set, so it cannot also be
the thing that tells you whether the result set is complete.

What to record, alongside the five measurements: the per-term counts, which
terms return mostly noise (facilities, mechanical, sales "engineers"), and
which terms the board or employer uses for software roles. That list belongs
in the instance's filled search-criteria file, so later sweeps start from
known-good terms and don't rediscover them.

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

