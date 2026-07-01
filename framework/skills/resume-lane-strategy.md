# Skill: Resume Lane Strategy

**Load when:** deciding which resume to use for a role, editing resume content or
bullet ordering, or evaluating whether a posting is a fit before applying.

**Depends on:** `private/profile.yml` (`lanes.pc`, `lanes.ic`) for the
actual title lists and org-size ranges this pattern routes against.

---

## The problem

A single resume, and a single positioning story, doesn't fit every role a search
targets if the search spans more than one kind of organization. The same
candidate, the same facts, need a different opening impression depending on what
a reviewer is actually screening for.

## The pattern: two lanes, one set of facts

**IC (Individual Contributor) — large-org IC roles, or a small team inside a larger company.**
The role is individual-contributor, technically deep, and the organization is
large enough that a leadership-forward opening reads as a category mismatch. A
reviewer screening for a senior IC will misfile a leadership-led resume as
belonging to a manager, not an engineer, and move on.

**PC (Player-Coach) — small-org hands-on leadership.**
The organization is small enough (see `profile.yml: lanes.pc.org_size`) that
the technical work and the leadership work are the same job. Here the
team-and-judgment story *is* the qualification being screened for, not a
secondary signal. Leading with pure technical detail buries the actual point.

Same underlying facts, different lead, because the lead is answering a different
implicit question: "is this person deep enough to trust with hard technical
problems" versus "is this person someone I'd trust to run a team and still be
useful in the code."

## Routing signal

Route a given opportunity into a lane using, in order of reliability:

1. **Explicit org size**, if known (team size, company size). Below the
   `pc.org_size` threshold in `profile.yml`, default to PC read.
2. **Title-implies-scale-up language** in the posting. Titles that almost always
   grow into pure people-management (see the "requires explicit qualification"
   tier in `search_criteria.md`) should be read as PC only if the JD body
   explicitly disclaims that growth path.
3. **When genuinely ambiguous**, prefer whichever resume a warm contact at the
   company would find familiar — if there's a referral path, ask rather than guess.

Title alone is an unreliable router by itself. The same job at a company small
enough to need a hands-on leader gets called "Staff Engineer," "Director of
Engineering," or "Head of Engineering" depending on the org's own conventions,
not on the actual scope of the role.

## Ordering within a resume

The lane determines the resume, but it also determines the internal ordering of
the *same section* within that resume:

- **IC ordering:** open with the strongest one or two purely technical
  outcomes. Place leadership/mentorship material in the prominent upper-middle,
  not first and not buried. Differentiated leadership material still needs to be
  visible, just not load-bearing for the first impression.
- **PC ordering:** open with the strongest team-judgment or ownership story.
  Technical delivery material follows, still substantial, but not the lead.

## A reconciliation trap worth naming explicitly

General resume advice ("don't bury your most differentiated material at the
bottom") and lane-specific ordering can appear to conflict. They usually don't;
both are satisfied by placing differentiated material prominently *without*
necessarily making it the opening line. The trap is applying general advice
without checking it against an already-made, more specific lane decision, since
the general advice is usually correct in isolation and easy to apply without
noticing it's quietly reversing an earlier, deliberate call. When general advice
and a specific existing decision appear to point different directions,
reconcile them explicitly rather than letting whichever was stated most recently
win by default.

## What this pattern does not decide

This file describes the routing logic and the ordering principle. It does not
contain anyone's actual lane assignments, bullet content, or resume text — see
`private/skills/resume_strategy.md` for the filled, human-readable instance of this
pattern applied to one person's real facts.
