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

  next_action:
      One line. Leave blank ONLY when `owed_by: nobody`, and say why in the
      body. Deliberate inaction is a decision and gets recorded as one.

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
