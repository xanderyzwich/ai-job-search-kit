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

**Both `SESSION_INIT.md` files (this one and `private/SESSION_INIT.md`) are meant
to be stable.** If you're using this framework with a persistent context feature
(Claude Projects or similar), these are the files to load there once, they should
rarely need editing. Neither one carries current, dated state, that lives in
`private/skills/session_log.md` (or wherever the private overlay's own skill files
put it), which is read fresh each session rather than baked into static context.
If a fact needs a date attached to it ("as of," "currently," "this week"), it
belongs in the log, not in either init file.

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
│   ├── SESSION_INIT.md      personal overlay: directory map, environment/tool notes.
│   │                        Stable, see the note above; not where current state lives.
│   ├── profile.yml          structured personal data: comp floor, constraints, lanes
│   ├── experience_summary.md   verified source of truth
│   ├── job_tracker.csv               application log
│   ├── skills/                        filled methodology, one file per concern, includes
│   │                                  session_log.md, the actual current-state log
│   ├── feedback/                      external input received along the way
│   └── resume/                        generated resumes and their build scripts
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
2. **Read `private/SESSION_INIT.md`** — the directory map and tool notes. Then read
   the top (most recent) entry of `private/skills/session_log.md` for current
   positioning and open threads, that's the file that actually changes session to
   session.
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

End-of-session, update `private/skills/session_log.md` with a new dated entry
(open threads, positioning changes, what happened). Leave `private/SESSION_INIT.md`
alone unless the directory structure or tool environment itself changed, that file
is meant to be stable. If a change is generally useful — a better search pattern, a
refined triage rule — consider whether it belongs in `framework/skills/` too,
generalized and stripped of personal specifics, so the public side of the repo
stays current.
