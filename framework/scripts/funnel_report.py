#!/usr/bin/env python3
"""Funnel report: turn a job_tracker.csv into conversion measurements.

Reads a tracker following framework/CONTRACT.md's column schema and reports
response and advance rates overall and split by source, found_via (discovery
point; URLs are grouped by domain), lane, and resume_version — the
difference between "volume isn't working" as a feeling and as a measurement.

Definitions:
  submitted  status in {applied, dm_sent, phone_screen, interview, offer,
             declined_by_us, declined_by_them, closed_no_response}
             closed_no_response counts here because it WAS a real submission;
             leaving it out would shrink every denominator and silently
             inflate the rates. It is not a response and not an advance.
  response   a response_date is set, or status implies one
             (phone_screen/interview/offer/declined_*)
  advance    status is phone_screen, interview, or offer — a response that
             moved forward rather than closed

Usage: python3 framework/scripts/funnel_report.py [path/to/job_tracker.csv]
       (default: private/job_tracker.csv relative to the repo root)
"""
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_history import load_entries  # noqa: E402 — same-dir sibling script

SUBMITTED = {"applied", "dm_sent", "phone_screen", "interview", "offer",
             "declined_by_us", "declined_by_them", "closed_no_response"}
RESPONDED_STATUSES = {"phone_screen", "interview", "offer",
                      "declined_by_us", "declined_by_them"}
ADVANCE = {"phone_screen", "interview", "offer"}


def ever_advanced(row):
    """Did this application EVER reach a screen, interview or offer?

    Read from `peak_stage`, not from `application_status`. Status is current
    state, so an advance that ends in a rejection overwrites itself and
    disappears from the count -- which means the metric decays toward zero
    precisely as a search progresses and the deepest results are the first to
    vanish. Falling back to the live status keeps this correct on a tracker
    that predates the column."""
    return (row.get("peak_stage", "").strip() in ADVANCE
            or row["application_status"] in ADVANCE)
WARM_SOURCES = {"referral", "recruiter"}


def responded(row):
    return bool(row.get("response_date", "").strip()) \
        or row["application_status"] in RESPONDED_STATUSES


def pct(part, whole):
    return f"{part}/{whole} ({part / whole:.0%})" if whole else "0/0 (n/a)"


def normalize_place(value):
    """Group discovery-point URLs by domain so a split doesn't fragment."""
    v = (value or "").strip()
    if v.startswith(("http://", "https://")):
        return urlparse(v).netloc.replace("www.", "") or v
    return v


def split_report(rows, key, label, normalize=None):
    groups = defaultdict(list)
    for row in rows:
        v = (row.get(key) or "").strip()
        if normalize:
            v = normalize(v)
        groups[v or "(blank)"].append(row)
    lines = [f"\nBy {label}:"]
    for name in sorted(groups, key=lambda n: -len(groups[n])):
        g = groups[name]
        resp = sum(1 for r in g if responded(r))
        adv = sum(1 for r in g if ever_advanced(r))
        lines.append(f"  {name:<24} submitted {len(g):>3}   "
                     f"response {pct(resp, len(g)):<12} advance {pct(adv, len(g))}")
    return lines


def main():
    default = Path(__file__).resolve().parent.parent.parent / "private" / "job_tracker.csv"
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else default
    rows = [r for r in load_entries(path)
            if r["application_status"] in SUBMITTED]

    resp = sum(1 for r in rows if responded(r))
    adv = sum(1 for r in rows if ever_advanced(r))
    warm = [r for r in rows if (r.get("source") or "").strip() in WARM_SOURCES]
    cold = [r for r in rows if r not in warm]

    print(f"Tracker: {path}")
    print(f"Submitted: {len(rows)}   response {pct(resp, len(rows))}   "
          f"advance {pct(adv, len(rows))}")
    print(f"Warm (referral/recruiter): submitted {len(warm)}, "
          f"response {pct(sum(1 for r in warm if responded(r)), len(warm))}")
    print(f"Cold (everything else):    submitted {len(cold)}, "
          f"response {pct(sum(1 for r in cold if responded(r)), len(cold))}")

    # A rejection before anyone spoke to you and a rejection after a full
    # interview loop are the same status value, and they diagnose opposite
    # problems: one says the resume is not getting you into the room, the
    # other says the room is not converting. Pooling them hides the single
    # most actionable split in the funnel, so it is reported separately.
    rejected = [r for r in rows if r["application_status"] == "declined_by_them"]
    after = [r for r in rejected if ever_advanced(r)]
    print(f"\nRejections: {len(rejected)}"
          f"   at screen {pct(len(rejected) - len(after), len(rejected))}"
          f"   after a conversation {pct(len(after), len(rejected))}")
    talked = sum(1 for r in rows if ever_advanced(r))
    print(f"Reached a conversation at all: {pct(talked, len(rows))} of submissions"
          f"  <- the number a response rate hides")
    for key, label in (("source", "source"), ("lane", "lane"),
                       ("resume_version", "resume version")):
        print("\n".join(split_report(rows, key, label)))
    print("\n".join(split_report(rows, "found_via", "discovery point",
                                 normalize=normalize_place)))


if __name__ == "__main__":
    main()
