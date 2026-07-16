# Template: session_init.md
#
# Copy this to private/skills/session_init.md. This is the one skill file
# that loads every session unconditionally, unlike everything else in
# skills/, which loads only on demand. See
# framework/skills/session-continuity.md for the full reasoning.
#
# This file is meant to be stable enough to load once into a persistent
# context feature (a Claude Project's knowledge base, or similar) and mostly
# forget about. If you're about to add something to this file that needs a
# date attached to make sense ("as of," "currently," "this week"), that's
# the signal it belongs in your session log file instead, not here.

# Skill: Session Init

**Load when:** every session, first, before any other task.

**Depends on:** `profile.yml`, `experience_summary.md`, and whichever file
you use as your dynamic session log (see
`framework/skills/session-continuity.md` for why that should be a separate
file from this one).

---

## Directory map

Sketch your actual `private/` layout here if it differs from the default
(`skills/`, `feedback/`, `resume/` subdirectories described in
`framework/CONTRACT.md`). If you're using the default layout, this section
can just point back there instead of repeating it.

## Startup checklist

Adapt this to your actual file names, but the shape holds:

1. Read `profile.yml`, the structured facts.
2. Read your open-threads / current-state file and the top (most recent)
   entry of your session log — what's open and due, plus recent positioning.
3. If your instance has the daily-log tool, run its `open` step: it creates
   the day's working-notes file and regenerates a gitignored
   `temp/context_map.md` — skill routing plus the ripple map. Read that map;
   before editing any `framework/` or root-doc file, consult its ripple
   section and touch every mirror it names in the same batch. (No daily-log
   tool yet? Run `framework/scripts/build_context_map.py` directly.)
4. Read `experience_summary.md`, the verified backbone.
5. Read `framework/README.md` — the small index of the public half; it
   routes to skills, templates (canonical shapes for every generated file
   type — check before creating any file), and scripts. Then load only the
   `framework/skills/` files relevant to the task at hand.
6. Read your tracker file if the task touches applications.
7. Confirm any browser or tool state your workflow depends on.
8. Ask which thread you're picking up, if it's not already obvious.

## Where to find current state

Point to the actual files: which one has your current positioning and
strategy, which one has open threads and recent history, which one has
verified facts. Don't restate the content here, just say where it lives.

## Tool Notes (your environment specifics)

Whatever is specific to your actual setup: which tools you use for browser
automation or file access, environment quirks, usernames, anything a session
needs to know before touching your actual machine or accounts that isn't
captured elsewhere.

## What to update each session

State plainly: update your session log at the end of every session, and
leave this file alone unless the directory structure or your tool
environment itself changed.
