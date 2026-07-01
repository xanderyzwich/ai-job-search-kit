# Architecture

This document explains why the system is shaped the way it is: the mechanisms
underneath the ideas summarized in `README.md`, and a few decisions that were
wrong on the first pass and had to be corrected once the mistake became visible.

---

## The three-layer separation

```
framework/   the reusable system        — public, no personal data, works for anyone
private/     one person's actual data   — gitignored, its own independent git repo
output/      generated deliverables     — gitignored, not standing state
```

The test for where something belongs: **would this sentence still make sense if
`private/` were deleted?** If a methodology file says "the candidate's floor" it
belongs in `framework/`. If it says an actual dollar figure, it belongs in
`private/profile.yml` and the methodology file should be rewritten to reference it
instead of restating it.

This sounds like an obvious rule once stated, but it was violated once during this
project's own construction (see "Mistakes and corrections" below), which is
itself evidence for why it needs to be a checked rule rather than an assumed
habit.

`private/` being its own independent git repository, rather than just a gitignored
folder, matters for a reason beyond privacy: a real job search accumulates real
history worth version-controlling, revised resumes, changing positioning, session
notes, and that history shouldn't be lost just because it can't be public. Nesting
an independent repo inside a gitignored path costs nothing (the parent repo never
sees it) and gets the personal data its own real history.

---

## Source of truth, not just a reference document

The riskiest failure mode in a long AI-assisted job search isn't an outright
fabrication, it's small, plausible-sounding rounding. "Owned and operated a
platform" becomes "built a platform" becomes "architected a platform," each step
individually defensible, the cumulative distance from what actually happened
significant. This compounds specifically because the content is regenerated
across many sessions and many documents: a resume, three or four cover letters,
LinkedIn copy, DM drafts. Nothing catches the drift unless something is designated
to catch it.

The mechanism here is a single verified document (`experience_summary.md` in the
private contract) that every other piece of content defers to, including an
explicit list of claims to *not* make, phrasings that were tried, found to be
overclaims on closer inspection, and deliberately excluded going forward. New
content gets checked against this file before being finalized, not written fresh
from a general impression of "roughly what happened."

The list of excluded claims is as load-bearing as the verified facts. Without it,
a plausible-sounding overclaim that was already rejected once can quietly get
reintroduced in a later session that doesn't have the earlier conversation in
context.

---

## Config separated from content

Personal specifics, a salary floor, excluded relocation regions, contact details,
target title lists, live in one structured file (`private/profile.yml`), not
scattered as inline values across prose documents. Framework methodology files
reference these as named variables ("the candidate's floor") rather than
hardcoding a number.

This is a direct import of a pattern every software project already uses for
secrets and environment-specific config: separate the logic from the values so
the logic can be shared, published, and reasoned about independently of any one
deployment's actual data. Here, "deployment" is a person's actual job search.

The practical benefit shows up immediately at the moment a repo is about to go
public: instead of auditing every prose document for leaked numbers, there's one
file to check, and everything else is provably generic by construction as long as
the "reference, don't restate" rule was followed while writing it.

---

## Lane-based routing

A single positioning strategy doesn't fit every role a search actually targets.
Two org shapes produce very different screening logic even when the underlying
candidate and facts are identical:

- **IC** (large-org individual-contributor roles, or a small platform team inside a larger company):
  the opening impression needs to read as deep technical ownership first, or a
  reviewer misfiles a leadership-forward candidate as a manager rather than a
  senior IC.
- **PC** (small-org hands-on leadership): the team-and-judgment story *is*
  the qualification a reviewer is screening for, so leading with technical detail
  buries the actual signal.

Rather than writing generic advice and hoping it fits both, the methodology
routes: which resume, which cover-letter posture, which bullet ordering, based on
which lane a given opportunity actually falls into. The routing signal is
articulated explicitly (roughly: company/team size, and whether the role is
titled in a way that implies people-management scale-up) rather than left
implicit, so a new session can make the same call consistently instead of
re-deriving the distinction from scratch, or worse, blending both approaches into
a document that serves neither well.

---

## Session continuity

An assistant with no persistent memory across sessions will, by default, either
lose context entirely or re-derive decisions that were already carefully made.
Both failure modes are expensive: the first repeats work, the second can
silently reverse a considered decision without anyone noticing it happened.

`SESSION_INIT.md` is the fix: a fixed entry point every session reads first.
The public root version is deliberately generic, it checks whether a private,
filled-in skill exists (`private/skills/session_init.md`) and loads it if
present, for the same reason `profile.yml` is separated from the methodology:
the pattern is reusable even though the content isn't. That private skill
itself splits into two files with different lifecycles: a stable map (safe to
load once into a Claude Project and forget about) and a dynamic log (read
fresh each session for what currently exists, what's decided, and what's
still open). Conflating those two, letting dated facts creep into the stable
map, is the failure mode that motivated the split; see
`framework/skills/session-continuity.md` for the fuller reasoning.

A second continuity problem shows up at scale rather than on day one: a
methodology document that starts small tends to grow, every session adds a
section, until it's an 800-plus-line file that gets fully re-read for every task
regardless of relevance. The fix is decomposition into small, single-purpose
skill files, each with a one-line description of when it applies, loaded only
when the task at hand actually needs it. The session-init skill acts as the
index: it doesn't contain the methodology, it says which smaller file contains
the methodology relevant to today's task, with one exception, it's the one
skill that loads unconditionally rather than on demand, since its whole job is
telling a session what else to load.

---

## The human-writing quality gate

Any generated content intended to actually be sent, a cover letter, an essay
answer, an outreach message, passes a standards check before being presented as
final. The check targets recognizable AI-generated patterns specifically:
uniform sentence length, certain stock phrases, structural tells like
three-part parallel constructions repeated across paragraphs. This exists
because the failure mode in a job search isn't generic bad writing, it's writing
that's competent but detectably not the candidate's own voice, which is a
specific, catchable signal a reader can pick up on even without articulating
why something feels off.

---

## Mistakes and corrections

Two are worth recording plainly, since a system that only presents its finished
state hides the more useful information: what actually goes wrong when building
something like this, and how it gets caught.

**A personal-data leak in the framework's own scaffolding.** An early draft of
the public `SESSION_INIT.md` included the actual comp floor and actual excluded
relocation regions directly in the file, before the config-separation pattern
existed. It was never committed, but it existed, uncommitted, in a directory that
would eventually be pushed public. The fix wasn't just deleting the numbers, it
was building `profile.yml` and rewriting the file to reference it, then
explicitly re-checking every public-facing file with a grep for personal
identifiers before treating the boundary as trustworthy. The larger lesson: a
public/private boundary that relies on remembering not to write something in the
wrong place will eventually fail. The boundary needs a check, not just a
convention.

**A positioning decision that got reversed without being flagged as a
reversal.** Earlier reasoning had explicitly concluded that a Staff/Principal IC
resume should lead with technical impact, not leadership, specifically to avoid a
reviewer misreading a leadership-forward opening as evidence of an EM rather
than a senior IC. Later in the same project, in the course of expanding that
same resume to a second page, the section got reordered to lead with leadership,
justified at the time by unrelated general advice about not burying
differentiated material at the bottom. That advice was correct in isolation, but
applying it without checking against the earlier, more specific decision
reversed a considered call silently. It was only caught because the earlier
reasoning was checked directly against a transcript rather than reconstructed
from memory. The fix applied going forward: general advice and specific,
already-decided constraints get reconciled explicitly when they appear to
conflict, rather than letting the more recently stated one silently win.

Both corrections point at the same underlying practice: when something might
contradict an earlier decision, check the actual record rather than trusting a
summary of it, including a summary generated by the assistant itself.

---

## Known limitations

- `framework/scripts/` is empty. The resume builder currently used exists as a
  personal, one-off script in the private data (hardcoded to one person's
  content) rather than a generalized script that reads from `profile.yml` and
  `experience_summary.md` directly. Generalizing it is the main remaining gap
  between what `framework/CONTRACT.md` implies is possible and what actually
  works out of the box today.
- The lane-routing signal (org size, title-implies-management-scale-up) is
  currently a judgment call applied per-role, not a hard rule. It could be made
  more explicit with concrete thresholds, at the cost of some flexibility.
- The human-writing quality gate is a checklist applied by the assistant, not an
  automated test. It depends on the assistant applying it consistently, which is
  itself a continuity problem the skill-decomposition approach is meant to help
  with, but doesn't fully solve.

## Open design questions

- Should `framework/scripts/` generate documents from `profile.yml` and
  `experience_summary.md` directly (more automated, less flexible), or remain a
  set of building blocks a session assembles per-document (more flexible, more
  manual)?
- How much of the lane-routing judgment can be made data-driven versus how much
  should stay a qualitative read of a given job posting?
