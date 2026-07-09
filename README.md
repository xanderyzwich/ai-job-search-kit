# AI Job Search Kit

A structured workspace for running a job search as a long-running collaboration
with an AI assistant, across many sessions, without losing context, drifting into
overclaims, or re-deciding the same strategy twice.

This repo is the **framework**: the reusable system, not any one person's job
search. It's designed so someone else could clone it, drop their own data into a
gitignored `private/` directory, and run the same workflow, without ever seeing a
name, a salary figure, or a company from the original author's search.

---

## The problem this solves

Using an AI assistant for a job search sounds simple until you actually try to run
it for more than a session or two. A few things break in practice:

- **Context resets.** Every new session starts from zero unless something tells the
  assistant what's already been decided, verified, and ruled out.
- **Claims drift.** A resume bullet gets a little rounder each time it's rewritten.
  Without a single source of truth to check against, small exaggerations compound
  silently across dozens of documents and applications.
- **One-size-fits-all advice doesn't fit.** A resume, cover letter, or even a
  LinkedIn profile that leads the same way for a Staff IC role and a Head of
  Engineering role will misfire on one of them. The right framing depends on what's
  actually being screened for.
- **Personal data doesn't belong in a portfolio.** If you want to show the system
  off, your comp floor and your recruiter's phone number can't be sitting in the
  same repo.

This kit addresses each of those directly, rather than assuming an assistant will
handle them by default.

---

## How it's built

```
ai-job-search-kit/
├── README.md              — this file
├── ARCHITECTURE.md        — the design decisions and why they were made
├── CHANGELOG.md           — how the framework evolved, tied to real failures
├── QUICKSTART.md          — step-by-step setup, including how to generate
│                           experience_summary.md
├── SESSION_INIT.md        — entry point; checks for and loads the private
│                           session-init skill if one exists
├── LICENSE                — MIT
├── .gitignore              — excludes private/, output/, temp/
│
├── framework/              — the reusable system (tracked in git, no personal data)
│   ├── CONTRACT.md           the exact file contract private/ must satisfy
│   ├── skills/                small, focused methodology files, loaded on
│   │                          demand: search, triage, resume lanes, tracking,
│   │                          writing standards, session continuity, the
│   │                          verified-experience interview, and a
│   │                          communications/ set for warm outreach and
│   │                          screen-call prep
│   ├── scripts/                working tooling: a one-command bootstrap, a
│   │                          layout-only resume renderer driven by a content
│   │                          file, a tracker-to-history generator, a
│   │                          one-commit-per-day log tool, and a funnel report
│   └── templates/              blank versions of every file private/ needs
│
├── private/                — the user's actual data (its own gitignored repo)
│   └── (see framework/CONTRACT.md — never committed to this repo. Canonical
│        facts at the root, methodology in skills/, working state in data/)
│
└── output/                 — generated deliverables (gitignored, not tracked)
```

`private/` is deliberately outside this repo's git history. It's set up as its own
independent repository, so a real job search gets real version control, just not in
public. Nothing in `framework/` or this README depends on `private/` existing to be
read and understood; it depends on it existing to actually *run*.

### The core design ideas

**A single source of truth, checked against, not just referenced.**
One document holds every verified fact about the candidate's actual experience,
including the overclaims to specifically avoid. Every other document, resume,
cover letter, LinkedIn copy, defers to it. This is the mechanism that stops small
exaggerations from compounding across a long search: nothing gets written that
can't be traced back to something verified.

**Config separated from content.**
Anything sensitive, a salary floor, a location constraint, a list of target titles,
lives in a small structured data file (`private/profile.yml`), not scattered as
hardcoded numbers across prose documents. The framework's methodology files
reference "the candidate's floor," never a real number. This is the same
config-versus-code separation any software project uses for secrets, applied to a
job search instead of an API key.

**Lane-based routing instead of one-size-fits-all advice.**
The search runs two distinct strategies at once, each with a different resume, a
different cover-letter posture, and a different framing on the same underlying
facts. A methodology file doesn't give generic advice; it routes based on which
lane a given role actually falls into.

**Session continuity as a first-class concern.**
`SESSION_INIT.md` exists because an assistant with no memory of yesterday's
decisions will happily re-litigate them today. The public root version checks
for a private, filled-in session-init skill and loads it if present; once your
private instance exists, that private file supersedes the generic one
permanently. That skill splits into a stable map (safe to load once into a
Claude Project and forget about) and a dynamic log read fresh each session,
so current state never goes stale in static context. A small open-threads
file, overwritten at every session close, answers "what's due" without
digging through the log, and a daily-log tool folds each day's notes into one
amended commit, so the bookkeeping never becomes debt. From there, loading
only the smaller skill files relevant to today's task keeps a session from
re-reading the entire methodology to answer one narrow question.

**State kept apart from methodology, and views generated rather than mirrored.**
Working state (the session log, open threads, dated market snapshots,
per-company call briefs) lives in its own data layer, separate from the skill
files that describe method. A methodology file never carries an "as of" fact;
a snapshot never hides in a file that's assumed to be timelessly true. The
application tracker is the single hand-edited record, and the human-readable
history is rendered from it by script. Two hand-maintained files describing
the same applications will eventually disagree; a generated view can't. This
rule was adopted after that exact drift happened once in practice.

**A funnel that gets measured, not felt.**
Every application row carries its source, its lane, and which resume version
went out, and a small script turns the tracker into response and advance
rates split by each. "The volume isn't converting" stops being a feeling and
becomes a number, including a clean before/after read any time the resume
changes.

**A human-writing quality gate.**
Every piece of generated copy that will actually be sent passes a standards check
before it's presented, specific patterns that read as AI-generated get caught and
rewritten, on the theory that a job search is exactly the wrong place for a
recruiter to notice the writing wasn't yours.

See `ARCHITECTURE.md` for the fuller reasoning behind each of these, including a
couple of decisions that were wrong on the first pass and had to be corrected.

---

## If you found this through my resume

Then this repo is doing its second job: it's a work sample. The search it
runs is mine, and none of my actual data appears here, but the engineering is
all visible. Config is separated from content the way production systems
separate secrets from logic. Human-readable views are generated from a single
record instead of maintained as mirrors, a rule adopted after mirror drift
bit once and cost a rebuild. State lives apart from methodology so nothing
dated can hide in a file that's supposed to stay true. The funnel is
measured, not felt. And the mistakes in `ARCHITECTURE.md` are recorded on
purpose: a system that only shows its finished state hides the most useful
information, and how an error got caught says more about the builder than
the parts that went right the first time.

The short tour: this file for the what, `ARCHITECTURE.md` for the why
(including two recorded mistakes and their corrections), `CHANGELOG.md` for
how it evolved, `framework/CONTRACT.md` for the interface discipline, and
`framework/scripts/` for working code.

---

## Using this for your own search

The full walkthrough is in `QUICKSTART.md`, and `framework/scripts/bootstrap.py` does the file setup in one command. The short version: read
`framework/CONTRACT.md` for the file shapes, copy the templates from
`framework/templates/` (and the tooling from `framework/scripts/`) into your
own gitignored `private/`, fill them in, and point an assistant at the repo
root. `SESSION_INIT.md` bootstraps a fresh clone; once your private
session-init skill exists, it supersedes the generic checklist for good, and
every session after that starts from your own map.

One file in that list deserves more than a copy-and-fill treatment.

### On generating `experience_summary.md`

Every other template is mechanical: `profile.yml` is a form, the skill
templates are a pattern to apply. `experience_summary.md` is different,
and it's worth understanding why before treating it as one more file to
fill in.

This file didn't get built by transcribing a resume into a nicer format. It
came out of an adversarial interview: going claim by claim and asking what
was actually done versus what a team or predecessor did, what the real
mechanism behind an outcome was, whether a stated number had been verified
or just sounded about right. Several lines that started out clean and
resume-ready got walked back mid-conversation once they were actually
pushed on, "built fraud detection" became "built the data layer behind a
detection system someone else owned," which is a less flashy sentence and a
considerably more defensible one.

That process, not the document it produces, is the thing worth replicating.
Doing it well means asking an assistant to find the soft spot in each claim
rather than to make your experience sound better, and being willing to have
something you're proud of turn out rounder than the truth. The full
methodology is a loadable skill,
`framework/skills/verified-experience-interview.md` — what to push on, the
walk-back protocol, the overclaim patterns worth hunting. `QUICKSTART.md`
has the walkthrough including a starter prompt, and `ARCHITECTURE.md`
covers why a single verified source of truth matters enough to justify the
extra effort.

---

## Status

Actively developed alongside a real job search. `framework/` is extracted
from a working personal instance rather than designed in the abstract, so it
reflects what actually held up under repeated use, and what broke and got
fixed. The drift-prevention rules, the generated-views rule, and the data
layer all exist because the failure they prevent happened at least once in
practice. Current state and what's still soft: see `ARCHITECTURE.md`,
"Known limitations."

---

## License

MIT — use it, adapt it, run your own search on it. The one condition is the
one intended: the copyright notice travels with any copies or substantial
portions, so credit follows the work wherever it's distributed or forked.
See `LICENSE`.
