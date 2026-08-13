#!/usr/bin/env python3
"""Render data/application_history.md from job_tracker.csv.

The tracker is the single hand-edited application record. This script
generates the human-readable views (active, closed, vetted) plus summary
counts. Never hand-edit the output file: fix the tracker and rerun this.

Usage: python3 scripts/build_history.py
"""
import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "job_tracker.csv"
OUT = ROOT / "data" / "application_history.md"

ACTIVE = ("applied", "dm_sent", "phone_screen", "interview", "offer")
CLOSED = ("declined_by_them", "declined_by_us")
VETTED = ("researching", "skipped")
RESPONDED = ("phone_screen", "interview", "offer",
             "declined_by_them", "declined_by_us")


def esc(value):
    return (value or "").strip().replace("|", "\\|").replace("\n", " ")


def render_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "---|" * len(headers)]
    lines += ["| " + " | ".join(esc(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def truncate(text, limit=160):
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def load_entries(path=None):
    """Read the tracker, refusing to proceed on a malformed row.

    A single unquoted comma inside a field value shifts every column after
    it, so the row still parses but its later fields (source, lane,
    resume_version, notes, found_via) silently read the wrong values. The
    views and the funnel report both tolerate that shape, which is how the
    bug survived two rounds of cleanup. This is the guard: field count must
    match the header exactly, or nothing is generated.

    Shared: `funnel_report.py` imports this so both readers of the tracker
    fail the same way instead of one of them quietly tolerating bad shape.
    """
    path = Path(path) if path else TRACKER
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            raise SystemExit(f"{path}: file is empty (no header row).")
        bad = []
        rows = []
        for row in reader:
            if not row:
                continue
            if len(row) != len(header):
                bad.append((reader.line_num, len(row), row))
            rows.append(row)

    if bad:
        lines = [
            f"{path.name}: {len(bad)} malformed row(s) — expected"
            f" {len(header)} fields per row. Nothing was generated.",
            "",
            "Almost always an unquoted comma inside a field value. Quote the"
            " offending field (or remove the comma) and rerun.",
            "",
        ]
        for line_num, count, row in bad:
            company = row[2] if len(row) > 2 else "?"
            role = row[3] if len(row) > 3 else "?"
            lines.append(f"  line {line_num}: {count} fields — {company} / {role}")
        raise SystemExit("\n".join(lines))

    return [dict(zip(header, row)) for row in rows]


def main():
    entries = load_entries()

    def g(entry, key):
        return (entry.get(key) or "").strip()

    def status(entry):
        return g(entry, "application_status")

    active = sorted((e for e in entries if status(e) in ACTIVE),
                    key=lambda e: g(e, "date_applied"), reverse=True)
    closed = sorted((e for e in entries if status(e) in CLOSED),
                    key=lambda e: g(e, "response_date") or g(e, "date_applied"),
                    reverse=True)
    vetted = [e for e in entries if status(e) in VETTED]
    unknown = [e for e in entries
               if status(e) not in ACTIVE + CLOSED + VETTED]

    submitted = active + closed
    responded = [e for e in submitted
                 if g(e, "response_date") or status(e) in RESPONDED]
    rate = f"{len(responded) / len(submitted):.0%}" if submitted else "n/a"

    parts = [
        "# Application History",
        "",
        "> **GENERATED FILE — do not hand-edit.** Rendered from"
        " `job_tracker.csv` by `scripts/build_history.py` on"
        f" {date.today().isoformat()}. The tracker is the single hand-edited"
        " record; fix it there and rerun the script (or let"
        " `scripts/daily_log.py close` do it).",
        "",
        "## Summary",
        "",
        f"- **Submitted:** {len(submitted)} ({len(active)} active,"
        f" {len(closed)} closed)",
        f"- **Responses on submitted:** {len(responded)} ({rate})",
        f"- **Vetted, not applied:** {len(vetted)}"
        f" ({sum(1 for e in vetted if status(e) == 'researching')} researching,"
        f" {sum(1 for e in vetted if status(e) == 'skipped')} skipped)",
        "",
        "## Active Applications",
        "",
        render_table(
            ["Company", "Role", "Salary", "Status", "Applied"],
            [[g(e, "company"), g(e, "role"), g(e, "salary_range"),
              status(e), g(e, "date_applied")] for e in active]),
        "",
        "## Closed Applications",
        "",
        render_table(
            ["Company", "Role", "Salary", "Applied", "Closed", "Status"],
            [[g(e, "company"), g(e, "role"), g(e, "salary_range"),
              g(e, "date_applied"), g(e, "response_date"), status(e)]
             for e in closed]),
        "",
        "## Vetted — Not Applied",
        "",
        render_table(
            ["Company", "Role", "Salary", "Status", "Fit / Note"],
            [[g(e, "company"), g(e, "role"), g(e, "salary_range"),
              status(e), truncate(g(e, "notes"))] for e in vetted]),
        "",
    ]

    if unknown:
        parts += [
            "## Rows With Unrecognized Status (fix these in the tracker)",
            "",
            render_table(
                ["Company", "Role", "Status"],
                [[g(e, "company"), g(e, "role"), status(e)]
                 for e in unknown]),
            "",
        ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(submitted)} submitted, "
          f"{len(vetted)} vetted, {len(unknown)} unrecognized.")


if __name__ == "__main__":
    main()
