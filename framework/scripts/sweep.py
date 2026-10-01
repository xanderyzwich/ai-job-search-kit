#!/usr/bin/env python3
"""Board-sweep recorder.

A sweep is the unit of SEARCH EFFORT: one board, one query family, one
continuous sitting. The tracker records what a sweep produced; without the
sweep itself recorded, "167 rows from board X" has no denominator and cannot
answer the only question that matters -- where to spend the next hour.

    sweep.py start <board> [--query Q] [--lane ic|pc] [--note N]
    sweep.py end [--screened N] [--known N] [--minutes N] [--signal S] [--note N]
    sweep.py status
    sweep.py report [--board B]

`start` opens a sweep and writes data/sweep_open.json. Every tracker row
added while one is open should carry its `sweep_id`; `end` stamps any row
that has a blank sweep_id and a found_via naming this board, then closes it.

WHY THIS IS A COMMAND AND NOT A MARKDOWN TABLE: the hand-maintained sweep
log it replaced died twice. In its final state it showed two boards last
swept months earlier that had both been swept that same week -- so the one
question it existed to answer could not be answered from it. A record that
depends on remembering to append to it ends up describing what someone
remembered instead of what happened.

THE THREE NUMBERS THAT ONLY EXIST IF CAPTURED NOW:
  screened  how many listings you actually looked at. The tracker holds
            only survivors, so this is the one honest denominator for
            precision, and it is unrecoverable the moment you close the tab.
  known     of those, how many were ALREADY in the tracker. This is the
            overlap measurement, and it is free -- you hit the collisions
            anyway. Without it, whichever board you sweep FIRST banks all
            the overlap and looks artificially strong.
  minutes   rough wall-clock. Without it, "per sweep" rewards sweep DEPTH
            (an 8-page sweep of one board vs a 1-page sweep of another)
            rather than board quality.

Estimates are fine and better than blanks. Say ~40, not nothing.
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if (ROOT / "job_tracker.csv").exists():          # installed into private/
    PRIV = ROOT
else:                                            # running from framework/
    PRIV = ROOT.parent / "private"

TRACKER = PRIV / "job_tracker.csv"
SWEEPS = PRIV / "data" / "sweeps.csv"
OPEN_FILE = PRIV / "data" / "sweep_open.json"

FIELDS = ["sweep_id", "date", "board", "query", "lane", "screened",
          "already_known", "minutes", "rows_created", "signal",
          "provenance", "notes"]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def load_sweeps():
    if not SWEEPS.exists():
        return []
    return list(csv.DictReader(SWEEPS.open()))


def write_sweeps(rows):
    SWEEPS.parent.mkdir(parents=True, exist_ok=True)
    with SWEEPS.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in FIELDS})


def tracker_rows():
    if not TRACKER.exists():
        return [], []
    rdr = csv.DictReader(TRACKER.open())
    return list(rdr), list(rdr.fieldnames or [])


def cmd_start(a):
    if OPEN_FILE.exists():
        cur = json.loads(OPEN_FILE.read_text())
        sys.exit(f"A sweep is already open: {cur['sweep_id']}\n"
                 f"Close it with `sweep.py end` before starting another.")
    board = slug(a.board)
    today = date.today().isoformat()
    existing = {r["sweep_id"] for r in load_sweeps()}
    sid = f"{board}-{today}"
    n = 2
    while sid in existing:
        sid = f"{board}-{today}-{n}"
        n += 1
    # Snapshot which rows already exist. `end` claims the DIFFERENCE and
    # nothing else. Without this the close matched on board name alone and
    # would have retroactively claimed every previously-unattributed row for
    # that board -- 44 of them on one real tracker, which would have inflated
    # the next sweep's yield eightfold and permanently mis-dated the rest.
    before, _ = tracker_rows()
    keys = sorted({f"{r.get('company','')}␟{r.get('role','')}" for r in before})

    OPEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    OPEN_FILE.write_text(json.dumps({
        "sweep_id": sid, "board": board, "date": today,
        "query": a.query or "", "lane": a.lane or "", "note": a.note or "",
        "started": datetime.now().isoformat(timespec="seconds"),
        "rows_at_start": keys,
    }, indent=1))
    print(f"SWEEP OPEN: {sid}")
    print(f"  Tag every new tracker row with sweep_id={sid}")
    print("  At the end you will be asked for: screened, already-known, minutes.")
    print("  Start counting now -- screened and already-known cannot be")
    print("  reconstructed once the tab is closed.")


def cmd_end(a):
    if not OPEN_FILE.exists():
        sys.exit("No sweep is open. `sweep.py start <board>` first.")
    cur = json.loads(OPEN_FILE.read_text())
    sid, board = cur["sweep_id"], cur["board"]

    rows, hdr = tracker_rows()
    stamped = 0
    if rows and "sweep_id" in hdr:
        # Only rows that did not exist when the sweep started. A row that was
        # already in the tracker belongs to whatever found it the first time,
        # even when this sweep surfaced it again -- that re-encounter is a
        # COLLISION, and it belongs in --known, not in this sweep's yield.
        before = set(cur.get("rows_at_start") or [])
        unbounded = cur.get("rows_at_start") is None
        for r in rows:
            if r.get("sweep_id", "").strip():
                continue
            if not unbounded and f"{r.get('company','')}␟{r.get('role','')}" in before:
                continue
            hay = f"{r.get('found_via','')} {r.get('source','')}".lower()
            if board.replace("-", " ") in hay or board in hay:
                r["sweep_id"] = sid
                stamped += 1
        if unbounded:
            print("WARNING: this sweep was opened before row-snapshotting existed;"
                  " its stamping is unbounded. Check the rows it claimed.")
        if stamped:
            with TRACKER.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=hdr)
                w.writeheader()
                w.writerows(rows)
    created = sum(1 for r in rows if r.get("sweep_id", "").strip() == sid)

    sweeps = load_sweeps()
    sweeps = [s for s in sweeps if s["sweep_id"] != sid]
    sweeps.append({
        "sweep_id": sid, "date": cur["date"], "board": board,
        "query": a.query or cur.get("query", ""), "lane": cur.get("lane", ""),
        "screened": a.screened if a.screened is not None else "",
        "already_known": a.known if a.known is not None else "",
        "minutes": a.minutes if a.minutes is not None else "",
        "rows_created": created, "signal": a.signal or "",
        "provenance": "recorded",
        "notes": " | ".join(x for x in (cur.get("note"), a.note) if x),
    })
    sweeps.sort(key=lambda r: (r.get("date", ""), r.get("board", "")))
    write_sweeps(sweeps)
    OPEN_FILE.unlink()

    print(f"SWEEP CLOSED: {sid}")
    print(f"  rows created      {created}" + (f"  ({stamped} auto-stamped)" if stamped else ""))
    for label, val in (("screened", a.screened), ("already known", a.known),
                       ("minutes", a.minutes)):
        print(f"  {label:17s} {val if val is not None else 'NOT RECORDED -- unrecoverable'}")
    if a.screened:
        print(f"  precision         {100 * created / a.screened:.0f}%"
              " (rows created / listings screened)")
    if a.screened and a.known is not None:
        print(f"  redundancy        {100 * a.known / a.screened:.0f}%"
              " (already tracked / listings screened)")


def cmd_status(_a):
    if OPEN_FILE.exists():
        cur = json.loads(OPEN_FILE.read_text())
        print(f"OPEN: {cur['sweep_id']}  (started {cur['started']})")
        print(f"  query: {cur.get('query') or '(none recorded)'}")
        print("  Close with: sweep.py end --screened N --known N --minutes N")
    else:
        print("No sweep open.")
    s = load_sweeps()
    print(f"{len(s)} sweeps on record; "
          f"{sum(1 for r in s if r.get('screened'))} have a screened count.")


def cmd_report(a):
    rows, _ = tracker_rows()
    SUB = {"applied", "dm_sent", "phone_screen", "interview", "offer",
           "declined_by_us", "declined_by_them", "closed_no_response"}
    per_sweep = defaultdict(lambda: {"rows": 0, "apps": 0})
    unknown = defaultdict(int)
    for r in rows:
        sid = r.get("sweep_id", "").strip()
        if not sid:
            continue
        # `<board>-unknown` means the board is known and the sweep is not.
        # It is a LABEL, never a sweep, and must stay out of every per-sweep
        # rate or it silently invents a sweep with no screened count.
        if sid.endswith("-unknown"):
            unknown[sid[: -len("-unknown")]] += 1
            continue
        p = per_sweep[sid]
        p["rows"] += 1
        if r.get("application_status", "").strip() in SUB:
            p["apps"] += 1

    board = defaultdict(lambda: {"n": 0, "rows": 0, "apps": 0, "dead": 0,
                                 # precision/redundancy are computed ONLY over
                                 # the sweeps that actually carry a screened
                                 # count. Dividing all-sweep rows by
                                 # some-sweep screened produced a 203%
                                 # "precision" for one board the first time this
                                 # ran -- a ratio whose numerator and
                                 # denominator came from different populations.
                                 "sc_n": 0, "sc_rows": 0, "screened": 0,
                                 "known": 0, "known_n": 0, "mins": 0})
    for s in load_sweeps():
        b = slug(s.get("board", "?"))
        if a.board and slug(a.board) != b:
            continue
        v = per_sweep.get(s["sweep_id"], {"rows": 0, "apps": 0})
        d = board[b]
        d["n"] += 1
        d["rows"] += v["rows"]
        d["apps"] += v["apps"]
        d["dead"] += 1 if v["apps"] == 0 else 0
        try:
            sc = int(float(s.get("screened") or 0))
        except ValueError:
            sc = 0
        # A `logged-only` sweep has a screened count from the written log but
        # no tracker rows carrying its id -- its rows_created is 0 by
        # construction, not by outcome. Counting it would drive precision
        # toward zero on a board that simply had sloppy found_via text.
        if sc and s.get("provenance") != "logged-only":
            d["sc_n"] += 1
            d["sc_rows"] += v["rows"]
            d["screened"] += sc
            try:
                kn = int(float(s.get("already_known") or ""))
                d["known"] += kn
                d["known_n"] += 1
            except ValueError:
                pass
        try:
            d["mins"] += int(float(s.get("minutes") or 0))
        except ValueError:
            pass

    print(f"{'board':20s} {'swps':>4} {'rows':>5} {'apps':>5} "
          f"{'rows/sw':>8} {'apps/sw':>8} {'apps/row':>9} {'prec':>10} {'redund':>7} {'0-app':>6}")
    for b, d in sorted(board.items(), key=lambda x: -x[1]["apps"]):
        prec = (f"{100*d['sc_rows']/d['screened']:.0f}% ({d['sc_n']}/{d['n']})"
                if d["screened"] else "--")
        red = f"{100*d['known']/d['screened']:.0f}%" if d["known_n"] else "--"
        print(f"{b:20s} {d['n']:4d} {d['rows']:5d} {d['apps']:5d} "
              f"{d['rows']/d['n']:8.1f} {d['apps']/d['n']:8.1f} "
              f"{(100*d['apps']/d['rows'] if d['rows'] else 0):8.0f}% "
              f"{prec:>10} {red:>7} {f'{d[chr(100)+chr(101)+chr(97)+chr(100)]}/{d[chr(110)]}':>6}")
    if unknown:
        tot = sum(unknown.values())
        print(f"\n{tot} rows carry a `<board>-unknown` label: the board is known,"
              " the sweep is not.")
        print("  " + "  ".join(f"{b}:{n}" for b, n in sorted(unknown.items(),
                                                             key=lambda x: -x[1])))
        print("  They are EXCLUDED above -- counting them would attribute rows to"
              " sweeps that have no screened count,")
        print("  which is the same error as judging a board on volume alone.")
    print("\nprec is rows/screened over ONLY the sweeps carrying a screened count"
          " -- the (n/total) beside it says how many that was.")
    print("redund is blank until `already_known` is recorded; apps/sw rewards"
          " sweep DEPTH until `minutes` exists. Read both with that caveat.")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start"); s.add_argument("board")
    s.add_argument("--query"); s.add_argument("--lane"); s.add_argument("--note")
    s.set_defaults(fn=cmd_start)

    e = sub.add_parser("end")
    e.add_argument("--screened", type=int); e.add_argument("--known", type=int)
    e.add_argument("--minutes", type=int); e.add_argument("--signal")
    e.add_argument("--query"); e.add_argument("--note")
    e.set_defaults(fn=cmd_end)

    sub.add_parser("status").set_defaults(fn=cmd_status)
    r = sub.add_parser("report"); r.add_argument("--board"); r.set_defaults(fn=cmd_report)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
