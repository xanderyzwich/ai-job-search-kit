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
mkdir -p private/skills private/data/companies private/data/archive \
         private/scripts private/feedback private/resume private/temp
cd private && git init && cd ..
```

Nothing about the public repo needs to know this happened. See
`ARCHITECTURE.md`, "The three-layer separation," for why it's structured this
way. The `data/` directory is your working state, kept apart from the
methodology in `skills/` — see `framework/CONTRACT.md` for what goes where.

## 2. Copy the templates and tooling in

```bash
cp framework/templates/profile.yml           private/profile.yml
cp framework/templates/experience_summary.md private/experience_summary.md
cp framework/templates/tracker_schema.csv    private/job_tracker.csv
cp framework/templates/session_init.md       private/skills/session_init.md
cp framework/templates/resume_content.yml    private/resume/resume_content.yml
cp framework/scripts/build_resume.py         private/resume/build_resume.py
cp framework/scripts/build_history.py        private/scripts/build_history.py
cp framework/scripts/daily_log.py            private/scripts/daily_log.py
```

The three scripts compute their paths relative to where they sit, which is
why they get copied into place rather than run from `framework/` (the
framework copies are the canonical source; if you improve one, improve it
there). `build_history.py` renders your human-readable application history
from the tracker, `daily_log.py` runs the one-commit-per-day log workflow,
and `build_resume.py` renders your resume lanes from the content file.

There's no template for your session log or open-threads file — they start
empty and grow with use. Create `private/data/session_log.md` with a one-line
header, and `private/data/open_threads.md` empty, whenever you actually start
working (or let the assistant create them during your first real session).
`session_init.md` points to both, so they need to exist by the time anyone
reads that pointer.

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

Have it read the root `SESSION_INIT.md` first. That file is a two-stage
bootstrap by design: on a fresh clone it walks the generic checklist, but
once `private/skills/session_init.md` exists (step 2 above put it there),
the root file's only job is finding and loading it — your private
session-init supersedes the generic one from then on, permanently. That
private file has its own checklist folded in (read `profile.yml`, read
`data/open_threads.md` and the top of `data/session_log.md`, read
`experience_summary.md`, and so on), so you never point at each private file
individually. If you use a persistent-context feature (a Claude Project or
similar), the private session-init is the one file to load there directly.
From there a session loads individual `framework/skills/` files only when
the task at hand actually needs them, and ends by running
`python3 private/scripts/daily_log.py close` — one commit per day, no
bookkeeping debt.

## 7. Build your first resume

Fill in `private/resume/resume_content.yml` — every bullet traced to your
`experience_summary.md` — then:

```bash
python3 private/resume/build_resume.py
```

One layout-only renderer, one content file, one docx per lane you defined.
Reordering bullets, changing which bullet leads, or rewording a summary is
an edit to the YAML; the script never changes for a strategy change. If you
prefer a different document pipeline entirely, nothing else in the system
depends on this one — any process that produces a document from the verified
facts works.
