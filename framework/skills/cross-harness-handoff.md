# Skill: Cross-Harness Handoff

**Load when:** switching between two agent harnesses mid-task — writing a
handoff before you stop, or consuming one when you pick up. Also load it when a
handoff is waiting and you do not know the protocol.

**Depends on:** the instance's handoff file (`data/handoff.md` in this repo's
private instance) and `daily_log.py handoff`.

---

## The problem this solves

Two harnesses with complementary gaps — one holds a browser and a logged-in
session, the other holds long-context refinement and scripted file work — split
a single day's work **mid-task, not between tasks.** State therefore has to
travel across the boundary, and the boundary is crossed many times a day.

**The failure is not lost files. It is unrecoverable knowledge of what the other
side already did.** Measured instance: one harness submitted four applications
and wrote good notes into the tracker; the next session in the other harness
learned of it by accident, during an unrelated query. Nothing was lost — but only
because that query happened.

## The critical design constraint

**Do not hang the trigger on session start.** A long-running session that
persists all day passes session-start once and never again, while switches
happen repeatedly. A handoff surfaced only at init will be missed every time
after the first.

**The reliable trigger is the human.** They are the one who knows a switch is
happening, because they are the one performing it. So:

- **The switch is REQUESTED, never inferred.** Nothing is owed to the handoff
  file between switches.
- **The receiving session's first action is to read it**, on being told a switch
  has occurred. One command, not a convention to remember.

## Writing one

1. **Write it BEFORE you stop.** The moment a switch is requested is the moment
   the context is still in hand.
2. **Checkpoint first** so the handoff points at committed state. A handoff
   referring to uncommitted work is a trap.
3. **Never overwrite an OPEN handoff.** If one is unconsumed, it was not acted
   on — say so rather than replacing it. Losing that record means losing whether
   its asks were ever done.
4. **It is a BATON, not a log, and not a to-do list.** The session log is the
   log; the tracker is the status; the open-threads file is the queue. This
   carries only what the next session must ACT on, now.
5. **Point, do not copy.** Reference the file that owns each fact. A handoff that
   restates content becomes a second copy that goes stale — the first draft of
   this protocol failed exactly that way, copying five pending items out of two
   other files into a body that would have been wrong within a day.
6. **Name what to send back.** If the answer is "nothing," say so explicitly.
   Silence is indistinguishable from an unfinished handoff.

## Shape

`FROM` · `TO` · `WRITTEN` · then four sections:

- **The ask** — the specific next action, not a topic. Numbered if there is more
  than one, in the order they should happen.
- **State** — what is committed, what is mid-flight and how far.
- **Watch** — traps the receiving side will hit. Cite the file that owns each.
- **Return** — what to write back, and where.

## Reading one

Run `daily_log.py handoff`. It prints an open handoff and does not consume it.

**It also re-indexes the skill map first, and that is the point of doing it
here.** A handoff means the other harness has been working — possibly adding or
editing skills — and a session that has run all day holds an index from whenever
it opened. Pickup is the one moment both sides know the repo has moved
underneath the reader, so it is the right place to rebuild.

**Consume by acting, then `daily_log.py handoff --clear`.** A stale OPEN handoff
is worse than none, because the next session acts on it twice.

## Boundaries worth knowing

- **A handoff written while the other session is already running does not
  surface on its own.** Tell that session to read it.
- **Urgent operational rules do not belong here.** A handoff is consumed once and
  cleared; a standing rule has to survive that. Put standing rules where the
  tooling states them unprompted, and leave the reasoning in a skill.

## If a sweep is open when you hand off

Sweeps usually run in whichever harness has a browser, and applications
usually run there too — so the harness that OPENS a sweep is normally the one
that closes it, and the baton does not need to carry sweep state.

The exception is a handoff mid-sweep, or one where the receiving side will do
the applying. An open sweep is live state in a file, and the counts needed to
close it (listings screened, how many were already tracked, rough minutes)
exist only in the head of whoever ran it. So: **if a sweep is open, say so in
`State`, with those three numbers.** Receiving a handoff that names an open
sweep means closing it with those numbers, not deleting the file — deleting
it throws away the only copy of a count nothing can rebuild.
