# Skill: Browser Delegation

**Load when:** you are the agent doing browser work — harvesting listings,
fetching a posting a plain request could not, or filling an application form.

**Pairs with:** `agent-contracts.md` (what you must return). The coordinator
does not need this file; it needs only the decision to delegate, which lives in
`search-apply-ritual.md`.

---

**Split from the apply ritual on 2026-10-06, by READER rather than by topic.**
The *decision* to delegate belongs with the coordinator, in the ritual, where it
is made. The *mechanics* belong here, with the agent that executes them. Split
the other way and the ritual loses its trigger: a coordinator reads the steps
and never learns to delegate at all — which is exactly how an earlier
delegation rule sat unread in a long file for two months.

**Screenshots are the single largest consumer of a long session's context**, and
the fix is architectural rather than a matter of taking fewer of them. A
sub-agent's working context is discarded when it returns; only its report
reaches the parent. Measured on one real setup: a sub-agent that drove a browser
through 45 tool calls and 4 screenshots moved the parent's context by **2.2K
tokens against ~149K spent inside the agent**.

> **The principle: main context holds decisions and tables. Agents hold pages,
> text and screenshots. Disk holds everything in between.**

**The corollary is the part that gets missed.** Routing content through the
parent to hand it to another agent defeats the whole design — harvested job
descriptions must never pass through the main conversation on their way from the
agent that fetched them to the agent that scores them. Agents write to disk; the
parent passes paths.

**Create the output directory in the parent before launching any agent.** A
file-write tool that does not create parent directories will let every agent
fetch successfully and then fail at the write — a whole batch lost at the last
step.

**Batch work per agent; do not spawn one agent per item.** A sub-agent costs a
large fixed amount just to start (system prompt plus tool schemas), independent
of task size. Few agents doing batches, not many doing singles. Context is
protected by delegation; total usage is not.

**Never acquire text you will score from with a summarising fetch tool.** A
summary erases precisely what scoring depends on — requirement counts and the
vagueness signals that expose an inflated score — and the output still reads
like a posting, so the substitution is silent. Pull raw text, or use the board's
own API.

**Demand a literal return shape.** Ending an agent prompt with an explicit
"final message: ONLY one JSON object" plus the literal shape held across eight
agents in testing, with errors arriving inside an `error` field rather than as
prose. Without it, returns drift into narrative and the parent has to re-read
what the agent already knew.

**Agents write incrementally, never only at the end.** A long harvest that
returns everything at completion loses everything if the agent dies near the
end; one file per item as it lands means a crash costs one item.

### Reading a page without screenshotting it

Prefer text reads for *reading* and reserve screenshots for verification:

- A whole-page text read is not viewport-limited, but its element heuristic can
  pick the wrong container and silently return a fragment — check the length
  against what the page should contain.
- An accessibility-tree read gives labelled, clickable element references, so a
  click does not need screenshot coordinates — but it IS viewport-limited, so a
  long form needs section-by-section traversal.
- Where a screenshot is genuinely needed, a reduced scale costs a fraction of
  the tokens of a full-resolution one.

**Which boards and forms are text-readable is a per-board fact that changes over
time.** Keep it in a dated capability table in the instance's search file, and
re-probe once per sweep rather than per listing — stable within a sweep, not
across months.

### Filling a form in a background tab

Only when the flow genuinely needs it — the common case is pipelining, where an
agent prepares the next application while the human reviews and submits the
previous one.

- **Detect that the page rendered before filling anything.** Count the form's
  inputs and check for two or three expected labels. Zero inputs, or missing
  labels on a form URL, means report "did not render" — never fill blind. A
  screenshot that times out is itself a reportable exception, not a retry loop.
- **Use a DOM-level set, not simulated clicking and typing.** In a background
  tab, simulated input can fail *silently and unreliably* — some fields land,
  most do not, and the tool output still reads as success. A DOM-level setter
  works, and on frameworks that track their own state the value survives a
  re-render, which is the real test that it registered.
- **Verify by reading the values back**, never by screenshot.
- **Fields a DOM set cannot drive** — custom typeahead widgets, comboboxes, file
  upload — go on the report as "needs foreground", to be done when the human
  brings the tab up for review.
- **Do not disturb the human's own tab.** Work in a new one, never switch the
  active tab, and be careful closing tabs: on some setups closing the tab that
  anchors the automation's tab group dissolves it and orphans everything created
  since.

