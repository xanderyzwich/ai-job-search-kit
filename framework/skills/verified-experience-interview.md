# Skill: The Verified-Experience Interview

**Load when:** generating or substantially revising an
`experience_summary.md`, or adding any single new claim to an existing
one — new claims get the same scrutiny the originals did.

**Depends on:** whatever raw material exists (a resume, a LinkedIn About
section, notes), and a person willing to have something they're proud of
turn out rounder than the truth.

---

## What this is, and what it is not

This is not resume writing. The assistant's job here is to find the soft
spot in each claim the way a sharp interviewer would, not to make experience
sound better. The output is a document where every line survives a hostile
follow-up question — which is worth more than any polished line that
doesn't, because the polished line eventually meets that follow-up in a
live interview, with no time to walk it back gracefully.

## How to run it

Go claim by claim, one at a time, never in batch. For each claim, push on
four things in order:

1. **Attribution.** What did this person specifically do, versus what a
   team, a predecessor, a vendor, or a tool did? This is the single most
   common place overclaims live. "Built X" often decomposes into "operated
   and extended X, which someone else designed" — a less flashy sentence
   and a far more defensible one.
2. **Mechanism.** What actually produced the outcome being cited? A claim
   that names a result but can't explain the mechanism behind it will
   collapse under one "how?" in an interview. If the person can't state the
   mechanism, the claim gets narrowed until they can.
3. **Numbers.** Is every figure something that was verified, or something
   that sounds about right? Unverified numbers get replaced with what IS
   known ("hundreds of," "a multi-terabyte," an honest range) or dropped.
   A round number a candidate can't source is worse than no number.
4. **Titles and scope.** Did the role actually carry the scope the title
   implies, and vice versa? Both directions matter: inflated titles get
   caught in reference checks, and deflated ones undersell real scope that
   the verified facts support.

## The walk-back protocol

When a claim turns out rounder than the truth, two writes happen, not one:

- The **corrected version** goes into the summary — fixing today's document.
- The **original overclaim** goes into the "Overclaims to avoid" section,
  verbatim, with the correction beside it.

The second write is the load-bearing one. A rejected exaggeration that
isn't written down anywhere will quietly resurface in a later session that
doesn't have this conversation in context — plausible-sounding overclaims
are exactly the kind of thing a fresh drafting pass reinvents. And when an
overclaim is scrubbed, search the entire private instance for its phrasing,
including sample copy inside skill files; a stale example is a
reintroduction vector.

## Patterns worth pushing on specifically

- "Built / architected / designed" where "operated," "extended," or
  "maintained" is the truth — each step up that ladder is individually
  small and cumulatively large.
- Outcomes inherited from a system's existing design, claimed as personal
  results.
- A prototype or proof-of-concept described in shipped-to-production
  language.
- Team-level or org-level wins ("we integrated four companies") carrying an
  implicit personal "I."
- Precise-sounding metrics with no measurement behind them, especially
  round user counts, percentages, and environment tallies.
- Credit that belongs partly to someone else — a colleague's prototype
  that got adapted, a lead who set the direction. Keep the credit split
  intact in the written record; it will come up.

## Signs it's working

The person walks something back mid-conversation and the corrected version
still reads well. The document gets slightly less impressive and
substantially more defensible. The "Honest gaps" section grows alongside
the accomplishments — a summary with no admitted gaps hasn't been pushed
hard enough. Multiple passes happen; a single-pass summary is a transcribed
resume with extra steps.

## A starter prompt

> I want to build a verified account of my work experience that I'll use as
> the source of truth for my resume and job search materials going forward.
> Here's my current resume/background: [paste it]. Go through each claim
> with me one at a time. For each one, ask what I specifically did versus
> what a team or predecessor did, what the real mechanism behind any result
> was, and whether any number I'm using is something I actually verified.
> Push back if something sounds rounder or more impressive than it probably
> was. I'd rather have an accurate, slightly less flashy account than a
> polished one I can't defend in a follow-up question.
