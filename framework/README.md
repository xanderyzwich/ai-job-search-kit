# framework/ — map of the public half

The index to everything below. A private instance's session init points
here once; new skills, templates, and scripts announce themselves by
adding a line to this file in the same commit that adds them, so the
always-loaded private map never needs editing to make new pieces
discoverable. Read it at session start — it's small on purpose.

No personal data lives anywhere in `framework/`.

- **`skills/`** — generic methodology, one file per concern (including
  `communications/`). Routing lives in each file's first 8 lines
  (`**Load when:**` — see the header contract in
  `skills/framework-maintenance.md`). Scan alongside the private
  instance's `skills/` at task time:
  `grep -rA2 --include='*.md' '^\*\*Load when' framework/skills private/skills`
- **`templates/`** — the canonical shape of every file type that has one
  (company brief, profile, experience summary, tracker schema, resume
  content, session init, feedback, and the per-surface skill shape used for
  one-file-per-board and one-file-per-ATS-vendor). State files (session log, open threads)
  start empty; generated views come from `scripts/`. **Rule: before creating any new file, check
  here — if a template exists, the file is created from it and keeps its
  sections.** Structural edits to an existing instance preserve the
  template's sections too.
- **`scripts/`** — canonical tooling. **Deliberately not listed here:** each
  script's first docstring line is its routing header, and the generated
  context map indexes them all from there, so a list in this file would be a
  mirror that rots. Installed copies live in the private instance's
  `scripts/`; `bootstrap.py`'s COPIES names which ones get installed, and
  after upstream changes, re-copy.
- **`CONTRACT.md`** — the exact file contract a private instance must
  satisfy for the framework to function.
