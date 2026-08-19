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

That entry point also materializes a session context map: if the instance
uses the daily-log tool, its `open` step regenerates a gitignored
`private/temp/context_map.md` holding skill routing (every Load-when header) and the
framework's ripple map, so "what to touch when" is in context from the start
rather than depending on a mid-session decision to go scan for it.

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

### Where init stops

The entry point ends by reporting, not by asking. Once the reads are done, state
what was found — script output, overdue cadences, the top of the open-threads
file, anything that changed since the last log entry — and then wait for the
person to say what they want, in their own words. A multiple-choice menu of
threads at the end of init reads as helpful and isn't: it makes the assistant's
guess at the shape of the day the frame the person has to answer inside, and the
one they actually wanted is usually the option nobody listed.

The same boundary applies to the work itself. Init is read-only orientation, so
the substantive work of the process — the sweeps, the submissions, the outreach,
any standing watch — waits to be asked for, even when a file calls the check
"daily" or "at session start." Read that cadence as "due the next time the
process runs," not as authorization to run it before the person has said a word.
Surfacing that something is due IS the deliverable; doing it unasked spends the
person's context on work they didn't choose, and buries the state report they
did.

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
- **A mutating write isn't verified until it's checked, and a git-tracked
  instance should checkpoint locally as work happens, not only at session
  close.** A write that's supposed to append or surgically edit can instead
  silently overwrite the whole file — the failure looks identical to success
  until the next read, so verify (a line count, a tail, a diff) before
  starting the next edit on that file. If the instance's state layer is
  git-tracked, take a local commit at the end of every unit of work,
  amending it as the day continues rather than stacking new commits, and
  push only once at actual close. That turns every checkpoint into a
  recovery point: a caught mistake costs only the mistake, not everything
  done earlier that session.

  **Define the trigger, or it won't fire.** "After each meaningful batch of
  edits" was the earlier wording here, and an undefined threshold reliably
  resolves to "not yet" — one session ran four discrete units of work and
  checkpointed once, at the very end, because each unit was individually easy
  to argue wasn't big enough. The usable trigger is **reporting**: when you are
  about to tell the person what you found or did, the edits behind that
  statement are a finished unit, so checkpoint first and then report. That
  boundary needs no interpretation and can't be quietly deferred, because
  reporting is unavoidable. Two secondary triggers: something expensive to
  reproduce has landed (re-deriving it is the cost being insured against), or
  the next thing is a different concern entirely.

  **One exception, and only one: never checkpoint a knowingly inconsistent
  state.** A half-mirrored change — content moved out of one file but not yet
  into its counterpart, a component added but its ripple not yet walked, a data
  edit whose generated view hasn't been regenerated — commits a contradiction,
  and that recovery point is worse than none, because reverting to it restores
  something broken. Finish the pair first. Since amending keeps N checkpoints
  as one commit, the marginal cost of checkpointing is seconds and the bias
  belongs firmly toward more often.

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
