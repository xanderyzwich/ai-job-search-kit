# CLAUDE.md — ai-job-search-kit

**This file auto-loads. It is a ROUTER, not a manual.** Everything it points at
is longer and more current than anything restated here would be, so it names
where things live and how to find them, and nothing else. It carries no counts,
no skill list, no script list, and no methodology — those are generated or owned
elsewhere, and a copy here would rot.

This repo is a public-safe framework for running a job search as a structured,
multi-session collaboration with an AI assistant.

---

## Two repos, one directory

```
ai-job-search-kit/          ← PUBLIC repo. The reusable framework.
├── framework/              canonical skills, scripts, templates, CONTRACT.md
├── README.md  ARCHITECTURE.md  QUICKSTART.md  CHANGELOG.md  SESSION_INIT.md
└── private/                ← SEPARATE, PRIVATE repo. Gitignored from the public one.
                              The actual search: data, tracker, resume, instance skills.
```

They are committed and pushed **independently**. `private/` is listed in the
public `.gitignore` — it is not a submodule and its contents never appear in the
public repo.

**THE BOUNDARY, which is the one mistake here that cannot be undone:** nothing
under `framework/` or at the public root may contain a real dollar figure, a
real company name from the search, a real person's name or contact, or anything
else specific to one person rather than to the general method. When a framework
file needs a personal value it names the variable ("the candidate's salary
floor") and reads the number from `private/profile.yml` at runtime.

**Run `git status` and actually read it before any `git add` in the public
repo.** Do not assume `.gitignore` caught a new file or a new file type. A leak
scan over changed files — grepping for currency symbols, employer names and
personal names — costs seconds and has caught a real leak.

---

## Start here, every session

```bash
cd private && python3 scripts/daily_log.py open
```

That one command creates the day's working file, prints anything waiting (an
open cross-harness handoff, a sweep left open, the count of scored roles never
applied to), and **regenerates `private/temp/context_map.md`.**

---

## How to find a skill or a script — do this before inventing either

**`private/temp/context_map.md` is the index.** It is generated fresh at every
`open` from the files themselves, never hand-maintained, and it contains:

- **every skill** in `framework/skills/` and `private/skills/`, each with the
  trigger for when to load it;
- **every script** in `framework/scripts/` and `private/scripts/`, each with the
  one-line job it does;
- the **ripple map** — what else to touch when you change a framework file.

**Read it before you design a process, score something, write a document, or
write a one-off query. The answer is usually already a skill or already a
command.** The failure mode is not that the map is missing; it is that a session
generates it, prints one line, and forgets it exists while context compaction
drops the older output.

If the map is absent, both halves are discoverable directly — skills by their
`Load when:` header, scripts by their first docstring line:

```bash
grep -rA2 --include='*.md' '^\*\*Load when' framework/skills private/skills
```

---

## The files that own what this one deliberately does not

| for | read |
|---|---|
| full layout, startup checklist, public/private rules | `SESSION_INIT.md` |
| this instance's scope, overrides and footguns | `private/CLAUDE.md` |
| the instance's own manual — loads first, every session | `private/skills/session_init.md` |
| what `private/` must contain, and every schema | `framework/CONTRACT.md` |
| what to touch when changing the framework itself | `framework/skills/framework-maintenance.md` |
| why it is built this way | `README.md`, `ARCHITECTURE.md` |

---

## Standing rules

These are the rules here. If a `CLAUDE.md` in any parent directory is also
loaded, it belongs to different work and **does not govern this repo** — where
the two disagree about this kit, this file and `private/CLAUDE.md` win. Do not
assume such a file exists; usually none does.

- **Never push.** No `git push`, no remote writes, no `gh` write commands. The
  owner pushes both repos themselves.
- **Commit freely.** In this kit the commit IS the safety mechanism — the
  daily-log tool makes or amends one commit per day and every checkpoint is a
  `git checkout --` recovery point. A rule from elsewhere that forbids
  committing would disable recovery entirely; it does not apply here.
- **Both repos stay on `main`.** No branching, no checkouts.
- **If you clobber a file, recover it from git. Never reconstruct it from
  memory.** `git show <commit>:<path>` or `git checkout -- <path>`. Only work
  since the last checkpoint is unrecoverable.
- **Never submit an application without the owner reviewing it first**, and
  never choose which roles to apply to unilaterally — present the list and let
  them pick.
- **Generated files are never hand-edited.** Fix the source and regenerate.
  `private/data/application_history.md` comes from the tracker;
  `private/temp/context_map.md` comes from the skill and script headers.
