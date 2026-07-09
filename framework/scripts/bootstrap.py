#!/usr/bin/env python3
"""Bootstrap a private instance: QUICKSTART steps 1 and 2 in one command.

Creates the private/ directory layout, copies every template and tool into
place, seeds the empty state files, and initializes private/ as its own git
repository. Safe to re-run: existing files are never overwritten.

Run from anywhere inside the framework repo:
  python3 framework/scripts/bootstrap.py

What it does NOT do: fill in profile.yml, generate experience_summary.md
(that's an adversarial interview, not a form — see
framework/skills/verified-experience-interview.md), or decide your lanes.
It prints those next steps when it finishes.
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
FRAMEWORK = REPO / "framework"
PRIVATE = REPO / "private"

DIRS = [
    "skills/communications", "data/companies", "data/archive",
    "scripts", "feedback", "resume", "temp",
]

COPIES = [  # (source relative to framework/, destination relative to private/)
    ("templates/profile.yml", "profile.yml"),
    ("templates/experience_summary.md", "experience_summary.md"),
    ("templates/tracker_schema.csv", "job_tracker.csv"),
    ("templates/session_init.md", "skills/session_init.md"),
    ("templates/resume_content.yml", "resume/resume_content.yml"),
    ("scripts/build_resume.py", "resume/build_resume.py"),
    ("scripts/build_history.py", "scripts/build_history.py"),
    ("scripts/daily_log.py", "scripts/daily_log.py"),
]

SEEDS = {
    "data/session_log.md":
        "# Session Log\n\nChronological session notes, newest first. The"
        " daily-log tool (scripts/daily_log.py) folds each day's working"
        " notes in above this line's first entry.\n",
    "data/open_threads.md":
        "# Open Threads\n\n> Small, mutable, read FIRST at every session"
        " start. Overwritten (not appended to) at every session close:"
        " what's open, what's due, who's owed a follow-up — and nothing"
        " else. History lives in session_log.md; this file is only ever"
        " the current state.\n",
    "data/pending_outreach.md":
        "# Pending Outreach Queue\n\n> State only: connection requests"
        " sent, messages queued for acceptance, threads awaiting a reply."
        " The how-to lives in skills/communications/.\n",
    "data/rituals.yml":
        "# Last-run stamps for non-daily rituals (machine-managed).\n"
        "# daily_log.py open/status warn when cadence_days has elapsed;\n"
        "# stamp with: daily_log.py ritual <name>."
        " cadence_days null = on demand.\n"
        "weekly_review:\n  cadence_days: 7\n  last_run: null\n"
        "  note: funnel report + staleness sweeps — see the"
        " search-apply-ritual skill\n",
}


def main():
    made = skipped = 0
    for d in DIRS:
        (PRIVATE / d).mkdir(parents=True, exist_ok=True)

    for src, dst in COPIES:
        source, dest = FRAMEWORK / src, PRIVATE / dst
        if dest.exists():
            print(f"  skip (exists): private/{dst}")
            skipped += 1
        else:
            shutil.copy2(source, dest)
            print(f"  created:       private/{dst}")
            made += 1

    for rel, text in SEEDS.items():
        dest = PRIVATE / rel
        if dest.exists():
            print(f"  skip (exists): private/{rel}")
            skipped += 1
        else:
            dest.write_text(text, encoding="utf-8")
            print(f"  created:       private/{rel}")
            made += 1

    if not (PRIVATE / ".git").exists():
        result = subprocess.run(["git", "init", "-q"], cwd=PRIVATE)
        print("  git:           initialized private/ as its own repository"
              if result.returncode == 0 else
              "  git:           init failed — run 'git init' in private/ yourself")
    else:
        print("  git:           private/ is already a repository")

    print(f"\nBootstrap complete: {made} created, {skipped} left alone.")
    print("""
Next steps (QUICKSTART.md has the detail):
  3. Fill in private/profile.yml — every field is a fact about you.
  4. Generate private/experience_summary.md via the adversarial interview —
     load framework/skills/verified-experience-interview.md for the method.
  5. Fill in skills as you need them, not as a batch.
  6. Point an assistant at the repo root; SESSION_INIT.md does the rest.""")


if __name__ == "__main__":
    if not FRAMEWORK.is_dir():
        sys.exit("Run this from inside the framework repository.")
    main()
