# Skill: Framework Maintenance

**Load when:** changing the system itself — adding or renaming skills,
scripts, templates, directories, or schema columns; syncing documentation
after a structural change; or auditing whether the docs still match reality.

---

## Why maintenance is its own skill

This system describes itself in several places: two READMEs, two directory
trees, a contract, a quickstart, a bootstrap script, and an always-loaded
session map. Self-description drifts exactly the way any other mirror
drifts — a structural change lands, four of the seven descriptions get
updated, and the other three quietly start lying. The fixes below were all
earned during real maintenance sessions; this file exists so the next one
doesn't rediscover them.

## When something should happen and nothing triggers it, that is the skill

**A gap in this system almost never looks like a missing rule. It looks like a
correct rule nobody loads**, because its trigger does not match the event that
should fire it.

**The diagnostic, in the owner's words:** *if there is something that should be
done and the trigger doesn't already exist, create a skill for that trigger.*

**The worked example, 2026-10-20.** Two threads went wrong in a week — one
state file said a thread was waiting on someone who had already answered, and
two live interview stages never reached the index read first at every session.
Both looked like discipline failures. Neither was. **The procedure was written
down, correctly, and had been for months — inside the skill for preparing and
debriefing a CALL.** Almost nothing that changes the state of a search is a
call; that week's changes arrived as rejection emails, a text, a scheduling
invite and several direct messages. **The rule was correct, current, and behind
a door those events never knock on.**

**So the test when something goes wrong: before writing a new rule, check
whether the rule already exists and ask what would have had to happen for
someone to read it.** If the answer is "an event that did not occur", the fix is
a new trigger, not new content — and often the content can simply move.

**Name the trigger after the thing that actually happens**, in the words someone
would use when it happens. *"A communication lands or goes out"* is a trigger.
*"Keeping records consistent"* is a topic, and nobody loads a topic.

**A good sign you have found a real one: it is a sentence the person already
says out loud.** The example above became a skill because *"I have some comms to
log"* opens half of these sessions and had no procedure attached to it.

## Is it a skill or is it data? Ask who EXECUTES it

**The test is not "does it have a trigger." It is "who acts on it."**

- **A skill is something the ASSISTANT does.** An agent loads it mid-task and
  acts: filling a form, sweeping a surface, scoring a posting, running a ritual.
- **Data is something the PERSON reads.** It informs a decision or a
  conversation the assistant is not party to and cannot execute.

**This was got wrong on 2026-10-19 and the error is instructive, because the
file passed every structural check.** Per-platform notes for automated coding
assessments were filed as skills. They had a clean `Load when`, they were
addressed by name the way the board and ATS directories are, they carried real
measured findings, and they linted clean. **They were still data**: nobody but
the candidate ever opens them, because no agent sits a coding assessment.

**Why the resemblance is so convincing, and worth naming so it does not recur:**
the vendor-shaped directories really are skills — a board file is loaded by the
agent running the sweep, an ATS file by the agent filling the form. An
assessment file is shaped identically and loaded by a human on their way into a
room the assistant cannot enter. **Same shape, different executor, different
home.**

The owner's formulation, which is the one to keep: **"skills are for Claude to
do things; data is informational."**

Practical consequence when this is misjudged: the misfiled thing drags routing
machinery behind it. The 10/19 error also added the directory to the context
map's collapse list, which had to be reverted — **a file in the wrong half pulls
index and ripple changes with it, so the test is cheaper to apply before
writing than after.**

## Method travels; research about one employer does not

**A second test, and it cuts across the first.** "Is it a skill or is it data?"
asks who EXECUTES something. This one asks **where it still applies** — and a
section can pass the first test and still be in the wrong file.

A question bank in a call-prep skill held both halves at once: a list of likely
questions sourced from third-party guides for ONE employer, and a rubric for
what a senior loop is actually scoring. **Both are method by the first test.**
Nobody but the reader executes either. But the rubric travels to every interview
the candidate will ever have, and the question list is research about one
company's hiring process — which belongs in that company's brief, beside
everything else known about them, and which goes stale the moment that thread
closes.

**The tell is a proper noun in a rule.** When a sentence of method cannot be
written without naming a specific employer, board or platform, it is usually
research wearing method's clothes. Conventioned directories already encode this
for whole files — one per board, one per ATS vendor — and the same split applies
*inside* a file: keep the rule, move the named instance to the record that owns
that name.

**The costs differ.** Method that travels is loaded often, so it should be short
and durable. Research about one employer is loaded once, by one reader — in a
skill it charges everyone else, and nobody updates it when that process changes.

## A skill holds what the task needs, not what happened

A skill file contains only what the assistant needs to complete the task it is
loaded for, plus the guards that keep it off unwanted tangents. **Learnings
belong in a skill. State and history do not.** Counts as of a date, probe logs,
queue contents, "this claim was withdrawn" narratives and the story of how a
rule was found are records, and records live in dated data files with an as-of
header.

**The test:** if this paragraph were deleted, would an agent doing the task get
it wrong? If not, it is history or state and belongs in data. A learning is the
rule stated in the present tense with the one-line reason it exists; the
account of the day it was discovered goes elsewhere.

**Why it matters:** every agent that loads a skill pays for all of it. A file
that is growing past the size warning should be suspected of carrying history
before anyone proposes raising the limit.

## The header contract (skill routing in one call)

Every skill file must deliver its complete routing information — the
`# Skill:` title and the full `**Load when:**` block — within its **first 8
lines**, with the Load-when itself at most 3 lines. Not by padding to a
fixed length; by budget. The point is that one command scans every skill's
routing without truncation, so choosing what to load costs one tool call:

```bash
grep -rA2 --include='*.md' '^\*\*Load when' framework/skills private/skills
```

(or `head -n 8` per file, guaranteed sufficient by the same budget). A
Load-when that outgrows 3 lines is usually a skill trying to cover two
concerns — split it before padding it.

**`framework/scripts/lint_skills.py` checks this mechanically, and the daily-log tool
runs it at `close`** so the check happens at a ritual rather than on request.
It ERRORS on what breaks the scan — a missing routing header, or one below the
line budget — **and on a backticked file reference that resolves to nothing**,
which is how a move or rename announces itself. It WARNS on the rest, including
file size. The size
warning is how the next oversized file announces itself: the one that prompted
all this had reached 2,207 lines before anyone measured it.

**Keep the error set narrow.** The first version of that script also errored on
a literal title prefix and on any Load-when over three lines, and would have
forced churn across fifteen files for two things that were not problems — an
instance may title its skills in its own house style, and a fourth line is
usually a disambiguation clause worth keeping.

## The context map (generated at session start — read it first)

`daily_log.py open` runs `build_context_map.py`, which materializes the
ripple map (kept in `framework-ripple-map.md`) plus every skill's `Load when` header into
`private/temp/context_map.md` (gitignored, rebuilt each session — a view,
never a source). It exists so "what do I touch when" is in context from the
first moment instead of depending on a remembered header scan: this was
added after a documentation ripple was missed because the routing scan is a
session-start ritual and the edit that needed it arrived as a mid-session
pivot. Before editing any `framework/` or root-doc file, read that file's
obligations in the ripple section and touch every mirror it names in the same
batch. The generator EXTRACTS the section from `framework-ripple-map.md` verbatim rather than
re-encoding it, so that stays the one place the ripple map lives; it keys off
the section heading there, which fails loudly (an empty section) if the heading is renamed.

## The ripple map lives in its own file now

**`framework-ripple-map.md` holds the "when X changes, also touch Y" table**, moved out of this skill on 2026-11-17 because it is consulted AFTER a change and was 184 lines of a 468-line file. Walk it at the end of a batch, before the changelog entry and the close. A verbatim copy is generated into `private/temp/context_map.md` every session, so you rarely need to open it; open the file only to edit the table. Edit it THERE, not here.

## The changelog entry — what it owes, and how to rebuild one

**Any change to the mechanisms of this framework owes an entry, in the same
commit.** Not "a new skill" — that phrasing was the rule for a while and it is
why nine of fourteen framework-touching commits went unrecorded: most of them
added no skill at all.

**Trivial changes are exempt, but the exemption must be CLAIMED, not assumed.**
A reference rename, a typo, a path correction, a reflow — put
`[no-changelog: <reason>]` in the commit message. `check_changelog.py` counts
claimed exemptions separately and prints the total, so "trivial" cannot quietly
become the default. If the mechanism changed, it is not trivial, however small
the diff.

### Write the body, not just the entry

**An entry inherits its commit body's richness.** Measured on this repo: the
entries that survived being written up later came from commit bodies of 200–425
words; the one that came out thin came from a body of 41. Authorship and timing
were coincidences — body length was the variable.

So the preservation mechanism is the commit body. It should carry **what
changed, what forced it, and the numbers** — the measurement, the failure, the
count. Anyone writing the entry later, including you next week, has only what
the body says.

### Who the entry is written for

**Someone who was not there, does not have the repo checked out, and is reading
this file on its own.** That is the actual audience: the changelog is the public
record of why this framework looks the way it does, and for a portfolio-visible
repo it is often the only part anyone reads in depth. A commit message is not a
substitute — nobody reads a git log to learn a system's reasoning — and neither
is a diff, which the reader does not have open.

Three consequences:

- **Name the problem, not just the fix.** What was going wrong, what it cost,
  and how it was noticed. A reader learns more from "nine of fourteen commits
  had no entry, and the misses skewed toward fixes" than from "improved
  changelog coverage."
- **Keep the numbers.** They are what make an entry credible rather than
  decorative, and they survive anonymisation: *one of twenty-one requisitions*,
  *2.2K tokens against 149K*, *0 for 12*. Strip the employer, keep the
  measurement.
- **Do not polish the failures out.** The portfolio value is in the failures
  being visible and honestly described — a record that only contains successes
  reads as marketing and teaches nobody anything. An entry that says a first
  attempt was wrong, and why, is worth more than one that implies the design
  arrived finished.

**The filter for what deserves one is not diff size.** It is *would someone
otherwise relearn this the hard way*. A reorganisation is visible in the tree; a
silent failure mode is not, and the silent ones are exactly what gets
rediscovered expensively. The historical misses skewed toward fixes and
follow-ups for precisely this reason — they felt small and carried the most
transferable content.

### Rebuilding an entry after the fact

In this order, and stop when you have the mechanism and the numbers:

1. **The commit body.** Read the FULL message — subject and body. A rich body
   usually contains the entry already.
2. **The session log for that date.** This is the recovery when the body is
   terse, and it is where people look last. One thin entry here was missing the
   measurement that gave its change the whole point — a single keyword returning
   one of twenty-one open requisitions — and that number had been in the day's
   log all along.
3. **The diff.** Last resort. It tells you what changed and never why, which
   produces text that reads like a record and carries nothing.

**If none of those yield a reason, write a short honest entry or none at all.**
A thin entry is worse than an absence, because it stops the next person looking
further.

**Cite what you backfill.** A late entry names the commits it covers:
`<!-- covers: abc1234 · backfilled YYYY-MM-DD -->` — invisible in rendered
Markdown, greppable in source, and the hash is verified to resolve so a typo
cannot read as covered forever. Written-at-the-time and backfilled are counted
separately on purpose; collapsing them hides the only signal worth watching.

**Do not chase history.** The rule has a start date and commits before it are
reported as predating it. Backfilling months of history from diffs alone
produces a wall of thin entries that look like records.

## Change workflow

1. **Order the work:** rules/structure first, data corrections second,
   enhancements third — one commit per activity, so each is reviewable and
   revertable on its own.
2. **Replacing a generator:** fidelity gate before the swap — compare old
   and new output mechanically (text, styles, whatever the artifact
   carries), and verify the checked-in artifacts match the OLD generator
   first, so no manual edit gets silently clobbered.
3. **Migrating live data:** copy the file to `temp/` first. One-off
   migration scripts live in `temp/` and get deleted after they run;
   they're scaffolding, not tooling.
4. **Every public commit:** run `git status` and read it, then grep the
   new/changed public files for personal data. The `.gitignore` is a
   backstop, not the check.

## Closing a batch — the audits live next door

**Every maintenance batch ends with the three closing audits**, and they are in
`framework-audits.md` rather than here. They are a different moment: this file
is read WHILE changing something, the audits are read AFTER, and carrying both
made every mid-edit lookup pay for seventy-seven lines it would not use.

**It also holds `Splitting a file safely`** — read that BEFORE any split, not
after, because a split is the operation where content disappears while nothing
errors and the result looks finished.
