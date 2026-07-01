# Quickstart

A step-by-step walkthrough for setting this up as your own workspace. If
you just want to understand the system, `README.md` and `ARCHITECTURE.md`
cover that. This document is for actually using it.

---

## 1. Set up `private/`

`private/` is gitignored by the root `.gitignore` already. Create the
directory, and if you want real version history for your own data (recommended
once you're actually using this for a search), initialize it as its own
independent git repository:

```bash
mkdir -p private/skills private/feedback private/resume
cd private && git init && cd ..
```

Nothing about the public repo needs to know this happened. See
`ARCHITECTURE.md`, "The three-layer separation," for why it's structured this
way.

## 2. Copy the templates in

```bash
cp framework/templates/profile.yml           private/profile.yml
cp framework/templates/experience_summary.md private/experience_summary.md
cp framework/templates/tracker_schema.csv    private/job_tracker.csv
cp framework/templates/session_init.md       private/skills/session_init.md
```

There's no template for your session log, it starts empty and grows as you use
it. Create `private/skills/session_log.md` with a one-line header and your
first dated entry whenever you actually start working (or let the assistant
create it during your first real session). `session_init.md` points to it, so
it needs to exist by the time anyone reads that pointer.

## 3. Fill in `profile.yml`

This part is mechanical. Every field is a fact about you: contact info, your
salary floor, where you won't relocate, what lanes your search runs in (see
`framework/skills/resume-lane-strategy.md` if the lane concept doesn't apply
to your search, one lane is fine, just leave the other's title list empty).
Fill this in first; everything else in the system references it rather than
restating your numbers.

## 4. Generate `experience_summary.md` — the part that isn't mechanical

This is the one file that can't be filled in quickly. It's the source of
truth every resume, cover letter, and piece of outreach copy has to trace
back to, and the whole point is that it's been stress-tested, not just
self-reported. See `ARCHITECTURE.md`, "Source of truth, not just a reference
document," for why this matters.

**How to actually do it:**

1. Start from whatever self-description you already have, a resume, a
   LinkedIn About section, notes on your own experience.
2. Go through each claim one at a time and interrogate it, rather than
   transcribe it. For every accomplishment: What exactly did *you* do, versus
   what did a team, a predecessor, or a tool do? What's the actual mechanism
   behind the outcome you're citing, not just the outcome? Is the number
   you're using something you verified, or something that sounds about
   right?
3. Have the assistant push back deliberately. Don't ask it to make your
   experience sound good, ask it to find the soft spot in each claim, the way
   a sharp interviewer would. This only works if you actually want the
   pushback rather than a nicer-sounding version of what you started with.
4. When a claim turns out to be rounder than the truth, write down the
   corrected version, and separately add the original overclaim to the
   "Overclaims to avoid" section. Both matter: the correction fixes today's
   document, the avoid-list stops the original overclaim from quietly
   resurfacing in a session that doesn't have this conversation in context.
5. Treat this as a real conversation, not a form. It took multiple passes,
   real back-and-forth, and a willingness to have something you were proud of
   get walked back once it was actually examined.

**A starter prompt**, if you want something concrete to paste to an
assistant to kick this off:

> I want to build a verified account of my work experience that I'll use as
> the source of truth for my resume and job search materials going forward.
> Here's my current resume/background: [paste it]. Go through each claim
> with me one at a time. For each one, ask what I specifically did versus
> what a team or predecessor did, what the real mechanism behind any result
> was, and whether any number I'm using is something I actually verified.
> Push back if something sounds rounder or more impressive than it probably
> was. I'd rather have an accurate, slightly less flashy account than a
> polished one I can't defend in a follow-up question.

## 5. Fill in the rest of `skills/`, as needed

Not all at once. Copy `framework/skills/resume-lane-strategy.md` (and any
others that apply) into `private/skills/` under the same name, and fill in
the generic pattern with your actual lane assignments and reasoning. Do this
as you need each one, not as a batch, there's no requirement to have all of
`skills/` filled in before you start.

## 6. Point an assistant at the repo

Have it read the root `SESSION_INIT.md` first. It checks for
`private/skills/session_init.md` and loads it automatically, that file has
its own checklist folded in (read `profile.yml`, read the top of
`session_log.md`, read `experience_summary.md`, and so on), so you don't need
to point at each private file individually. From there it should be able to
work the same way this project's own sessions do, loading individual
`framework/skills/` files only when the task at hand actually needs them.

## 7. Build your first resume

`private/resume/` is where generated resumes live. There's no required tool
here, `framework/scripts/` is intentionally unopinionated about how you go
from `profile.yml` + `experience_summary.md` to an actual document. A
generated `.docx` built with a small Python script is one way; anything that
produces a document from the verified facts works.
