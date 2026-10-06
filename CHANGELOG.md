# Changelog

The public framework's history, newest first. Dates are commit dates; the
framework is extracted from a working private instance, so entries here
generally land after the pattern they describe survived real use. The
private search data has its own repository and its own history — nothing
from it appears here.

## 2026-10-06 — The changelog rule was too narrow, and skipped the changes that mattered most

An audit found nine of fourteen framework-touching commits carried no entry
here. The ripple map was the cause: it said *a new skill owes a changelog line
if public*, and most of those commits added no skill at all. It now says any
public change owes one, in the same commit.

The selection pattern underneath is worth recording, because it will recur. The
entries that got written were for changes that felt architecturally large — a
new measurement, a new column, a file reorganisation. The ones skipped were the
fixes and follow-ups: a recorder that claimed rows it had not found, a tactic
measured and found not to work, a tool that fails silently in a background tab.

**Those are the entries with the most transferable content.** A reorganisation
is visible in the tree; a silent failure mode is not, and it is exactly what
someone rebuilds this from scratch to rediscover. The filter should be "would
someone otherwise relearn this the hard way", not "is this a big change".

Backfilling them was possible but strictly worse than writing at the time. An
entry reconstructed from a diff carries what changed; an entry written at the
decision carries why the alternative was rejected, and that half does not
survive the week.


## 2026-10-06 — Split by reader, not by topic

Two skills had grown past the point where a reader could load only what they
needed, and the cut that works is not the obvious one.

The sweep runbook carried the browser-delegation mechanics: how to read a page
without screenshotting it, how to fill a form in a background tab, what to
batch. Splitting that out by TOPIC would have taken the whole section with it
and left the runbook without its trigger — a coordinator would read the steps
and never learn to delegate at all, which is precisely how an earlier
delegation rule sat unread in a long file for two months. Splitting by READER
keeps the decision where it is made and moves only the mechanics to the agent
that executes them.

The same file also carried the question of whether a board earns a place in the
rotation at all. That is a different moment with a different reader — asked
rarely, where the runbook is read constantly — so it is now its own skill, and
its deliverable is that board's own file rather than a section appended to a
growing one.

A size warning is a prompt to look, not an order to split. One file reviewed
this way is staying as it is: its content half moved out, what remains is a
single coherent method, and the warning's reasoning is agent-centric while that
file is read by a human before a phone call. The reason is recorded in the file
so the next reviewer does not re-open the question.


## 2026-10-06 — A moved file breaks links silently

Splitting an oversized skill left four relative links one level short. Nothing
reported them: a dangling reference in prose produces no error, no failed
build, and no symptom until a reader follows one and finds nothing. The same
pass turned up a wrong data path that had been wrong for an unknown length of
time.

So the skill linter now resolves every backticked file reference and treats an
unresolvable one as an error. It lives in the existing linter rather than a
second script, which keeps it on a check that already runs and adds no
documentation ripple.

The rule that makes it usable is that a reference WITHOUT a slash is prose, not
a path. Skills say "run `the-tool.py`" and "the `state-file.md`" constantly, and
resolving those against a directory is wrong. A bare name passes if such a file
exists anywhere; only a spelled-out path, or a name that exists nowhere, can be
broken. The first version ignored that and produced fifty-one errors, none of
them real — the second time in one day a too-strict first draft would have
caused churn instead of catching a defect.


## 2026-10-06 — One file per surface, because agents pay for every line

A single search-criteria file had reached 2,207 lines. Under one context that
was awkward; under a sub-agent flow it is a repeated cost, because an agent
sweeping one board loads the whole file to reach the hundred lines that concern
it, and pays again on every agent and every sweep.

It also carried two faults that size alone does not explain. Twenty-one dated
table rows sat in a methodology file, which the contract forbids outright. And
knowledge about a single application vendor was spread across five separate
places in it, because the file was organised by when things were learned rather
than by who needs them.

So it dissolved. Per-board detail became one file per board; application-vendor
detail became one file per vendor, on a separate axis, since finding a job and
applying for one are different questions asked by different readers. A vendor
that is both a job board and an application target gets a file on each axis,
which is deliberate and is written down so a later cleanup does not merge them.
Constraints, lane definitions, board strategy and cross-vendor form rules each
became their own file. The dated rows moved to the data directory.

Files in those per-surface directories are addressed BY NAME, not by routing: a
coordinator hands an agent a surface name and the agent derives the path.
Nothing scans an index to choose one, and the directory listing is the
inventory. The context map collapses each such directory to a single line,
because a dozen near-identical routing entries would drown the skills that are
genuinely routed.

Two new skills support the flow. An agent-contracts skill defines what crosses
the boundary in both directions — the literal return shape per role, errors
inside the object rather than as prose, which skills each role loads, and what
an agent must never do: submit anything, choose what to apply to, or edit a
skill file. A capability change is reported as data and written up later by a
context that knows the repository's standards, because an agent mid-sweep is
not that context and neither is a coordinator in the middle of getting
applications out.

Finally, the header contract is now checked by a script rather than by eye, and
it runs at close rather than on request. Its first version errored on a literal
title prefix and on any routing header over three lines, and would have forced
churn across fifteen files for two things that were not problems. It now errors
only on what breaks the mechanism — a missing routing header, or one below the
scan budget — and warns on the rest, including file size, which is how the next
oversized file announces itself early.

## 2026-10-06 — Screenshots are an architecture problem, not a discipline problem

Browser automation produces screenshots, screenshots accumulate in the
conversation that drives them, and a long session dies of it. The instinct is
to take fewer. That is the wrong lever: the form-filling rules prescribe a
screenshot per field for a real reason, and removing them reintroduces a bug
that scrambled a work-history section once already.

The right lever is where the screenshots land. A sub-agent's working context is
discarded when it returns, so delegating browser work converts a hundred images
into one text report. Measured on a real setup: an agent that drove a browser
through 45 tool calls and 4 screenshots moved its parent by 2.2K tokens against
~149K spent inside it.

The corollary is the part that gets missed, so it is stated outright: routing
content through the parent to hand it to another agent defeats the whole
design. Harvested text goes to disk and the parent passes paths.

Four findings here were paid for in testing rather than reasoned out, and every
one of them fails silently. A file-write tool that does not create parent
directories lets a whole batch of agents work and then lose everything at the
write. A summarising fetch tool erases exactly what scoring depends on while
still returning something that reads like a posting. In a background tab,
simulated clicking and typing fails unreliably rather than cleanly, with the
tool output still reporting success, while a DOM-level set works and survives a
framework re-render. And a sub-agent costs a large fixed amount simply to
start, so batching work per agent matters more than parallelism.

The apply ritual gains the step it never had: decide where the browser work
happens. The agent fills and stops; the human reviews on the live form rather
than on screenshots in a transcript, which is why delegating costs the review
nothing.

## 2026-10-05 — Map a board's title vocabulary before narrowing a query

A query narrowed against the wrong words returns a thin result set that looks
like a thin market. Boards do not share a title vocabulary — the same role is
posted under different words on different surfaces — so narrowing before
learning the local words measures the query rather than the board.

## 2026-10-01 — Delete the mirror, keep the reference

Scripts were enumerated by hand in seven places: a Scripts block in the private
session-init, a transcribed `cp` list in the quickstart, prose lists inside four
directory trees, and a row in the contract. Every one of them was a copy of
something the files already said about themselves, and three were measurably
stale — the session-init block went out of date the day two scripts were added,
the quickstart list still said "the three scripts" when there were five, and the
contract row named two of four.

Skills never had this problem, because nothing enumerates them: a skill's
`Load when:` header is its routing and the generated context map indexes every
one from the files themselves. Scripts now work the same way, keyed on each
script's first docstring line, so the lists had nothing left to justify them
and were removed rather than corrected.

What replaced them is not nothing. The quickstart points at `bootstrap.py`'s
COPIES, which is the authoritative set of files an instance starts with and is
executable rather than descriptive. The trees say that scripts are indexed
rather than listed. The private session-init keeps only what a docstring cannot
carry — the order things run in, and what is non-obvious locally — and dropped
from 63 lines to 38.

The ripple map shrank as a direct result: a script added or changed now names
three obligations instead of six, and it carries the rule explicitly, so the
deleted mirrors are not helpfully recreated later. The general form is worth
stating, because this repo now has three failures of exactly this shape in one
day: **a list inside a document is a mirror, and a mirror rots. Describe what a
generated view contains, never how many things are in it or what they are.**

## 2026-10-01 — The always-loaded file was one directory too low

The instance's `CLAUDE.md` lived inside `private/`. Harnesses that auto-load a
`CLAUDE.md` scan the working directory and its PARENTS, so a session opened at
the repo root never reached it — the file whose entire job is "read this first"
was silently skipped for any session that did not start inside `private/`.
Nothing announced it, and the gap was only visible by noticing that a documented
rule had never been mentioned.

There is now a `CLAUDE.md` at the repo root, and it is deliberately a ROUTER
rather than a manual: the public/private boundary, the one command that starts a
session, how skills and scripts are discovered, and a table of which file owns
what. It carries no skill list, no script list, no counts and no methodology,
because every one of those would be a mirror of something generated or owned
elsewhere. Being public-safe, it ships with the framework, so a fresh clone gets
an agent that can orient itself.

Two related fixes. **Scripts are now discovered the way skills are** — the
generated context map indexes them from each script's first docstring line,
exactly as skills are indexed from their `Load when:` headers, replacing a
hand-maintained list that went stale the day two scripts were added.

**And always-loaded instance files were added to the ripple map**, which had
covered READMEs, trees, the contract, the quickstart and the bootstrap script
but not the one document guaranteed to be read every session. It had gone stale
twice as a result: a hard-coded skill count, and a description of the generated
map that predated the map indexing scripts. The entry says to prefer deleting
the mirror over adding an obligation — describe what a generated view contains,
never how many things are in it.

## 2026-10-01 — Rules that argue with an absent file

The instance's always-loaded file opened by arguing against a file in an
ancestor directory: it named that file, described what it was for, and framed
this project's own rules as exceptions to it. That file belongs to unrelated
work, is not guaranteed to exist in future, and will not exist at all for
anyone else who clones the framework.

Rules written as rebuttals degrade badly when the thing they rebut disappears:
what remains is a reader being argued out of a position nobody holds, with the
actual rule never stated plainly. So the rules are now stated positively and
unconditionally, and the ancestor case is a short clause underneath. The clause
keeps the one thing worth knowing — a rule that is correct in another project
can be actively harmful here, since a blanket "do not commit" would disable
this framework's entire recovery path.

## 2026-10-01 — Check for a connection at vet time, and rank it by who would vouch

Whether anyone you know works at a company is cheap to check and changes what
you do next, but it had been checked twice in several hundred logged roles,
both on the same day, and never again. It is now a step in the vetting ritual
with a fixed note convention, so the answer is recorded either way — recording
"none" matters as much as recording a hit, or nothing distinguishes a company
that was checked from one nobody looked at.

The guardrail is the part worth stating, because it is counterintuitive and it
comes from outcomes rather than instinct. **Degree of connection is not the
signal.** On one real search, every human-sourced interview came from someone
who knew the candidate BEFORE the search began — a community they belonged to,
a former manager, a recruiter who had placed them — and no connection made
during the search produced an interview across two cohorts and two months.
Meanwhile a nominal second-degree link turned out to be hollow: the mutual had
no idea who the person was.

The cold half of the tactic has a measured record, and it is 0 for 12. Thirteen
applications went out with a message attached to someone at the company; one
advanced, and that one was not cold — the recipient already knew the candidate
and had sent him the posting. Nine of the twelve failures were messages to
recruiters rather than to engineers on the team, which is the one variant that
remains untested rather than disproven. Negative results are the ones that get
lost and re-tried, which is why this is recorded with its denominator.

## 2026-10-01 — A sweep that claims rows it did not find

The sweep recorder matched rows on board name with no bound, so closing a sweep
claimed every previously-unattributed row for that board rather than the ones
the sweep actually produced. On one real tracker the next close would have
claimed 44 old rows, inflating that sweep's yield eightfold and mis-dating the
rest — corrupting the one measurement the ledger exists to produce, silently,
on first use.

`start` now snapshots the existing rows and `end` claims only the difference. A
row that was already present belongs to whatever found it first; this sweep
re-encountering it is a collision, and collisions belong in the already-known
count rather than in yield.

Rows whose board is known but whose sweep is not carry a reserved
`<board>-unknown` label instead of a blank, and readers exclude it from
per-sweep rates — counting it would attribute rows to a sweep that has no
screened count, which is the same error as judging a board on volume.

## 2026-10-01 — A rejection erased the interview that preceded it

The funnel computed `advance` from a row's current status. So the moment an
advance ended in a rejection the row became `declined_by_them` and the advance
disappeared — every screen and interview that did not become an offer erased
itself, and the metric decayed toward zero exactly as a search progressed,
deepest results first. On one real tracker it reported two advances where six
had happened. The defect was documented in the morning and fired the same
afternoon: a completed five-round final was declined, and the only
direct-to-employer advance on record vanished from the measurement on the day
it concluded.

The same gap made rejections unreadable. A rejection at the résumé screen and
a rejection after a full interview loop carried the same status and diagnose
opposite problems — one says the resume is not getting you into the room, the
other says the room is not converting. 92% versus 8% of rejections, pooled
into one number.

`peak_stage` records the furthest stage an application ever reached. Outcome
and depth are orthogonal, which is why it is a column rather than a new status
value: a `declined_after_interview` enum entry would conflate them and force a
migration of every existing rejection. It ratchets upward automatically from
`application_status` at `close`, so nothing is hand-maintained — edit the
status exactly as before. Lowering it takes a deliberate hand edit, because
silently losing a high-water mark is the bug it exists to prevent.

**Deriving it on read was tried first and does not work**, which is worth
recording so it is not retried. Notes prose says "interview" about automated
video screeners, scheduling mail, interview prep, and negations like "never
interviewed" — on one tracker that heuristic produced two false positives out
of three hits, both of them automated submission-time video screens. A walk of
version-control history has better precision but keys on company plus title,
which changes when a row is retitled mid-process, and then counts one
application as two. Both sources were run and reconciled by hand for the
backfill; neither is sound as a standing derivation.

The report now also prints the share of submissions that ever produced a
conversation at all — 4% against a 45% response rate, since a rejection counts
as a response.

## 2026-10-01 — Measure the cost of a search, not just its output

The tracker recorded what every sweep produced and never what it cost, so a
board could only be judged on raw volume. "167 listings from LinkedIn" could
be three sweeps or thirty, and nothing distinguished them.

Two things forced the issue. First, the hand-maintained sweep log had died
twice — by the end of September it showed two boards last swept in July that
had both been swept that week, so the one question it existed to answer could
not be answered from it. Second, an audit found that the downstream metrics
being used to rank boards could not carry the weight: per-board submission
counts sit around twenty, where a single reply moves a response rate five
points, and the strongest-looking channel in one real tracker turned out to be
thirteen applications to one employer whose ATS answers everything. Strip that
company out and the channel fell from 86% to 62% on a sample of eight.

So the metrics got reassigned to the questions they can actually answer.
**Boards are judged on yield and precision per sweep. Response and advance
rates measure the resume and the positioning, and only hold up globally.**

`scripts/sweep.py` makes a sweep a first-class record — `start` before the
board opens, `end` in the same sitting — and writes `data/sweeps.csv`. It
captures three numbers that do not survive closing the browser tab: how many
listings were screened (the tracker keeps only survivors), how many of those
were already tracked, and roughly how long it took. The second one matters
more than it looks: without it, whichever board gets swept first banks all the
overlap between boards and looks strongest for reasons unrelated to its
quality.

Four tracker columns were added. `sweep_id` ties a row to the effort that
found it. `tech_fit` holds the match score, and `hard_reqs` /
`tech_named_reqs` hold the requirement count that makes the score readable — a
vague posting scores high precisely because it asks for little that can be
missed, so the score and its denominator travel together or a raw sort floats
artifacts to the top.

`scripts/backlog.py` answers the question those columns exist for: what
cleared the scoring bar and never got applied to. These are not rejections.
A stack rank gets worked top-down, the day ends, and whatever sat below the
waterline stays `researching` indefinitely. The daily-log tool prints the
count at `open`, alongside a warning for a sweep left open overnight — a
forgotten sweep is a permanent data loss, not an untidiness.

**One defect is documented rather than fixed.** The funnel report computes
`advance` from a row's current status, so an advance that ends in a rejection
erases itself and the metric decays toward zero as a search progresses. On one
real tracker, git history recovered six advances where the report showed two —
and inverted the conclusion, since four of the six came from warm channels
that were 5% of submissions. Fixing it needs a monotonic high-water-mark
column; until then the skill says not to read per-source advance rates off the
report.

## 2026-09-18 — Separate the checkpoint from the end of the day

The daily-log tool's `close` carried two meanings at once: "save a recovery
point" and "the day is over." That was fine until the checkpoint discipline
started asking for frequent mid-session closes, and the weekly review became
anchored to a weekday's close. Then the two meanings collided. On any due
Friday the FIRST mid-session checkpoint would run the funnel report and stamp
the weekly review — but the review is only half script. Its sweeps (outreach
age, snapshot as-of dates, passed open-thread dates) are in-session judgment
work, and those hadn't happened. Worse than a merely premature stamp: a stamped
ritual stops announcing itself at `open`, so the skipped half goes silent
instead of resurfacing.

Added `close --mid-day`, which does the same fold, archive, regenerate and
amend but never runs a dated ritual, and prints what it skipped and why. Bare
`close` is unchanged and remains the only form that can run and stamp the
weekly review. The flag is named for its intent rather than for the feature it
suppresses, because it is typed far more often than the bare command.

The general rule, now in `session-continuity.md`: if one verb means both
"checkpoint" and "end of day," every end-of-day-only step riding on that verb
fires on the first checkpoint instead. Give the checkpoint its own command.

## 2026-09-16 — A ritual for the stage after submission

The runbook covered finding roles, applying to them, and the weekly pass over
everything at once. It had nothing for the moment an application actually
moves, which is the moment the per-company brief stops being a record and
starts being the document someone reads minutes before a call. Two costs came
out of that gap. Briefs written before a template revision stayed on the old
shape indefinitely, because "migrate it on touch" was advice sitting inside the
call-prep skill rather than a step in an ordered list, and the touch that would
have triggered it was always the touch that was in a hurry. And a templated
recruiting email describing a loop one way was liable to quietly overwrite a
more specific account a person had given earlier.

Added a continuation ritual: migrate the brief to the current template first
and in full, fold new facts into the sections that own them, update the tracker
row, record what is owed in the open-threads file, and reconcile rather than
overwrite when a generic message contradicts a specific one. The call-prep
skills now point at it instead of carrying the migration rule as a footnote.

## 2026-09-14 — A status for the most common outcome, which had none

Sweeping every submitted-but-silent application for whether its posting was
still up turned a pile of silence into information: a meaningful share of the
reqs were simply gone, some within a week of the application going in. None of
the existing statuses could say that. Leaving those rows at `applied`
overstated how much was genuinely pending, which is the number a search is
steered by; moving them to `skipped` would have erased real submissions from
the funnel's denominator and flattered every rate in the report; and
`declined_by_them` would have invented rejections that never happened.

Added `closed_no_response` — applied, posting later came down, no reply ever
arrived. It counts as a submission, not as a response, not as an advance, and
it moves the row out of the active list where it was misrepresenting the
pipeline. The readers were updated together so neither silently mis-bucketed
it, and the full status vocabulary was written into the application-tracking
skill, because it had been re-derived from memory more than once and come back
short — once badly enough that a live interview sat at `applied` while the
weekly funnel reported zero advances.

One guard rail came with it: set the status only on positive evidence that a
posting is gone (a 404, an explicit closure message, an ATS error redirect, an
HTTP 410). A page that was merely unreachable, robots-blocked, or rendered as a
JavaScript shell proves nothing, and treating those as closures would erase the
very distinction the status was added to draw.

The same sweep exposed the opposite failure and the guard rail grew a second
half. A stored requisition URL was fetched, returned HTTP 200 with a page full
of real job listings, and was recorded live — but the ATS had silently
redirected a dead requisition to the company's board index with an error flag
in the query string, and the role was gone. Status codes and page content both
said live; only the landing URL said otherwise. So the rule is now to read the
URL you ended up on: if the requisition ID has fallen out of it, or it resolves
to a board index or search page, the requisition is closed. Its mirror image is
recorded alongside it, because a repost gives a live role a new ID and a dead
stored URL, which fails in the other direction.

## 2026-08-19 — Define the checkpoint trigger, or it never fires

The continuity rule said to take a local commit "after each meaningful batch of
edits." The mechanism was right — amend one commit through the day, push once at
close, so every checkpoint is a recovery point — but the trigger was a judgment
call, and this one resolves the same way every time. A session ran four discrete
units of work (a record logged, a new channel evaluated, a decomposition of an
oversized methodology file, a change to this framework) and took exactly one
checkpoint, at the very end. None of the four was individually easy to call
"meaningful," so hours of edits sat unrecoverable while a defined rule sat in the
file saying otherwise.

The replacement trigger is reporting. When you are about to tell the person what
you found or did, the edits behind that statement are a finished unit — so
checkpoint first, then report. That boundary needs no interpretation, and it
cannot be quietly deferred the way "meaningful" can, because reporting is
unavoidable. Two secondary triggers cover the rest: something expensive to
reproduce has landed, or the next thing is a different concern entirely.

One exception, stated as the only one, because a vague rule invites new ones:
never checkpoint a knowingly inconsistent state. A half-mirrored change — content
moved out of one file but not yet into its counterpart, a component added before
its ripple is walked, a data edit whose generated view is stale — commits a
contradiction, and that recovery point is worse than none, since reverting to it
restores something broken. Finish the pair first.

The general shape is worth naming beyond this rule: a process step whose trigger
is an adjective will be skipped by anyone who has a reason to keep working, and
they will always have one. Triggers should be events, not thresholds.

## 2026-08-19 — Evaluating a board is a go/no-go, not a sweep

A new board got a first-pass evaluation that ran 55 minutes across 122 tool
calls: ~238 result cards read, ~35 individual job-detail pages opened. The
verdict it produced was correct and the work was competent. It was also mostly
waste — the decision had been determined by four facts visible in the first few
minutes, and not one of those 35 detail pages contributed to it.

The cause was not a missing checklist. It was one task asked to answer two
different questions: "is this channel worth returning to" and "what is in it
right now." The first is answered by a handful of aggregate, card-level
measurements — how big the relevant pool actually is, how much of it is one
poster, how far back the tail runs, how often comp is posted, and whether the
listings are original or mirrored from somewhere already in the rotation. The
second is answered per-listing and costs an order of magnitude more. With no
gate between them, the expensive one runs unconditionally.

So the ritual file now opens with a board-evaluation runbook: the five
measurements, an explicit NO-GO / CONDITIONAL / GO gate that must be passed
before any per-listing work, and a rough quarter-hour budget for reaching it.
CONDITIONAL is there because an unqualified "keep" silently becomes a weekly
obligation, and a documented no is a real deliverable — it stops the same board
being re-evaluated from scratch two months later.

Two smaller notes came out of the same session. The sweep step already said
"sweep and vet are different modes, and mixing them makes both worse"; this is
that rule one level up, which is a fair sign that a principle stated at one
scale is worth checking at the next. And when the work is delegated, the gate
has to be written into the brief — a competent worker handed a three-part brief
completes all three parts well, so the judgment about whether to spend an hour
belongs to whoever writes the brief, not to whoever executes it.

## 2026-08-18 — Init ends by reporting, and does not start the work

The session entry point had a final step that read "ask which thread," and in
practice that turned into a multiple-choice prompt at the end of every startup:
here are four things I think you might want, pick one. It reads as helpful and
isn't. It makes the assistant's guess at the shape of the day the frame the
person has to answer inside, and the thread they actually wanted is usually the
one that wasn't listed. So step 8 is now "report what init found, then wait" —
options offered as sentences, and the person answers in their own words.

The same session surfaced the sharper version of the problem. A `data/` file
described a board watch as a "daily, session-start" check, so init ran it: a
browser connect check, a full board render, and a page of findings, all before
the person had said what the day was for. The finding happened to be real, which
is exactly what makes the habit hard to see as a cost. Init is read-only
orientation now, explicitly: sweeps, scoring, submissions, outreach, and standing
watches wait to be asked for, and a "daily" cadence in a data file means "due the
next time the process runs," not "run on arrival." Surfacing that something is due
is the deliverable.

Also added to the checklist: read the persistent context store at startup when
the assistant has access to it. It had been treated as a delivery mechanism that
hands over the map file and nothing more, which is the same underestimation the
8/13 entry below corrected for writes.

## 2026-08-13 — Refreshing the persistent copy is the assistant's job, and it goes last

The session-init file is designed to be loaded once into a persistent context
store rather than re-read every session, which is what makes it cheap. The cost
is a second copy that goes stale the moment the file changes, so the ripple map
has long said to refresh it. What it didn't say is who does it, and the default
assumption — that a human re-uploads it — turned out to be wrong in at least one
setup, where the store was writable through a tool that had been available the
whole time. Months of handing back a manual step that never needed to be manual.

So the entry now says the assistant does it whenever the store is writable, and
only falls back to asking when it genuinely isn't — in which case it has to be
named as an outstanding step rather than quietly assumed.

The more interesting half is ordering. Refreshing the copy as soon as the file
is saved feels right and is wrong: any later edit in the same batch can
invalidate a line in it, including an edit to a completely different file. That
happened here — a `.gitignore` change falsified a sentence in the map minutes
after a correct copy had been uploaded. The ripple therefore fires at the end of
the batch, after the last change that could touch the file, and any
"copy refreshed" stamp waits for that final verified upload. Verified meaning
read back, like any other write.

## 2026-08-13 — One log heading per day, because checkpoint closes fragment it

The close step is deliberately not just an end-of-day ritual: running it at
every meaningful batch of edits is what makes each checkpoint a recovery point,
and because it amends, doing so costs nothing in commit noise. The fold didn't
match that design. It inserted a fresh `## Session Notes (date)` heading above
the newest entry every time it ran, so a day with four checkpoints produced
four headings carrying the same date.

That isn't only untidy. Session start is contracted to read the top entry of
the log for recent context, and with the day split across several headings the
top one holds whatever happened in the last twenty minutes rather than the
day's arc. Worse, the fragments read as separate days to anyone scanning, which
is exactly the confusion the newest-first ordering exists to prevent.

The fold now checks whether the newest entry already carries today's date and,
if so, appends into it rather than repeating the heading. Within a day that
leaves entries in the order they were recorded; across days the log stays
newest-first. Existing runs of repeated same-date headings collapse cleanly,
since the old behaviour always prepended and therefore always left them
contiguous — the redundant heading is removable without moving any content, so
no note that refers to something "earlier today" can be invalidated by the
cleanup.

## 2026-08-13 — Name the working file's full path, because a decoy swallows days

Every tool here resolves its paths from its own location, so they all read and
write under `private/` regardless of the directory you invoke them from. The
docs, though, wrote the day's working file as `temp/today.md`. Read from the
repo root that names a different directory — and if one exists there, notes
written to it are accepted in silence. Both are gitignored, so there is no
error, no dirty status, nothing missing. The close step folds nothing and the
day is simply absent from the log, discoverable only when someone later
notices a gap.

That happened twice before it was traced. The second time it also produced a
confident wrong diagnosis: the close step does skip folding a working file
that holds nothing but its header, so that looked like the cause, and the
conclusion drawn was that the notes had gone into other files. They hadn't.
They were sitting intact at a path no tool reads. The header-only file was the
downstream symptom.

Four fixes, in increasing order of how much they actually help. Every path
reference in the docs and templates now reads `private/temp/...`, with a
warning that a root-level `temp/` is a trap and an instruction to check the
working file has content beyond its header before closing. The daily-log tool's
own output stopped printing the ambiguous form: it was rendering the path
relative to `private/`, so every open, status, and close taught the wrong path
to whoever read it — documentation that contradicts tool output loses, because
the tool is what people copy.

Those two only help someone who reads. The other two fail loudly instead. The
daily-log tool now checks for a root-level `temp/today.md` at open, status, and
close, and says plainly that nothing reads it and the work will be missing from
the log — the close check runs before the fold, which is the last moment the
notes can be rescued. And `/temp/` came out of the root `.gitignore`. It was
ignored for symmetry with `/private/` and `/output/`, but bootstrap creates
`temp/` under `private/`, so a root-level one is never legitimate. Ignoring it
was the reason a stray directory full of a day's work never appeared in `git
status`.

The general shape is worth stating. When a wrong path silently succeeds, the
failure is invisible by construction, and writing the correct path in prose
does not fix it — that was tried, and the second occurrence followed the first
by a month. Delete the decoy if it isn't sanctioned, make the tool print the
unambiguous path every time it runs, and add a check that names the mistake out
loud. Prose is the weakest of the four.

## 2026-08-13 — Two kinds of resume mirror, and each check where it fires

The platform-copies idea started from a file problem: an ATS auto-attached a
cached stale PDF to live applications. So the rule became "a release walks the
inventory of every platform storing a copy." Two things were wrong with that.

It missed the copies most people actually read. A professional-network
profile's own experience section and a personal site listed on applications are
retyped prose, not uploaded files, so they drift differently: not merely stale,
but contradictory on facts. A release that re-dates an employment range, and
then walks only the stored files, ships a profile that disagrees with the
resume about where the candidate works and when. Nothing will prompt that fix,
because there's no submit event to hang a check on.

And for the stored files it was the wrong moment. A stale stored file can only
do damage when something is submitted through that system, so the release now
just marks those stale in the inventory and the refresh lands in the apply
ritual, at submit time, for the one system in play. Walking every ATS on
release day spends effort on systems the search may never touch again, and the
effort expires the next time the resume changes.

So the release section of the search-apply ritual splits the inventory in two
and sends each half to the moment where its check actually fires, apply-ritual
step 2 refreshes the stored copy rather than only verifying it, and the ripple
map records the distinction. One addition from practice: check the field's
character limit before drafting a content mirror. A capped field makes a
release a selection problem rather than an append, and finding that out after
the copy is written wastes the draft.

## 2026-08-13 — The tracker's column-shift bug fails loudly now

A single unquoted comma inside a tracker field shifts every column after it,
and the last columns are the analysis ones — `source`, `lane`,
`resume_version`, `notes`, `found_via`. The row still parses, the views still
render, and the funnel report still prints a resume-version split built from
fields reading their neighbors' values. This was found, repaired by hand, and
then found again weeks later on eight fresh rows, because the repair shipped
without a guard: the history generator reported "0 unrecognized" the whole
time, since it tolerated the shape rather than validating it.

`build_history.py` now counts fields against the header on every row and
exits without generating anything if any row disagrees, naming the line
number, the field count, and the organization and role so the row is findable
without a diff. `funnel_report.py` imports the same loader instead of doing
its own `DictReader` pass — a guard that only one of two readers honors is a
guard that gets routed around. The application-tracking skill gained the
reasoning, so the failure is legible at the moment it fires rather than only
in the script.

## 2026-07-17 — A skills ledger under the resume, so match/gap stops guessing

Match/gap reads kept getting a candidate's own stack wrong — a language flagged
as a gap when it was a decade of tooling, a database counted as a match when the
real engine was a different one under a shared brand name. The facts were correct
in the experience summary; the judgment step just wasn't consulting them, running
off recall instead.

So the resume content file now carries a two-layer skills ledger. `skills` became
a group → item → children tree where each node can hold `depth`, `years`, and the
`canonical` spelling listings use; a sibling `context_ledger` records off-resume
technologies as evaluated-not-adopted, honest-gap, or tooling-only. The renderer
prints names only and drops every tag, so the resume is unchanged (verified
byte-for-byte across both lanes before the swap). The match/gap step in the search
ritual now resolves every JD term against both layers rather than from memory, and
the maintenance ripple map gained an entry so a future schema change touches the
renderer, template, CONTRACT, the resume-strategy skill, and the vetting rule
together.

## 2026-07-17 — The weekly review, anchored to Friday's close

The weekly pipeline review used to ride a rolling seven-day timer, so it drifted
to whatever weekday it last happened to run. It's now weekday-anchored: a ritual
in the stamps file can carry `anchor: <weekday>`, and the weekly review uses
`anchor: friday`. It comes due every Friday and stays due if a Friday is missed,
so a skipped week surfaces at the next `open` instead of resetting the clock.

Running `close` on a due Friday now performs the measurable half of the review:
it runs the funnel report, writes it to `data/funnel_report.md`, stamps the
ritual, and makes its own `weekly-review: <date>` commit — kept separate from
the daily `log:` commit so the week's measurement is its own event in history.
The judgment steps (staleness sweeps, the passed-date scan) stay in-session,
done before the close.

## 2026-07-16 — Public-to-private handoff prompt, and a template close ritual

Two follow-ons to the first-session parity work. The template's end-of-session
guidance was one thin sentence while the mature private map has a full close
ritual, so the template now carries it: rewrite the open-threads file so the
next startup reads truth, promote durable learnings into a skill file, and run
the daily-log `close` (or update the log by hand). It stops short of
prescribing optional files (`companies/`, outreach queues, rituals) a new user
may not have. And the public-to-private transition is now prompted explicitly:
`SESSION_INIT.md` spells out that the private map is generated from the
template by bootstrap, must be personalized, and supersedes the generic
checklist permanently from the next session on; `bootstrap.py`'s next-steps
names personalizing it.

## 2026-07-16 — First-session parity with long-term usage

The context-map/ripple discipline — and, further back, reading current state
at startup — had landed in the mature private session-init checklist but not
in the two first-time entry points: the public `SESSION_INIT.md` generic
fallback and the `templates/session_init.md` a new instance inherits. A
first-time user would have silently skipped checks that long-term usage
treats as mandatory. Both were brought to parity with the mature checklist:
read current state (open threads + session log) before acting; regenerate and
read the context map, and consult its ripple section before editing any
framework or root-doc file; and route skills through `framework/README.md`.
The generic fallback calls `build_context_map.py` directly (it assumes no
installed tooling); the template uses the daily-log tool's `open` when present
and falls back to the script otherwise.

## 2026-07-16 — The context map: routing generated at load, not remembered

The template-honesty change below shipped without its documentation ripples
— the CHANGELOG, QUICKSTART, and bootstrap updates got caught only when
asked about explicitly. The cause wasn't a bad skill header; it was trigger
timing. The Load-when scan that routes tasks to skills is a session-start
ritual, but framework edits arrive mid-session as a pivot, and nothing
re-invoked the scan at the moment of the edit. The map existed; nobody
opened it.

Fix: stop relying on remembering to scan. `build_context_map.py` now runs
from `daily_log.py open` at every session start and materializes
`private/temp/context_map.md` — every skill's Load-when header (routing)
plus the ripple map, lifted verbatim from `framework-maintenance.md`. It's
generated, gitignored, and rebuilt each session, so it can't drift: a view,
never a source. The point is that "what to touch when" sits in context from
the first moment, so a mid-session pivot into a framework edit already has
the ripple obligations in front of it. The generator extracts rather than
re-encodes — skill headers and the ripple-map section stay the single
sources of truth — so the only new coupling is the section heading the
extractor keys off, which fails loudly (empty section) if renamed.

Per the ripple map, adding the script also touched the scripts lines in the
README, SESSION_INIT, and framework/README trees; the private session-init
map's checklist and scripts block; CONTRACT's generated-files table; and
session-continuity. Dogfooded: the map was run against its own change.

## 2026-07-16 — Template honesty, and a shape for feedback docs

A documentation audit caught the root README claiming `templates/` held
"blank versions of every file private/ needs." The framework deliberately
templates only files with a canonical *shape*: state files (session log,
open threads) start empty, and generated views (application history, build
record) come from scripts — three buckets, not one. `CONTRACT.md` already
sorted the files correctly; only the summary had drifted. Two fixes:

- **Wording aligned to the design.** The root README's templates line now
  names the three buckets instead of implying a template per file, and
  `framework/README.md`'s templates entry reads "every file type that has
  one."
- **A feedback template, optional by design.** `framework/templates/feedback.md`
  gives feedback docs a canonical shape — a free-text record of the feedback
  plus an actionable takeaways list — without requiring any to exist. Like
  the per-company brief, it's an on-demand template: created when feedback
  actually arrives, not instantiated at bootstrap, so `bootstrap.py`'s COPIES
  list is deliberately left untouched. QUICKSTART and CONTRACT note where the
  shape lives.

## 2026-07-10 — Discovery-point tracking in the funnel

The tracker's `source` column answers "which channel"; it can't answer
"which specific place keeps turning up roles worth applying to" — a board
listing URL, a saved search, a person. New `found_via` column (URL
preferred, short text allowed, blank when it would only repeat `source`),
added per the standing schema rule: columns are added, never renamed, and
readers treat absent as blank. The funnel report gains a discovery-point
split, grouping URL values by domain so the report measures places rather
than fragmenting into one-row groups. The application-tracking skill now
lists four analysis columns to fill at log time.

## 2026-07-10 — The public half got its own index

Earned by a real failure: a per-company call brief was regenerated without
its template because nothing at task time routed to `framework/templates/`
— the directory existed only as a path inside one grep command, and the
skills that govern brief-writing never named it. Three fixes, each at the
layer that failed:

- **`framework/README.md`** — a small routing index of the public half
  (skills, templates, scripts, contract; what each is and when to read
  it). A private instance's session init points here once; new skills and
  templates announce themselves by adding a README line in the same commit
  that adds them, so the always-loaded private map never needs editing to
  keep discovery working.
- **Templates rule** stated where it's discoverable: before creating any
  new file, check `templates/` — if a template exists, the file is created
  from it and keeps its sections through later edits. The screen-prep
  skill now names `templates/company_brief.md` directly, and the
  session-init template routes new instances through the README.
- **Ripple map updated** in the maintenance skill: layout changes, new
  templates, and script changes now list `framework/README.md` among the
  mirrors to touch.

## 2026-07-09 — Drift prevention, the data layer, and working tooling

A full-system review found the framework's own instance violating several of
its own rules: a canonical config file that had drifted behind a decided
policy, a scrubbed claim surviving inside a skill file's example, dated
market data embedded in a methodology file, and a hand-maintained mirror of
the application tracker that had already broken once and needed
reconstruction. Every fix became a rule, and most rules became structure:

- **Data layer.** The private contract now separates working state
  (`data/`: session log, an open-threads file read first every session,
  dated snapshots, per-company call briefs) from methodology (`skills/`),
  with the rule that a methodology file never carries an "as of" fact.
- **Generated views.** The tracker CSV is the single hand-edited
  application record; the human-readable history is rendered from it by
  script. Mirror drift is now structurally impossible rather than
  procedurally discouraged.
- **Drift-prevention rules** added to the session-continuity skill: policy
  changes land in canonical files the same session they're decided;
  scrubbing an overclaim means searching the entire private instance,
  including examples inside skill files; dated content lives only in the
  data layer.
- **One commit per day.** A daily-log tool folds the day's working notes
  into the log, archives old entries, regenerates views, and amends a
  single dated commit until it's pushed.
- **Communications skills.** Warm outreach (sequencing, queue pattern,
  raising gates in conversation rather than on forms) and screen-call prep
  (the per-company brief) — the post-application half of the funnel the
  framework previously didn't cover, added as the instance's own pipeline
  reached that stage.
- **A measured funnel.** New tracker columns (source, lane, resume version)
  and a report script turning them into response and advance rates, split
  by each.
- **Generalized resume builder.** The two per-lane build scripts turned out
  to be identical layout code with different content baked in; they became
  one layout-only renderer driven by a YAML content file, verified
  output-identical before the swap. A positioning-strategy change is now a
  data edit. This closed the framework's oldest known limitation.
- **Onboarding and display.** QUICKSTART rewritten for the new layout with
  a tooling copy step; README gained the state-vs-methodology and
  measured-funnel design ideas, an explicit two-stage session-init
  lifecycle, and a work-sample section; the private instance documented a
  full run-it-by-hand fallback.
- **Maintenance became a skill.** The framework describes itself in seven
  places, and self-description drifts like any other mirror — so the
  ripple map (when X changes, also touch Y, including the bootstrap
  script's deliberate layout duplication), the change workflow (fidelity
  gates, migration backups, boundary checks), and two closing audits now
  live in `framework/skills/framework-maintenance.md`. It also sets the
  skill header contract: complete routing information in the first 8 lines
  of every skill, Load-when at most 3 lines, so one grep scans every
  skill's purpose in a single call.
- **The pipeline's rituals got runbooks.** Session boundaries (init and
  end-of-day) live in the private session map; the search and apply
  sequences live in a new ordered runbook skill that sequences the other
  skills by pointer rather than copying their content — including the
  verify-what-the-ATS-actually-attached step, earned when a platform
  auto-attached a cached stale resume. Non-daily rituals get machine-
  checked stamps: the daily-log tool records last-run dates and warns at
  session start when a cadence has elapsed, and the resume renderer
  writes a build record (timestamp plus content hash) so platform-copy
  staleness is a mechanical compare instead of an act of memory.

## 2026-07-06 — Published

Pre-publication audit of every public file for personal-data leakage
(nothing found; the config-separation rule did its job), then announced
publicly with the repository linked. No code changes — the boundary held
without needing any.

## 2026-07-01 — Extraction

The framework's first public form, extracted from a private methodology that
had grown across several weeks of real search sessions: repository layout
and the public/private split, the session-init startup sequence, the single
methodology file decomposed into small on-demand skills, blank templates for
every private file, the quickstart including the adversarial
experience-summary generation process, the two-lane search reframing, and
the stable-map versus dynamic-log separation with the public init checking
for and loading a private counterpart. Ten commits in one day because the
patterns already existed — the work was separating the reusable system from
one person's data.
