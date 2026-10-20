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

## The fan-out, and it is ONE EDIT

**A state change goes into every file that carries it, in the same edit.** Not
"later", not "at close", not in the next session.

| file | what it holds | when it changes |
|---|---|---|
| `job_tracker.csv` | status, dates, the full reasoning | **always** |
| `open_threads.md` §1 | that the thread exists and what is live | any thread that is live, newly live, or just closed |
| `open_threads.md` §3 | a date created or killed | an interview booked, a window opened, a revisit promised |
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
builds `private/temp/contact_index.md` from the frontmatter of every contact
record: what needs a decision, how long since each last contact, and who
referred whom. **Shape the frontmatter per
`framework/templates/contact_record.md` or the contact drops out of the
index** — and a contact nobody can see is a contact nobody works.

**`last_contact` is a date and never a duration.** The index does the
arithmetic every run, so the file cannot go stale by sitting still.

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

**The date goes where dated things already live** — the hard-dates section of
the open-items file — **not only in a tracker note.** A note is read when
someone opens that row; a date is read at the start of every session, which is
the point.

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
- **If a date was created or killed, is §3 right?**
- **Does `pending_outreach.md` now say the true direction?**

## What belongs in the tracker note and what does not

The tracker note carries the reasoning, the quotes, and the numbers — it is the
durable record and it is allowed to be long. **The mirrors carry only what a
reader needs to act.** Point at the brief; do not restate it. See
`../framework-maintenance.md` for why a mirror that duplicates a source rots.
