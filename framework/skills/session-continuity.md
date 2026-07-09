# Skill: Session Continuity

**Load when:** starting any new session in this workspace, before any other task.

**Depends on:** `private/skills/session_init.md` (the stable map, itself a skill
file, see below for why) and whichever file the private instance uses as its
dynamic log (e.g. `private/data/session_log.md`).

---

## The problem

An assistant with no persistent memory across sessions defaults to one of two
failure modes: starting from zero and repeating already-completed work, or
worse, quietly re-deciding something that was already carefully settled,
without anyone noticing a reversal happened. Both are expensive. The second is
more dangerous, because it doesn't look like a mistake in the moment.

## The pattern: a fixed entry point, read first, every time

A generic root file (this repo's own public `SESSION_INIT.md` is itself an
example) states the checklist: what to read, in what order, before doing
anything else. It also checks whether a private, filled-in version exists, a
skill file, not a special standalone file category, and loads it if present;
if it doesn't exist yet, that's the signal this is a fresh clone with no
private instance set up. That private skill carries the person-specific
version: where things live, and how the environment works.

Split that private skill's job into two files with two different lifecycles,
not one:

- **A stable map.** Directory structure, tool/environment quirks, pointers to
  where each kind of information lives. This changes rarely, only when the
  structure itself changes. This is the file safe to load once into a
  persistent context feature (a Claude Project's knowledge base, or similar)
  without needing to re-upload it every session.
- **A dynamic log.** What's currently decided, what's currently open, what
  changed recently. This changes every session, sometimes several times a
  session, and needs to be read fresh from the live repository rather than
  baked into static context. A dated, chronological entry file works well here
  (see `application-tracking.md`'s tracker pattern for a similar idea applied
  to structured data).

Conflating these two is the single most common way this pattern degrades. A
map file that also carries dated facts ("current strategy as of March," "open
threads as of last Tuesday") either goes stale the moment it's loaded into
static context, or turns into something that needs constant editing, at which
point it's not really serving as a stable map anymore. The tell is syntactic:
if a sentence needs a date or an "as of" attached to make sense, it belongs in
the log, not the map.

The log file should answer three questions on its own reading its most recent
entry, without requiring the reader to reconstruct them from a long history:

1. What is the current strategy, stated as a conclusion, not a narrative of how
   it was reached?
2. What is explicitly still open or undecided?
3. What was corrected recently, and why, so a stale assumption doesn't get
   silently reintroduced?

### The open-threads file

"Read the top entry" degrades on heavy days: a single date can accumulate
several entries, and the open items end up scattered across all of them rather
than sitting in whichever one happens to be on top. The fix is a second, even
smaller state file (an `open_threads.md` in the private instance's data layer)
that is overwritten — not appended to — at every session close: what's open,
what's due, who's owed a follow-up, and nothing else. The log stays the
append-only history; the open-threads file is the current-state view of it.
Read the open-threads file first at session start, then the log's top entry
for recent context.

Both files have tooling: `private/scripts/daily_log.py open` creates a cheap
working file for the day's notes, and `close` folds it into the log's top,
archives old entries, regenerates the tracker views, and makes (or amends) a
single dated commit — so a session's end-of-day obligation is one command
plus rewriting the open-threads file, not a bookkeeping ritual.

## Drift-prevention rules

Three rules, each earned by a real failure this pattern is meant to prevent
from recurring:

- **Policy changes land in the canonical file in the same session they're
  decided.** A revised constraint, default answer, or standing policy gets
  written into the canonical config (e.g. `profile.yml`) immediately — the
  session log entry references the change, it never substitutes for it. A log
  that records a decision the canonical file doesn't reflect is drift with a
  timestamp: a future session loading the canonical file as authoritative will
  apply the superseded rule.
- **Scrubbing a claim means searching everything, not just the obvious
  documents.** When an overclaim is added to the avoid list, grep the entire
  private instance for its phrasing — including sample copy and examples
  embedded inside skill files. A stale example in a methodology file is a
  reintroduction vector: future drafts pattern-match on the example, not on
  the positioning doc that corrected it.
- **Dated content lives in the data layer, never in methodology files.** If a
  sentence needs a date or an "as of" attached to make sense, it belongs in a
  state file — the session log, or a snapshot file with an explicit as-of
  header — not in a skill. Methodology files are loaded on the assumption that
  they're timelessly true; a snapshot embedded in one goes stale silently,
  with no header to warn the reader.

## Loading only what's relevant

A second continuity failure shows up at scale, not on day one: a single
methodology document accumulates sections over many sessions until reading it
in full, every session, regardless of what the session is actually about,
becomes the dominant cost. The fix is decomposition: many small, single-purpose
files, each stating plainly at the top when it applies, loaded only when the
task at hand needs it.

This is the reason this skill file, and its siblings, exist as separate files
rather than sections of one large document. The session-init skill functions
as the index: it does not contain the methodology, it says which smaller file
contains the methodology relevant to today's task. It's the one exception to
"loaded on demand", it loads unconditionally, every session, before task
relevance is even known, precisely because its job is telling you what else
to load.

## When something might contradict an earlier decision

Check the actual record before overriding it. A summary of an earlier decision,
including one generated by the assistant itself, can lose the specific reasoning
that made the decision correct in its original context. If a new session's
instinct seems to conflict with something already settled, that's a signal to
verify against the source (a prior document, a transcript, the session log)
rather than trusting either the new instinct or a remembered summary by default.
