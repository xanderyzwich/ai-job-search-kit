# Skill: Framework Audits

**Load when:** closing out a maintenance batch, or auditing whether the docs
still match reality — after any split, move or rename.

**Depends on:** `framework-maintenance.md` (the ripple map says what a change
owes; this says how to check the batch actually paid it).

---

## The three closing audits

End every maintenance batch by asking, and actually checking:

1. **Do the human-readable docs match reality?** Both READMEs, QUICKSTART,
   both directory trees, CONTRACT — against the actual filesystem.
2. **Is every script wired to its moment?** Named in the task-time skill
   that governs when it runs, and in the always-loaded private map — not
   just in setup docs.
3. **Can every role actually do its job with what it loads?** See below. Run
   this one after any split, move, or rename — it is the only audit here that
   asks about READERS rather than files.

If an audit finds nothing, say so and stop; if it finds something, the fix
belongs in the same batch, not a someday list.

### Splitting a file safely

A split is the operation where content disappears without anyone noticing,
because nothing errors and the result looks finished.

1. **Account for the lines**, section by section: what left the source should
   equal what arrived, allowing for added headers.
2. **Then check the destination is LIVE.** Line accounting alone is not enough
   and has already failed once: a split's arithmetic balanced perfectly while
   three blocks of real methodology sat in a scratch directory, counted as
   accounted-for because they had moved *somewhere*. **Somewhere is not
   somewhere a reader will ever load.** Grep a distinctive phrase from each
   moved block and confirm it resolves to a file a role actually loads.
3. **Read the seams.** A mechanical split cuts paragraphs in half. Twice in one
   day a boundary rule left an orphaned sentence behind — a dangling "This
   compounds the standing risk…" with its antecedent now in another file. Line
   counts cannot see this; only reading the edges can.
4. **Re-point inbound references in the same batch**, and run the reference
   check. A moved file breaks links silently.
5. **Re-run the leak scan per moved section**, not once at the end. N new files
   is N new chances to put private content in a public one.

### Audit 3 — trace a role, not a file

Audits 1 and 2 ask whether the files are right and whether they are reachable.
Both can pass while a role is unable to work, because neither asks what any
particular reader ends up holding. On 2026-10-06 every structural check passed
— valid headers, resolving references, planned sizes — while **three roles were
missing inputs they could not function without**, including one whose skill
documents a real failure caused by exactly the input that had been left out.

For each role in turn:

1. **Write down what it must DO**, from the flow, in one line. Not what it
   loads — what it produces.
2. **List what it loads**, resolving every path. An input that does not exist
   is the cheap failure and the structural checks already catch it.
3. **Close the list transitively.** For every skill it loads, read that skill's
   `Depends on:` and confirm each name is also in the role's list. This is
   where the 2026-10-06 defect was: a role loaded the scoring skill and none of
   the six things that skill declares it needs.
4. **Ask the judgment question the script cannot:** given ONLY this, could the
   reader produce what step 1 says it must? Read the files and answer honestly.
   The failures look like a rule filed under the wrong reader — present in the
   repo, absent from the one role that performs it.
5. **Check for two documents disagreeing about who does what.** Closing a list
   transitively tends to surface these: one file says the scorer deduplicates,
   the flow says the coordinator does, and following both means an agent
   repeating finished work with hundreds of lines of state it should never have
   loaded.
6. **Record the load size per role.** Not a pass/fail — a cost. A role that is
   expensive for a good reason (honest matching needs the whole verified
   record) is different from one that is expensive by accident.

**Why this is not a script.** The mechanical half — resolve the paths, check
the transitive closure — could be automated, and it would have caught the worst
defect. It is not automated yet because the load lists are prose in a table,
and making them machine-readable means either parsing that prose, which is
fragile, or adding a structured copy, which is a second source of truth about
the same thing. **If those lists ever become structured for another reason,
build the check that day.** Until then the procedure above finds more than the
script would, because step 4 is the half that matters and no parser can do it.
