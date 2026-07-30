# Skill: Human-Writing Standards

**Load when:** presenting any generated content that will actually be sent or
published, a cover letter, an essay answer, an outreach message, profile copy.
This is a gate, not a style preference, run it before presenting a draft as final.

---

## Why this exists

The relevant failure mode in a job search isn't generic bad writing, it's
writing that's competent but detectably not the candidate's own voice.
Recognizable AI-generated patterns are a specific, catchable signal, and a
reader (a recruiter, a hiring manager) can often sense something is off even
without being able to name why. This gate exists to catch that before it ships,
not to enforce a house style for its own sake.

## Structural tells to check for

- **Uniform sentence length.** Real writing varies. A paragraph where every
  sentence runs roughly the same length reads as generated even when the
  content is accurate.
- **Three-part parallel constructions**, repeated as a structural habit rather
  than used once for genuine effect. "I bring X, Y, and Z" is fine once; a
  document that does this in every paragraph reads as templated.
- **Absence of contractions** throughout an otherwise casual-register document.
- **Stock phrases** that carry no specific content: "proven track record,"
  "passionate about," "I am excited to apply," "leverage" used as a verb where
  a plainer verb would do, along with "delve," "robust," "seamless,"
  "comprehensive," "dynamic," "results-driven," "cutting-edge," and
  "game-changing." These are near-universal AI tells specifically because
  they're near-universal human resume-writing tells too, but stacking several
  in one document compounds the signal.
- **Mirrored structure across multiple documents.** If a cover letter's
  paragraph order exactly mirrors the resume's bullet order, or several cover
  letters for different roles share an identical skeleton with only nouns
  swapped, that's a tell even if no individual sentence is flagged.
- **False-contrast framing.** "It's not just X, it's Y." "This isn't about X,
  it's about Y." "No X. No Y. Just Z." These mimic the shape of insight
  without containing any, and they're recognizable enough on their own to
  flag a document even when nothing else is wrong.
- **Em-dash overuse.** One is fine; several in a document is a strong tell on
  its own. Prefer a comma, a period, or a parenthetical.
- **Throat-clearing.** Opening with a sweeping context-setting line ("In
  today's competitive market...") or closing with an unearned summary ("In
  conclusion, I would be a great fit..."). Start on substance, end on
  substance.

## What to do instead

- Vary sentence length deliberately; a document with one long sentence
  followed by a short one reads as more natural than a metronome.
- Use contractions where the register calls for them.
- Lead with something specific to the situation rather than a general claim
  about the candidate. Specificity is both better writing and a stronger
  anti-tell than any phrasing trick.
- Be direct about gaps or weaknesses rather than writing around them. Writing
  that acknowledges a limitation plainly reads as more human, and more
  credible, than writing that carefully avoids the topic.
- When in doubt, read the draft aloud (or have it read back). Phrasing that's
  fine on the page but awkward spoken aloud is a reliable secondary check.

## Before presenting any draft

Run this check as an explicit step, not an assumption that good instructions
upstream already handled it. A draft that passed this check for one document
type doesn't automatically pass for a different one; check each piece of
content that will actually be sent.

## A note on the model doing the drafting

These drafts are written by Claude. Claude's default output already runs
cleaner on most of these tells than other AI writing tools, fewer em-dashes,
less "leverage"/"utilize" by default, but it isn't immune, and it follows an
explicit negative instruction ("don't do X") more reliably than a vague one
("sound human"). That's the reason this document names specific words and
constructions rather than just describing the failure mode: precision here
does more work than it would for a person editing their own writing.
