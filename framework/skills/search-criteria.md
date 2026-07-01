# Skill: Search Criteria

**Load when:** running a job search on any board, deciding whether a posting
clears the hard constraints, or refining search queries.

**Depends on:** `private/profile.yml` for the actual constraints, lane titles,
and floor to search against.

---

## Hard constraints gate everything

Before spending any time evaluating a posting's fit, check it against the
constraints in `profile.yml` (remote status, salary floor, excluded regions,
travel tolerance). A role that fails a hard constraint isn't worth reading
further regardless of how good the title looks. Apply this gate first, not
after getting excited about a strong-sounding posting.

## Title reliability varies by lane

Not every title is an equally reliable search filter. Group titles by how much
independent verification they need:

- **Search confidently:** titles that almost always match the intended scope
  without needing to read the JD body first.
- **Scan the JD body before applying:** titles that are good signal but
  ambiguous, verify the specific language (hands-on vs. people-management,
  IC vs. supervisory) before spending application effort.
- **Require explicit qualification:** titles where the label alone tells you
  little, the same title covers genuinely different jobs depending on the
  organization's size and conventions. Never apply on title alone here.

The actual title lists for each tier, and which lane they map to, live in
`private/profile.yml` (`lanes.lane_a.titles`, `lanes.lane_b.titles`) and the
person's own filled `search_criteria.md`.

## Org shape, not title, is the real filter

The situation being searched for is a company where the technical leadership
layer is thin enough that a senior technical role stays close to actual
production work. That situation exists under many different titles depending
on company convention and stage. Searching by title alone will always miss
some roles; combine title search with org-size signals and JD-body language.

## Query construction (board-agnostic principles)

- Short, specific, unquoted multi-word combinations generally outperform exact
  quoted phrases on ranked-relevance search engines: quoted phrases collapse to
  a small, repeat-heavy result pool, while unquoted phrasing lets the ranking
  engine diverge meaningfully across different word choices.
- A specific technical or domain qualifier (a stack, a subdomain) narrows
  usefully without narrowing so far that legitimate matches get missed.
- When a query returns heavy noise from an adjacent but wrong category
  (vendor/consulting roles instead of in-house engineering roles, for example),
  add a disambiguating word rather than abandoning the query outright.
- Cross-query frequency is a real signal: if the same posting surfaces across
  several differently-worded searches, that convergence itself indicates
  strong relevance, independent of any single query's rank.

## Per-board filter mechanics

Salary, remote-status, and date-posted filters exist on essentially every major
board, under different parameter names. The durable pattern is: always apply a
salary floor filter (dropping it floods results with underpaid postings),
prefer remote-only filtering over a text search for "remote" (title text is
unreliable), and sort by date/recency to catch fresh postings before they
accumulate high applicant counts. The specific parameter syntax for each board
in current use is tracked in the person's own filled `search_criteria.md`,
since board URL parameters change over time and are exactly the kind of detail
that needs periodic re-verification rather than being treated as permanently
correct.
