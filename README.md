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

1. Read `framework/CONTRACT.md` for the full list of files `private/` needs to
   provide, and their exact shape.
2. Copy each template from `framework/templates/` into your own `private/`
   directory (gitignored by the root `.gitignore` already) and fill it in with
   your real information.
3. Point an AI assistant with file access at the repo root and have it read
   `SESSION_INIT.md` first, every session.
4. Load only the `framework/skills/` files relevant to what you're doing that day,
   rather than the full methodology, to keep sessions fast and focused.

---

## Status

Actively developed alongside a real job search. `framework/` is being extracted
from a working personal instance rather than designed in the abstract, so it
reflects what actually held up under repeated use, not a theoretical best practice.
Current state and what's still in progress: see `ARCHITECTURE.md`.

---

## License

Not yet decided. Treat as all-rights-reserved until a license file is added.
