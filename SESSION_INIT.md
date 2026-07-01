# Session Initialization — ai-job-search-kit

The startup checklist for any session with Claude in this workspace. This file is
generic and safe to be public: it describes the pattern, not any person's data.
Personal specifics (comp floor, constraints, current positioning, open threads) live
in `private/SESSION_INIT.md` and `private/profile.yml`, both gitignored.

**Repo purpose:** a public-safe framework for running a job search as a structured,
multi-session collaboration with an AI assistant. `framework/` is the reusable system
(portfolio-visible, tracked in git). `private/` is the user's actual data (its own
gitignored repo, never committed here). See `README.md`, `ARCHITECTURE.md`, and
`framework/CONTRACT.md` for the full pitch, design rationale, and the exact file
contract `private/` is expected to satisfy.

---

## Directory Location

```
ai-job-search-kit/
├── README.md              — portfolio pitch: what this is, why it exists
├── ARCHITECTURE.md        — how the pieces fit together, design decisions
├── SESSION_INIT.md        — this file (generic, public)
├── .gitignore             — excludes private/, output/, temp/
│
├── framework/             — the reusable system (tracked in git, no personal data)
│   ├── skills/              small, focused methodology files, loaded on demand
│   ├── scripts/              generators (e.g. resume builder), parameterized
│   └── templates/            blank versions of tracker.csv, experience-summary.md, etc.
│
├── private/               — the user's actual data (GITIGNORED — its own git repo)
│   ├── SESSION_INIT.md      personal overlay: current positioning, open threads
│   ├── profile.yml          structured personal data: comp floor, constraints, lanes
│   ├── experience_summary.md   verified source of truth
│   ├── job_search_skill.md           full personal workflow doc (being decomposed)
│   ├── job_tracker.csv               application log
│   └── (resumes, cover letters, build scripts)
│
├── output/                — generated deliverables (GITIGNORED)
└── temp/                  — scratch (GITIGNORED)
```

---

## Session Startup Checklist

Run in order at the start of every session:

1. **Read `private/profile.yml`** — the structured facts (comp floor, constraints,
   lane definitions, title lists). Framework skills reference these as variables;
   never hardcode a personal figure into anything that could end up in `framework/`
   or the public repo root.
2. **Read `private/SESSION_INIT.md`** — current positioning and open threads.
3. **Read `private/experience_summary.md`** — the verified backbone.
4. **Load only the `framework/skills/` files relevant to the task at hand** (see each
   skill's one-line description in its own header — don't load all of them by default).
5. **Read `private/job_tracker.csv`** if the task touches applications.
6. **Confirm browser** (if doing browser work): run `list_connected_browsers`.
7. **Ask which thread** — resumes, warm outreach, new role search, or applications.

---

## The public/private boundary (read this before writing to any file)

Before writing content into anything under `framework/`, `README.md`,
`ARCHITECTURE.md`, or this file: if it contains a real dollar figure, a real company
name from the user's search, a real person's name or contact info, or any other
data specific to one person's search rather than the general method, it belongs in
`private/`, not here. When a framework skill needs a personal value, reference it as
a variable (e.g. "the candidate's salary floor") and pull the actual number from
`private/profile.yml` at runtime — never inline it.

Before any `git add` or `git commit` in this (public) repo: run `git status` and
read the output. Don't assume the `.gitignore` caught everything, especially right
after creating a new file or file type.

---

## What to Update Each Session

End-of-session, update `private/SESSION_INIT.md` (open threads, positioning changes)
and `private/job_search_skill.md` or its decomposed skill files (session notes, new
facts). If a change is generally useful — a better search pattern, a refined
triage rule — consider whether it belongs in `framework/skills/` too, generalized
and stripped of personal specifics, so the public side of the repo stays current.
