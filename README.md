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
├── QUICKSTART.md          — step-by-step setup, including how to generate
│                           experience_summary.md
├── SESSION_INIT.md        — generic startup checklist, loaded every session
├── .gitignore              — excludes private/, output/, temp/
│
├── framework/              — the reusable system (tracked in git, no personal data)
│   ├── CONTRACT.md           the exact file contract private/ must satisfy
│   ├── skills/                small, focused methodology files, loaded on demand
│   ├── scripts/                generators (e.g. a resume builder), parameterized
│   └── templates/              blank versions of every file private/ needs
│
├── private/                — the user's actual data (its own gitignored repo)
│   └── (see framework/CONTRACT.md — never committed to this repo)
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
decisions will happily re-litigate them today. It's the entry point every session
reads first: what's been decided, what's still open, and which of the smaller
skill files are actually relevant to today's task, so a session doesn't have to
load the entire methodology to answer one narrow question.

**A human-writing quality gate.**
Every piece of generated copy that will actually be sent passes a standards check
before it's presented, specific patterns that read as AI-generated get caught and
rewritten, on the theory that a job search is exactly the wrong place for a
recruiter to notice the writing wasn't yours.

See `ARCHITECTURE.md` for the fuller reasoning behind each of these, including a
couple of decisions that were wrong on the first pass and had to be corrected.

---

## Using this for your own search

The full walkthrough is in `QUICKSTART.md`. The short version: read
`framework/CONTRACT.md` for the file shapes, copy the templates from
`framework/templates/` into your own gitignored `private/`, fill them in,
and point an assistant at the repo root with `SESSION_INIT.md` as the entry
point.

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
something you're proud of turn out rounder than the truth. `QUICKSTART.md`
has the full walkthrough, including a starter prompt, and `ARCHITECTURE.md`
covers why a single verified source of truth matters enough to justify the
extra effort.

---

## Status

Actively developed alongside a real job search. `framework/` is being extracted
from a working personal instance rather than designed in the abstract, so it
reflects what actually held up under repeated use, not a theoretical best practice.
Current state and what's still in progress: see `ARCHITECTURE.md`.

---

## License

Not yet decided. Treat as all-rights-reserved until a license file is added.
