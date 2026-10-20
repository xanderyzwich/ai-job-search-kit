# Template: company_brief.md
#
# Copy to private/data/companies/<company>.md the first time a company has a
# live thread: a warm contact, a scheduled call, or an application submitted.
# Built to be read mid-phone-call: short, scannable, current.
#
# THREE RULES THAT KEEP IT READABLE (the previous shape of this file did not
# hold, and the failure mode was always the same: dated sections appended to
# the bottom until the file became a log).
#
# 1. STATE, NOT HISTORY. The session log keeps the history. Nothing here gets
#    a dated section heading. Provenance lives inline on the line it qualifies,
#    as a short dated parenthetical, the way a config file carries it:
#    "Comp confirmed $X (verified YYYY-MM-DD)". Topical sections, dated lines.
# 2. NEVER APPEND. New information gets folded into the section it belongs to.
#    If it does not fit any section below, it belongs in the session log, not
#    at the bottom of this file.
# 3. FOLD ON THE EVENT. The moment a role's tracker status changes to a
#    terminal state (declined by them, declined by us, withdrawn, or discovered
#    closed), its block moves to Archived Roles in the same edit, compressed.
#    Not "soon". Same edit.
#
# WHAT GOES IN ROLES
# - Only roles that have actually been applied to (tracker status applied or
#   anything downstream of it). A role enters this file in the same edit that
#   sets its tracker status to applied. Before that it is a tracker row; its
#   score lives in the stack-rank file and its reasoning in the session log.
#
# WHAT DOES NOT GO HERE
# - Roles still being researched, and roles skipped before any application.
# - Company-level next actions. The open-threads file owns what is OWED; two
#   sources of truth is how one goes stale. "None identified" is a complete
#   References entry. "Worth a LinkedIn pass" is a next action.
#   BOOKED DATES ARE THE EXCEPTION and live in Scheduled below. A commitment
#   someone else is holding is not a next action, and prose in the open-threads
#   file proved unable to hold a multi-stage loop: the stages that had no date
#   yet simply vanished from it.
# - Status words invented here. Status is the tracker's literal token plus a
#   date, nothing more; narrative goes in the summary line. One vocabulary
#   note that matters for the funnel: declined_by_us is a POST-application
#   status (a withdrawal). A decision not to apply is skipped, never a
#   decline, because the funnel counts every decline as a submission.
# - Empty optional sections. Sections marked (optional) are omitted when
#   empty, never stubbed with "None yet".

# [Company Name]

One short paragraph, company-wide facts only: what they do, business model,
size and ownership, alignment rating against the register, employer-risk read,
comp bands by level if known. Nothing role-specific.

## Applying

(optional) How applications to THIS company work, reusable across reqs: ATS
and board URL or token, form quirks (fields that only render on a real click,
mandatory freeform prompts, stored-resume traps, CAPTCHA steps), and the comp
ask derived from the posted band under the salary-ask rule.

## Interview Process

Anything known about how THIS company interviews, independent of any single
req: loop shape, stages and what each tests, standing rules (tools allowed or
banned, behavioral expectations), typical timeline. Details of one specific
interview belong under that role's Interview Notes, below.

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

       - 2026-02-03 10:00 CT | SCREEN | [name] | stage 2, 45m
       - TBD | PANEL | hiring manager + an IC | stage 3, after the screen
       - DUE 2026-02-14 | ASSESSMENT | — | take-home, ~4h, NOT STARTED
-->

## References / Contacts

"None identified." when there are none. Otherwise:

### [Contact Name]
- How known, relationship, connection degree
- Their role and team
- Communication check point: last touch, what they offered or promised, next
  touch if one is owed

#### Talking Points
(optional) Points FOR this person specifically.

#### Questions to Ask
(optional) Questions FOR this person specifically.

## Questions to Ask

(optional) Company-level questions for anyone here, independent of role or
contact: culture and team health, remote durability, promotion velocity, comp
philosophy, anything the company summary leaves open. Role-specific questions
go under the role; person-specific ones under the contact.

## Roles

### [Role Title] (req id)
- Location / remote:
- Salary:
- Status: applied (YYYY-MM-DD)  <- the tracker's literal token, dated
- Found: where and how it surfaced (the tracker's found_via)
- Referral: (optional line) who, and whether it was attached to the submission
- URL: https://... (live YYYY-MM-DD)  <- date the posting was last seen open

Non-stack summary: two or three lines on what the role actually is, in plain
terms, and the one thing that would make it worth pursuing or not.

Tech Fit: 130 (85/45), scored YYYY-MM-DD  <- tech_fit (hard_match% / nice_match%)
Match:
  Required: named, required, items, met
  Preferred: named, preferred, items, met
Gap:
  Required: named, required, items, not, met
  Preferred: named, preferred, items, not, met

Required and Preferred mirror the two halves of the score: the Required lists
account for the hard number, the Preferred lists for the nice number. When the
JD does not separate them, everything sits under Required and the line says
"JD does not distinguish", which is how the scorer treats it too. A role that
was vetted but never formally scored writes "Tech Fit: not scored (vetted
YYYY-MM-DD)" and still fills the lists from the JD; the split is a JD fact,
not a score fact.

#### Talking Points
(optional) Role-specific: gaps to name proactively with their honest reframe,
the one story to land for this role's problem.

#### Questions to Ask
(optional) Role-specific, including any gating question that decides whether
to keep investing. Ask it early.

#### Interview Notes
(optional) Dated, one entry per instance: who, when, format, what was asked,
short debrief, what to fix before the next round. Role-specific only. How the
company interviews in general goes in Interview Process above, not here.

## Archived Roles

(optional) Applications that were actually made and are no longer active. A
block moves here, compressed, in the same edit that changes its tracker
status. Keep: title, req id, outcome and date, one-line reason, and any
interview notes worth keeping. Enough to prevent a re-apply and to preserve
what was learned. Nothing that was merely skipped ever enters this section.
