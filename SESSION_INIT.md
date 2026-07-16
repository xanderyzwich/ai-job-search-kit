# Session Initialization — ai-job-search-kit

The startup checklist for any session with Claude in this workspace. This file is
generic and safe to be public: it describes the pattern, not any person's data.

**Repo purpose:** a public-safe framework for running a job search as a structured,
multi-session collaboration with an AI assistant. `framework/` is the reusable system
(portfolio-visible, tracked in git). `private/` is the user's actual data (its own
gitignored repo, never committed here). See `README.md`, `ARCHITECTURE.md`, and
`framework/CONTRACT.md` for the full pitch, design rationale, and the exact file
contract `private/` is expected to satisfy.

**This file, and its private counterpart, are meant to be stable.** If you're
using this framework with a persistent context feature (Claude Projects or
similar), these are the files to load there once, they should rarely need
editing. Neither one carries current, dated state, that lives in the private
instance's session log, read fresh from the live repository each session
rather than baked into static context.

---

## First step: check for a private session-init skill

Before anything else, check whether `private/skills/session_init.md` exists.

- **If it exists**, load it. It's self-sufficient, directory map, startup
  checklist, and tool notes for this person's actual setup, and it supersedes
  the generic checklist below. Follow it instead.
- **If it doesn't exist**, there's no private instance set up yet — this is a
  fresh clone, and setting one up is your first task, before anything else.
  Read `QUICKSTART.md` (or run `framework/scripts/bootstrap.py`), which
  generates `private/skills/session_init.md` from
  `framework/templates/session_init.md`. Then personalize that generated file
  — your directory map, where your state lives, your tool notes. From the next
  session on it supersedes this generic checklist permanently; you won't run
  the steps below again. Until it exists, the generic checklist below is the
  fallback and assumes `private/` has at least been scaffolded.

---

## Directory Location

```
ai-job-search-kit/
├── README.md              — portfolio pitch: what this is, why it exists
├── ARCHITECTURE.md        — how the pieces fit together, design decisions
├── CHANGELOG.md           — the framework's public history
├── SESSION_INIT.md        — this file (generic, public)
├── QUICKSTART.md          — step-by-step setup for a fresh clone
├── LICENSE                — MIT
├── .gitignore             — excludes private/, output/, temp/
│
├── framework/             — the reusable system (tracked in git, no personal data)
│   ├── README.md            the public half's index — routes to skills,
│   │                        templates, and scripts; read at session start
│   ├── skills/              small, focused methodology files, loaded on demand
│   ├── scripts/              working tooling: bootstrap, resume renderer,
│   │                         history generator, daily-log tool, funnel report,
│   │                         context-map builder
│   └── templates/            blank versions of profile.yml, session_init.md, etc.
│
├── private/               — the user's actual data (GITIGNORED — its own git repo)
│   ├── profile.yml          structured personal data: comp floor, constraints, lanes
│   ├── experience_summary.md   verified source of truth
│   ├── job_tracker.csv               application log — the only hand-edited
│   │                                  application record; other views are generated
│   ├── skills/                        filled methodology, one file per concern.
│   │                                  Includes session_init.md (the stable map,
│   │                                  loaded first). Methodology only — no state.
│   ├── data/                          working state: session_log.md (the dynamic
│   │                                  log), open_threads.md (read at startup),
│   │                                  dated snapshots, per-company briefs, and
│   │                                  generated views of the tracker
│   ├── scripts/                       history generator + daily-log tool
│   ├── feedback/                      external input received along the way
│   └── resume/                        generated resumes and their build scripts
│
├── output/                — generated deliverables (GITIGNORED)
└── temp/                  — scratch (GITIGNORED)
```

---

## Generic Session Startup Checklist

Only relevant if `private/skills/session_init.md` doesn't exist yet, meaning
there's no private instance to load its own checklist from. Once one exists,
it supersedes this section.

1. **Read `private/profile.yml`** — the structured facts (comp floor, constraints,
   lane definitions, title lists). Framework skills reference these as variables;
   never hardcode a personal figure into anything that could end up in `framework/`
   or the public repo root.
2. **Read `private/data/open_threads.md` and the top entry of
   `private/data/session_log.md`** if they exist — what's open and due, plus recent
   context. A brand-new instance won't have these yet; that's expected.
3. **Regenerate and read the context map**: run
   `python3 framework/scripts/build_context_map.py`, then read
   `private/temp/context_map.md` — skill routing plus the ripple map. Before editing
   any `framework/` or root-doc file, consult its ripple section and touch every
   mirror it names in the same batch. (Once your private instance has the daily-log
   tool, its `open` step does this for you automatically.)
4. **Read `private/experience_summary.md`** — the verified backbone, if the task
   produces any content about the candidate.
5. **Read `framework/README.md`** — the index of the public half; it routes to
   skills, templates, and scripts. Then load only the `framework/skills/` files
   relevant to the task at hand. One call scans every skill's routing:
   `grep -rA2 --include='*.md' '^\*\*Load when' framework/skills private/skills`.
6. **Read `private/job_tracker.csv`** if the task touches applications.
7. **Confirm browser** (if doing browser work): run `list_connected_browsers`.
8. **Ask which thread** — resumes, warm outreach, new role search, or applications.

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

End-of-session, update the private instance's session log (a new dated entry:
open threads, positioning changes, what happened). Leave `private/skills/session_init.md`
alone unless the directory structure or tool environment itself changed, that file
is meant to be stable. If a change is generally useful — a better search pattern, a
refined triage rule — consider whether it belongs in `framework/skills/` too,
generalized and stripped of personal specifics, so the public side of the repo
stays current.
