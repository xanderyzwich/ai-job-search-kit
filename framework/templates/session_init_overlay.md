# Template: session_init_overlay.md
#
# Copy this to private/SESSION_INIT.md. It's loaded alongside the public
# root SESSION_INIT.md every session — that one describes the generic
# pattern, this one carries your actual current state. See
# framework/skills/session-continuity.md for why this file exists and what
# problem it's solving.
#
# Keep this file current. Its whole value is answering "what's the state of
# things right now" without making a new session reconstruct it from a long
# history — update it at the end of a session, not just at the start of
# the next one.

# Session Initialization — private overlay

## Directory map (this repo)

If your private/ layout differs from the default (skills/, feedback/,
resume/ subdirectories), sketch it here so a new session doesn't have to
guess. If you're using the default layout, this section can just point back
to framework/CONTRACT.md instead of repeating it.

## Current Positioning

State this as a conclusion, not a narrative of how you got there — a new
session should be able to read this section alone and know where things
stand, without reconstructing the reasoning.

- **Target shape:** [what you're actually looking for, stated plainly]
- **Strategy:** [the current approach — which lanes, which channels, what's
  deprioritized and why]
- **Anything explicitly off the table:** [claims not to make, approaches
  already tried and rejected, anything a new session should not
  re-litigate]
- **Hard constraints:** pointer to `profile.yml` rather than restating the
  numbers here

## Open Threads

What's currently unresolved or in progress. Be specific enough that picking
this up cold, days later, doesn't require remembering the context — each
item should make sense read on its own.

- [thread one]
- [thread two]

## What changed recently

If something was corrected, reversed, or learned the hard way recently,
note it here explicitly, even briefly. This is the section that prevents a
stale assumption from quietly getting reintroduced by a session that
doesn't have the earlier conversation in context.

## Tool Notes (personal environment specifics)

Whatever is specific to your actual setup: which tools you use for browser
automation or file access, environment quirks, usernames, anything a
session needs to know before touching your actual machine or accounts that
isn't captured elsewhere.
