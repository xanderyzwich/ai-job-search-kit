# Skill: Review — Leak-Scan Triage

**Load when:** you are a TRIAGE AGENT dispatched by `framework-audits.md` because `leak_scan.py` reported possible leaks in the public half. Not for making changes.

**Your constraints:** read-only. No edits, no allow markers, no `STOP` changes, no staging, no commits, no network. A marker is a decision to publish and a `STOP` entry blinds the scan; both belong to the coordinator. Write ONLY the report file the dispatcher names for you (yours alone). In the report never repeat a person's name or a dollar figure; cite `file:line` and the matched pattern's category.

---

## Method

1. Run `python3 framework/scripts/leak_scan.py` from the repo root. Take each hit (`file:line  'pattern'`).
2. For each hit read the whole sentence at that line, plus its section heading.
3. Find where the pattern came from: a private company brief filename, a contact record, or a `profile.yml` value (list `private/data/companies/`, `private/data/contacts/`, grep `private/profile.yml`). Do not guess.
4. Decide which category the hit is, from the sentence, not from the word:

| category | meaning | recommended change |
|---|---|---|
| **common word** | an ordinary English word or generic noun that happens to be an employer's whole name | reword the sentence; add to `STOP` only if it is generic everywhere |
| **technology / vendor** | a public product or ATS/board name used as a technology, even though it is also an employer in the search | a line-level allow marker `<!-- leak-scan: allow -->` on that line. NEVER a `STOP` entry: that would hide a real leak of the employer |
| **real mention** | names the employer, person or figure as part of the search (a result, a verdict, a story) | generalise the sentence or move it to the private overlay. Never allow |
| **count without a name** | a measured figure with the identifying name removed that could still point at one board | owner's call: say so, do not decide |
| **cannot tell** | the sentence is ambiguous | say so and quote the sentence's role, not the content |

5. Also check every existing `leak-scan: allow` marker in the scanned files: does the line still read as a technology/vendor mention, or has the sentence drifted into a real mention?

## Report

A markdown table: `file:line`, pattern source (brief / contact / profile), category, recommended change, confidence. A 3-line summary first: how many hits, how many need a change, how many need the owner. Then stop. **The coordinator decides and applies every change; if you believe no change is needed for a hit, say "no change" with the reason.**
