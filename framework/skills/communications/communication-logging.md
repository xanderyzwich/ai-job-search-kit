# Skill: Logging a Communication

**Load when:** any communication lands or goes out about a role or a contact —
an email, a DM, a text, a recruiter relay, a form rejection, a scheduling
invite, a call you just finished.

**Pairs with:** `application-tracking.md` (the tracker schema and status
vocabulary), `screen-prep.md` (preparing for and debriefing a call),
`warm-outreach.md` (whether to send something at all). **This file covers only
what happens to the RECORD once a communication exists.**

---

## Why this is its own skill

**"I have some comms to log" is one of the most frequent things a search
session starts with, and it had no procedure.** Each one was handled ad hoc,
which is how two expensive failures happened in a single week — both of them
cases where the tracker was updated correctly and a file that mirrors it was
not.

A communication is the **only** thing that changes the state of a thread.
Applications do not advance on their own. So this is the moment the whole
record either stays true or starts drifting.

## READ THE PRIMARY FILE FIRST — before replying, before logging

**A communication cannot be understood, answered, or recorded correctly without
the state it arrives into.** Load the primary file for that conversation BEFORE
doing anything with the message.

**Which file is primary follows the ownership rule below:**

| the communication is from | primary file |
|---|---|
| a person whose value spans employers, or none | **their contact record** |
| someone who IS the employer — a hiring manager, an ATS, an internal recruiter | **that company's brief** |
| a recruiter about a specific requisition | **both** — the brief for the role, the record for the person |

**The frontmatter is the cheap read and usually enough**: `owed_by`,
`last_contact`, `next_action` tell you in one glance whose move it was. **The
log tells you why**, and you need that whenever the message is ambiguous, cold,
or surprising.

### The three failures this prevents, all observed in a single day

**1. Answering a question nobody asked.** A contact offered roles on *her own
project*, unposted. The reply discussed a *posted* role found on the company
site. She corrected it politely and re-offered — and the re-offer then sat
unanswered for six days. **Re-reading her actual message before replying would
have cost ten seconds.**

**2. "Correcting" a record that was already right.** An existing entry recorded
a contact's employer accurately. A new session researched him from scratch,
found stale third-party profiles, and overwrote the correct entry with a wrong
one — then had to be corrected back by the person who knew. **The existing file
was the better source and was never opened.**

**3. Nearly inventing an obligation.** A thread had just been closed by someone
who had already been thanked and whose stated etiquette is no follow-up push.
Without reading his record first, the instinct was to log an action owed to him.
**That is the mirror image of the failure that cost a six-month contract** — one
direction invents a wait, the other invents a debt, and both come from writing
without reading.

### Writing in light of what is there

**A new entry has to be consistent with the file it joins, or explicitly say it
is not.**

- **If it agrees, do not restate it.** Add what is new; the history is already
  written.
- **If it contradicts, say so in the entry**, with the date of the thing being
  superseded. **A silent overwrite destroys the provenance that makes the record
  trustworthy** — and the next reader cannot tell a correction from a
  disagreement.
- **If it changes the direction of who owes whom, update the frontmatter in the
  SAME EDIT**, not just the log. A log that says one thing while the summary
  above it says another is the file arguing with itself, and the summary is what
  gets read.

## The fan-out, and it is ONE EDIT

**A state change goes into every file that carries it, in the same edit.** Not
"later", not "at close", not in the next session.

| file | what it holds | when it changes |
|---|---|---|
| `job_tracker.csv` | status, dates, the full reasoning | **always** |
| `open_threads.md` §1 | that the thread exists and what is live | any thread that is live, newly live, or just closed |
| the primary file's `## Scheduled` block | **every live commitment and deadline, one line each** | a meeting booked, moved or cancelled; a deadline set, met or missed |
| `open_threads.md` §3 | a date belonging to NO person and NO company | a renewal, a lapse, a market window — **never an interview** |
| `pending_outreach.md` | **who owes whom, right now** | any change in direction |
| `data/companies/<name>.md` | the readable brief | anything a human would need before the next conversation |

**A row that disagrees with the tracker is worse than no row, because it gets
believed.**

## ONE OWNER PER FACT — the fan-out is slices, not copies

**The table above lists five files. That is five chances to write the same
paragraph five times, and a fact stored five times is a fact that will disagree
with itself within a month.** The point of the fan-out is that each file holds a
DIFFERENT SLICE of the same event, not the same slice repeated.

| fact | lives in | everywhere else |
|---|---|---|
| the **reasoning trail** on a role — how it scored, what the apply pass found, what was decided and when | **the tracker row** | a pointer |
| the **current structured state** of an APPLIED-TO role — status, comp, match and gap, talking points, interview notes | **the company brief's role block** | a pointer |
| the person — what they did, said, offered; what they are owed | **the contact record's log** | a pointer |
| a **booked commitment or a hard deadline** — when, with whom, which stage | **the `## Scheduled` block** on whichever file is primary | a pointer |
| what is open right now | **the open-items file** | one line and a link |
| who owes whom | **`owed_by` plus the outreach queue** | — |
| the narrative of the day | **the session log** | — |

### The tracker and the company brief are not duplicates — they are read differently

**Both hold role facts and that is correct.** The distinction is what each is
for, and it matches how each file already behaves:

- **The tracker row APPENDS.** It is the chronological reasoning trail, it is
  long, and it is **machine-read** — the funnel, the backlog check and the
  scoring all consume it. Nobody opens it before a phone call.
- **The company brief FOLDS.** Its role block is the **current** structured
  state — location, salary, the tracker's literal status token with a date,
  tech fit, the Match and Gap lists split required/preferred, talking points,
  interview notes. **It is what a human opens with ten minutes to go**, and old
  states are folded away rather than stacked up.

**So a role under discussion needs BOTH, and neither is the other's mirror.**
What the brief must not become is a retelling of the tracker's narrative — it
carries the state, not the history of how that state was reached.

**THE BOUNDARY IS ALREADY SET BY `framework/templates/company_brief.md` AND IT
IS A REAL ONE: only roles that have actually been APPLIED TO enter a brief, and
a role arrives in the same edit that sets its tracker status to applied.**
Before that it is a tracker row, its score lives in the stack-rank file, and its
reasoning lives in the session log. **A brief full of roles nobody applied to is
a brief nobody can read under time pressure**, which defeats the only thing it
is for.

**THE TEST, and it is one question: would deleting this sentence from HERE lose
anything that cannot be recovered from its owner?** If the answer is no, delete
it and link instead. **A mirror that duplicates its source does not stay a
mirror; it becomes a second, competing source.**

### When one communication is both a role event and a relationship event

**This is the common case and it is where the duplication happens.** A recruiter
relaying a decline is simultaneously news about a requisition and news about a
person.

**Split it rather than telling it twice:**

- **Role facts → the tracker row.** The decline, the stated reasons, what it
  implies about level or comp, any future window.
- **Relationship facts → the contact's log.** That they chased it rather than
  letting it go quiet, how they said it, what they are owed now.
- **Each links to the other.** Neither retells the other's half.

**Worked example.** A recruiter relays that a role went to someone else and
mentions a possible different role in two months. The tracker row carries the
decline, the level read, the comp arithmetic and the future date. The contact
log carries one entry: he chased the hiring manager for a real answer, came back
candid rather than silent, the candidate replied the same day, **nothing owed**. **The
contact log does not re-explain the comp arithmetic, and the tracker row does
not re-explain that he is a reliable correspondent.** Both are complete; neither
is redundant.

### The state files get a LINE, not a story

**The open-items file and the outreach queue are read first and scanned fast.**
Their job is to say that a thing exists and where to look, not to contain it. A
paragraph there is a paragraph that will be stale in a week while the owner
moves on without it — **and the stale copy is the one that gets believed,
because it is the one in the file everyone opens.**

## ASK THE DIRECTION QUESTION OUT LOUD: who owes what, now?

**This is the single highest-value line in this file.** After every
communication, state explicitly which of three things is true:

1. **They owe us** — we are waiting, nothing to do.
2. **We owe them** — there is an action, and it belongs somewhere with a date.
3. **Nobody owes anybody** — the thread is at rest, and **say so**, because
   silence reads as case 1 by default.

**Case 3 must be written down.** A thread at rest that is not recorded as at
rest will be read as waiting on the other party forever.

**The failure that bought this rule:** a recruiter answered every outstanding
question in a single message — rate, benefits, contract length — which moved the
ball squarely back to the candidate. `pending_outreach.md` still read *"awaiting
his answer. Nothing owed, nothing to invest until the band comes back."* It
stayed that way for three weeks. **Every review that consulted the file saw a
thread correctly waiting on someone else, and the role was filled before anyone
looked again.**

**And the inverse error is just as real:** do not invent an obligation. A
contact who brought a lead unprompted, chased it, and reported back candidly is
owed nothing further if the person has already replied. Recording that as "at
rest" is what stops a future session surfacing them as overdue.

## The index reads these files, so the frontmatter is load-bearing

**`framework/scripts/build_contact_index.py` runs at every session start** and
builds `private/data/dashboard/contact_index.md` from the frontmatter of every contact
record: what needs a decision, how long since each last contact, and who
referred whom. **Shape the frontmatter per
`framework/templates/contact_record.md` or the contact drops out of the
index** — and a contact nobody can see is a contact nobody works.

**`last_contact` is a date and never a duration.** The index does the
arithmetic every run, so the file cannot go stale by sitting still.

## A BOOKED DATE IS NOT A FOLLOW-UP DATE

**`next_contact` is a scalar, and a hiring process is a list.** An interview
round spanning four days, with an assessment deadline running in parallel, has
no honest representation in one field: the soonest date hides the rest,
rescheduling one leg rewrites the field another leg owns, and a deadline has no
counterparty slot at all. **Three different kinds of date got collapsed into
one, and the collapse is what loses them.**

| kind | who is holding it | what a passed date means |
|---|---|---|
| **commitment** | someone else cleared a slot | it happened, or something went wrong — never ambiguous |
| **deadline** | nobody; it expires | the opportunity is gone |
| **follow-up** | self-imposed | nothing was promised; decide now |

**Only the third belongs in `next_contact`**, which narrows to mean *when to
reach out if nothing is on the books.* **It still reaches the calendar** — a
self-imposed date is a dated item you own, and the point of the view is that
there is one place to look. What it does NOT do is collide: only `SCREEN`,
`PANEL`, `CALL`, `INTERVIEW` and `ONSITE` occupy a slot someone else is
holding, so only those can flag a conflict. **A reminder, a published report
and a follow-up fit around a day rather than competing for it**, and flagging
them trains the reader to ignore the flag. The first two go in a `## Scheduled`
block on whichever file is primary — same test as every other routing decision
in this skill.

### The block: live items only, one line each

```
## Scheduled
- <WHEN> | <KIND> | <WHO> | <NOTE>
```

`<WHEN>` is `YYYY-MM-DD`, or `YYYY-MM-DD HH:MM TZ`, or `DUE YYYY-MM-DD` for a
deadline, or **`TBD` for a stage that exists but has no date.** `<KIND>` is one
uppercase token — `SCREEN`, `PANEL`, `CALL` for a slot someone else is
holding; `ASSESSMENT`, `DEADLINE` for something that expires; `EVENT` for a
dated thing that happens whether or not you act. **`NOTE` is never written by hand** — the renderer synthesizes it for the handful of dates that belong to no person and no company and so stay in the open-items file.

**`FOLLOW-UP` is allowed in the block ONLY on a company brief**, which has no
`next_contact` field to hold one. On a contact record it belongs in that field,
and writing it in the block instead gives one fact two owners — the precise
thing the rest of this skill exists to prevent.

**The routing table above says "both" for a recruiter about a requisition. That
is a rule for READING, not for the block** — a date has exactly one home, or it
has two owners. The event goes where the event is: an interview for that req on
the company brief, a call about the person's own pipeline on their record.

**A loop spanning several people goes on the COMPANY BRIEF** — no single
contact record owns a panel of three. **A one-to-one goes on the CONTACT
RECORD.** Stages already held, and stages still hypothetical, are not in the
block; the prose description of the process stays where it is and remains worth
reading.

**`TBD` is the whole reason this is a block and not a date field.** A stage
that is real but unscheduled is the one most likely to vanish, and a scalar
cannot represent it. Two TBDs stacked on a live thread is a stall you can
see.

### Rescheduling and cancelling are communications, so they are this skill

**Rescheduling touches one line.** The other legs are untouched — which is
precisely what a single date field cannot do without risking the wrong one.

**Cancelling REMOVES the line and the log records why.** The block holds only
what is live, so nothing stale accumulates, and the history goes where history
already goes. **A cleared date with no log entry is the failure mode**: the
views will report it as undecided when it was in fact decided against, and that
reads as neglect for as long as nobody checks.

**Neither is a new obligation.** Both are state changes, so the one-edit
fan-out above already governs them: the log and the block move together.

### What reads it

**`framework/scripts/build_contact_index.py` parses these blocks at every
session start** — from `data/contacts/*.md` and `data/companies/*.md` alike —
and renders `private/data/dashboard/calendar.md`: overdue first, then this week, then
upcoming, then the undated-but-sequenced stages. **A line that does not match
the grammar is printed under `DIDN'T PARSE` rather than dropped**, which is the
property the frontmatter cannot offer: a malformed entry there becomes a key
named `- 2026-11-04 08` and is never seen again.

**RE-RUN IT AFTER EDITING A BLOCK MID-SESSION.** It renders at session start, so
between a reschedule logged at midday and the next `open` the calendar shows the
date that was just changed — and it shows it with a generation stamp that makes
it look current. The script costs under a second and reads every record; there
is no reason to defer it to tomorrow. **This is most dangerous in exactly the
case the block was built for**: someone moves a meeting, the line is corrected,
and the view still says the old day.

## IF IT NEEDS PICKING UP LATER, IT GETS A DATE NOW

**The direction question above has a time dimension, and it is the half that
gets lost.** "They owe us" and "we owe them" are both unfinished — and an
unfinished thread with no date on it is indistinguishable, a month later, from
one that is simply over.

**So when a communication leaves something pending, record three things in the
same edit:**

1. **The date** it should be picked up.
2. **The condition** — what would make the follow-up unnecessary. Usually "they
   replied."
3. **What happens if nothing arrives.** A date with no stated action is a
   reminder to feel bad, not an instruction.

**The date goes where that KIND of date lives** — a booked commitment or a
hard deadline in the primary file's `## Scheduled` block, a self-imposed
follow-up in `next_contact`, and only a date belonging to no person and no
company in the open-items file — **not only in a tracker note.** A note is read
when someone opens that row; all three of those render into a session-start
view, which is the point.

### THIS SKILL DOES NOT SET THE INTERVAL, AND MUST NOT

**How long to wait is decided case by case, when the communication arrives, by
the person whose relationship it is.** There is no table of intervals here and
there should not be one.

**The reason is that the correct interval is a fact about the relationship, not
about the category.** A recruiter who explicitly asked not to be chased, a
contact who is travelling for a week, a hiring manager who named their own
timeline, and a thread where the other party has already done more than their
share all look identical to a rule and are completely different to a person.
**A rule that fires on all of them produces nagging, which costs more than the
thing it was protecting.**

**What this skill requires is only that the decision be MADE and WRITTEN, not
that it be made a particular way.**

### "NO FOLLOW-UP" IS A DECISION AND IT GETS RECORDED

**Deliberately choosing not to chase is a valid outcome and it must be written
down as one**, with the reason — otherwise a later session reads the silence as
an oversight and sets a date nobody wanted.

The case that proves it: a recruiter who brought a lead unprompted, chased it
himself, and came back with a candid answer, whose own stated etiquette is no
follow-up push, and who has already been thanked. **The correct record is "at
rest, nothing owed, do not surface as an action item" — and writing that is what
protects the relationship from the system.**

## OUTBOUND COUNTS

**A message sent is a state change.** It moves the thread from "we owe them" to
"they owe us", and that transition is exactly the one that goes unrecorded —
sending feels like the end of the task, so the log gets skipped.

Record what was sent, to whom, and **what a reply would look like.**

## A communication that changes no status still gets logged

A warm note, a decline relayed through a third party, a "still looking, no
news", a comment thread. **Status may not move and the record still should** —
otherwise the next session cannot tell silence from inaction.

## The completeness check

Before calling it logged, confirm:

- **If the status is now live** (`phone_screen` / `interview` / `offer`), **is
  the thread named in `open_threads.md` §1?** A live thread that exists only in
  tracker notes and a company brief is invisible to the file read first at every
  session — this happened to two simultaneous live threads and went unnoticed
  until someone asked.
- **If the status is now terminal, does every file that mentioned it say so?**
- **If a date was created, moved or killed, is the `## Scheduled` block right?**
  A new commitment is a line; a reschedule edits that one line; a cancellation
  REMOVES it and the reason goes in the log. Only a date belonging to no person
  and no company belongs in §3.
- **Does `pending_outreach.md` now say the true direction?**

## What belongs in the tracker note and what does not

The tracker note carries the reasoning, the quotes, and the numbers — it is the
durable record and it is allowed to be long. **The mirrors carry only what a
reader needs to act.** Point at the brief; do not restate it. See
`../framework-maintenance.md` for why a mirror that duplicates a source rots.
