---
name: Full Name
company: Current employer, or blank if unaffiliated
role: What they do — recruiter, hiring manager, engineer, friend
owed_by: them
last_contact: 2026-01-01
next_contact:
next_action: One short line. Blank only when owed_by is nobody.
acquired_via: How this contact entered the search
linkedin:
email:
phone:
note: One sentence a reader needs before opening the file.
---

# Full Name

<!--
COPY TO private/data/contacts/<first-last>.md.

WHICH FILE DOES A CONTACT LIVE IN? Ask: **does this person's value survive if
the company goes away?**
  - NO  -> they ARE the company. Put them in `data/companies/<company>.md`
           under References / Contacts, where they are read in context.
  - YES -> they span employers (an agency recruiter) or have none (a friend,
           a peer, a community contact). They get a file here.

THE FRONTMATTER IS PARSED, SO ITS SHAPE IS A CONTRACT.
`framework/scripts/build_contact_index.py` reads it at every session start to
build the index. Flat `key: value` pairs only — no nesting, no lists. Dates are
YYYY-MM-DD. A blank value is meaningful and is not the same as a missing key.

FIELD NOTES, in the order that matters:

  owed_by: them | us | nobody
      The direction question from `framework/skills/communications/
      communication-logging.md`. **`nobody` must be stated, never left blank** —
      a thread at rest that is not recorded as at rest reads as waiting on the
      other party forever. That inversion cost a real six-month contract: a
      file said "awaiting his answer" for three weeks after he had answered.

  last_contact:
      A DATE, never a duration. The index computes elapsed days every run.
      Writing "85 days ago" into a file produces a number that is wrong
      tomorrow and misleading next month.

  next_contact:
      A date, or blank. **Blank plus `next_action` text means UNDECIDED, not
      at rest** — and the index reports it that way, because those two look
      identical from outside and mean opposite things.

      **This field is the SELF-IMPOSED follow-up only** — when to reach out if
      nothing is on the books. A date someone else is holding (a call, an
      interview) and a hard deadline are different facts with different failure
      modes, and they go in the `## Scheduled` block below. Do not put a booked
      meeting here: it is a scalar, so the second one overwrites the first.

  next_action:
      One line. Leave blank ONLY when `owed_by: nobody`, and say why in the
      body. Deliberate inaction is a decision and gets recorded as one.

  linkedin: / email: / phone:
      THE ADDRESSES. Fill each the moment it appears in a message header, not
      when someone finally needs it. **A contact reachable only through a
      shared employer is not reachable** — that channel ends with the job, for
      either party, and the record is what survives it.

      `phone:` exists because TEXT is a channel and had no home: a log entry
      could say a message arrived by text while the file held no number to
      text back. Any readable format; nothing parses it.

PACING IS NOT SET HERE AND MUST NOT BE. How long to wait is a fact about the
relationship, not the category — see the communication-logging skill. This
template requires only that the decision be made and written.
-->

One paragraph: who they are, how they know the candidate, and what they can actually
do. Not a biography — the thing a reader needs before picking up the phone.

## Referral provenance

**Referred BY: [Name](their-file.md)** — or "none recorded".

**Has referred onward:** list them, or "none recorded". **Recorded at BOTH ends
deliberately**, so a hub's yield is visible without anyone maintaining a tally,
and so any contact can be traced back through whoever connected them.

## What they can do

What this person is actually useful for, stated honestly. A recruiter who
places in the wrong band, a friend with no hiring authority, and a hiring
manager at a target employer are all "contacts" and none of them are the same
lever.

## Scheduled

<!-- LIVE COMMITMENTS AND DEADLINES ONLY, one line each. PARSED — the grammar
     is a contract. `framework/scripts/build_contact_index.py` reads this block
     at every session start and renders private/data/dashboard/calendar.md -- COMMITTED, so
     it is readable from a phone when the machine is off.

       - <WHEN> | <KIND> | <WHO> | <NOTE>

     <WHEN>  YYYY-MM-DD · YYYY-MM-DD HH:MM TZ · DUE YYYY-MM-DD (a deadline)
             · TBD (a stage that is real but not yet scheduled)
     <KIND>  one uppercase token. SCREEN · PANEL · CALL are commitments someone
             else is holding; ASSESSMENT · DEADLINE expire; EVENT is a dated
             thing that happens with or without you. FOLLOW-UP appears here ONLY
             on a company brief, which has no `next_contact` field -- on a
             contact record a self-imposed follow-up belongs in that field
             instead, and putting it here gives the same fact two owners.
     <WHO>   the counterparty, or a dash for a deadline nobody is holding
     <NOTE>  stage number, duration, what is blocking it

     WHY A BLOCK AND NOT A FRONTMATTER FIELD: `next_contact` is a scalar and a
     hiring process is a list. A four-stage loop with an assessment deadline
     running alongside it cannot fit in one field -- the soonest date hides the
     rest, and rescheduling one leg rewrites the field another leg owns.
     `next_contact` therefore means only "when to reach out if nothing is on
     the books."

     TBD IS THE POINT. A stage that exists but has no date is the one that
     disappears, and a scalar cannot represent it at all.

     LIVE ONLY. A held stage leaves this block; a cancelled one is REMOVED and
     the reason goes in the log. A date cleared without a log entry reads as
     undecided when it was in fact decided against.

     A line that does not match the grammar is reported under DIDN'T PARSE in
     the rendered calendar rather than silently dropped.

     NOTE is not written by hand -- the renderer synthesizes it for dates kept
     in the open-items file. A block line always uses one of the kinds above.

     THIS BLOCK SHIPS EMPTY ON PURPOSE. A sample event left in a copied
     template renders as a REAL commitment on a REAL calendar, under the name
     of whoever the file was copied for -- precisely the invented date this
     view exists to make impossible. Examples therefore live in here, where
     the parser cannot reach them:

       - 2026-02-03 14:00 ET | CALL | — | the intro call they offered
       - DUE 2026-02-10 | DEADLINE | — | they asked for a decision by then
-->

## Contact log

<!-- NEWEST FIRST, so the current state sits next to the frontmatter that
     summarises it. Append a new entry at the TOP; never rewrite an old one.

     THE FRONTMATTER AND THE TOP LOG ENTRY MUST AGREE, AND THEY ARE UPDATED IN
     THE SAME EDIT. A summary that drifts from its own log is the same failure
     as a tracker that disagrees with the file mirroring it — and the mirror is
     what gets believed. -->

### 2026-01-01 — what happened

**Result:** what actually came of it, in their words where possible.

**Owed after this:** them / us / nobody, and why.

**Next:** the action and its date, or the decision not to act and its reason.
