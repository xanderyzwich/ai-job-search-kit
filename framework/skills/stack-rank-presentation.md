# Skill: Stack-Rank Presentation

**Load when:** presenting scored roles to the owner — after a sweep, or any time they ask what there is to apply to, even with no sweep running.

**Pairs with:** `sweep-pipeline.md` (where the rows come from) and `match-gap-scoring.md` (what the numbers mean).

---

## What a row carries

One row per role, in this order, with the fields the owner acts on first and never missing:

1. **Company and role**, as the employer states them.
2. **Comp range as posted**, saying whether it is base, bonus-inclusive, zone-banded or blank. Blank says "not posted", never a guess.
3. **Apply link:** the employer's own application page wherever known. An aggregator's listing URL is only the listing; if the aggregator routes the application through its own form, name that on the row and prefer the employer's board.
4. **Level, lane and a one-line caveat** (remote unconfirmed, vague JD, prior application at that employer, possible duplicate requisition, liveness unconfirmed).

Scores, the actual missed requirements (quoted), and flags ride on the row after those four. **The number is the least useful part**: "two missed management requirements, both performance machinery, on a team of 4-6" tells the owner what the screen will be about; "75" does not.

## Ordering

- Default order: strictly by the score (`tech_fit`, or `rank = min()` of the dimensions present), ties marked "=" instead of an invented order. **If `profile.yml` states an ordering rule for a lane (for example that comp decides), that rule governs that lane's ordering**; the score then breaks ties.
- Apply the no-preference allowance in the SORT, not only at the admission floor: a row whose posting named no preferred items is scored out of a lower ceiling and would otherwise sort as worse. Add the same adjustment and mark it on the row (`100+15 NO-PREF`) so it is visible.
- Pay tier, alignment and lane ride alongside as tags, never blended into the score.

*Provenance: the no-preference allowance, the flat-decline rule and the caveats below were measured on one sweep and are working practice, not settled law. The liveness check is newer still. Tune them against use.*

## What does not occupy a slot

A row carrying a flag the owner treats as a flat decline (a fired gate, an explicit crunch trigger) is excluded from the ranked list and listed separately. Rank what can be applied to.

## How many

Present about ten above the owner's working score bar, not every survivor. The tracker holds all of them, so nothing is lost; `backlog.py` is where the rest live.

## Caveats ride ON the row

Three that would each have misled in a footnote: a band that is total cash including bonus rather than base; an alignment tag that belongs to the parent company rather than the role; a role naming no hands-on duty, which can outrank genuinely hands-on rows under a comp-first ordering.

## Check before presenting

Rows from an old sweep may be dead. Check liveness first where the board allows it, and mark "liveness unconfirmed" where it does not. A role the owner has already applied to, or that is on the closed list, is not presented again.
