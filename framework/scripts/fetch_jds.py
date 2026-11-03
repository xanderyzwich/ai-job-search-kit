#!/usr/bin/env python3
"""Fetch job descriptions into a cache, and REFUSE TO LIE ABOUT HOW MANY ARRIVED.

THE FAILURE THIS EXISTS FOR, measured 2026-11-03. An ad-hoc fetch loop pulled
339 postings, 213 of them failed, and the run reported a count and moved on. The
126 that survived were analysed as though they were the corpus. They were 37% of
it, and because the loop walked insertion order they skewed hard toward the
first query -- so the frequency analysis built on them under-represented three
whole title families and nothing in the output said so.

TWO DEFECTS, AND THE SECOND IS WORSE THAN THE FIRST.

  1. NO RETRY. `except Exception: fail += 1; continue`. One transient blip meant
     permanent loss for that URL. Re-probing six of the failures the next hour
     returned 200 with full content in under a second each -- the URLs were fine
     and the content was there.

  2. THE DIAGNOSTIC WAS DISCARDED. That bare `except` threw away the status code
     and the exception type, so the cause was a GUESS ("rate limiting") that
     then shaped the proposed fix. A failure you did not record is a failure you
     will mis-diagnose.

SO: retry is plain and short, because transient is what was measured. There is
no exponential backoff here -- backoff is the remedy for a server asking you to
slow down, and nothing has yet shown that is happening. `--failures` writes what
actually went wrong, and THAT is what should decide whether backoff is ever
added. Do not add it on reflex.

THE COMPLETION GATE IS THE POINT. Below `--require-rate` the run prints NOT
COMPLETE and exits non-zero, so a partial corpus cannot be handed downstream
looking whole. A sweep must not score what this refuses to certify.

TRIAGE BEFORE YOU GET HERE. This fetches exactly what it is given. Handing it a
whole harvest is the wrong move -- card data (title, url, snippet) is enough to
drop obvious misses, and fetching 336 detail pages to score 80 is waste whether
or not anything throttles.

    fetch_jds.py URLS.json --cache DIR [--retries 3] [--delay 1.2]
                 [--require-rate 0.95] [--failures FILE] [--limit N]

URLS.json is either a list of URLs or an object whose keys are URLs.
"""
import argparse
import html
import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
LD = re.compile(r'<script[^>]*type="application/ld\+?(?:json|&#x2B;json)"[^>]*>(.*?)</script>',
                re.S | re.I)


def cache_name(url):
    """A filesystem-safe, stable name for a URL."""
    return re.sub(r"\W+", "_", url)[-80:] + ".json"


def job_posting(body):
    """Pull a JobPosting out of JSON-LD, including when it is nested in @graph."""
    for m in LD.finditer(body):
        try:
            d = json.loads(html.unescape(m.group(1)))
        except Exception:
            continue
        nodes = d.get("@graph") if isinstance(d, dict) else (d if isinstance(d, list) else [d])
        for n in (nodes or [d] if isinstance(d, dict) else nodes or []):
            if isinstance(n, dict) and n.get("@type") == "JobPosting":
                return n
    return None


def fetch_one(url, retries, delay):
    """Return (record, attempts). Attempts is a list of what each try did --
    kept even on success, because a URL that needed two tries is evidence."""
    attempts = []
    for i in range(retries):
        try:
            r = urllib.request.urlopen(
                urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30)
            body = r.read().decode("utf-8", "replace")
            attempts.append(f"HTTP{r.status}")
            post = job_posting(body)
            if post is None:
                attempts.append("no-JobPosting")
                return None, attempts
            return {"url": url,
                    "title": post.get("title"),
                    "org": (post.get("hiringOrganization") or {}).get("name"),
                    "desc": post.get("description") or "",
                    "salary": post.get("baseSalary"),
                    "posted": post.get("datePosted")}, attempts
        except urllib.error.HTTPError as e:
            attempts.append(f"HTTP{e.code}")
            if e.code in (404, 410):
                return None, attempts          # gone is not transient; stop trying
        except Exception as e:
            attempts.append(type(e).__name__)
        if i + 1 < retries:
            time.sleep(delay * 2)              # a pause, not a backoff curve
    return None, attempts


def main():
    p = argparse.ArgumentParser()
    p.add_argument("urls")
    p.add_argument("--cache", required=True)
    p.add_argument("--retries", type=int, default=3)
    p.add_argument("--delay", type=float, default=1.2)
    p.add_argument("--require-rate", type=float, default=0.95,
                   help="fail the run below this fetched fraction (default 0.95)")
    p.add_argument("--failures", default=None, help="JSONL of what went wrong")
    p.add_argument("--limit", type=int, default=None)
    a = p.parse_args()

    raw = json.load(open(a.urls, encoding="utf-8"))
    urls = list(raw) if isinstance(raw, (list, dict)) else []
    if a.limit:
        urls = urls[:a.limit]
    cache = pathlib.Path(a.cache)
    cache.mkdir(parents=True, exist_ok=True)

    ok = skipped = 0
    failures = []
    for i, url in enumerate(urls, 1):
        path = cache / cache_name(url)
        if path.exists():
            skipped += 1
            continue
        rec, attempts = fetch_one(url, a.retries, a.delay)
        if rec:
            path.write_text(json.dumps(rec), encoding="utf-8")
            ok += 1
            if len(attempts) > 1:
                print(f"  recovered after {len(attempts)} tries: {url[-50:]}", flush=True)
        else:
            failures.append({"url": url, "attempts": attempts})
        if i % 40 == 0:
            print(f"  {i}/{len(urls)}  new={ok} failed={len(failures)} cached={skipped}",
                  flush=True)
        time.sleep(a.delay)

    have = ok + skipped
    rate = have / len(urls) if urls else 1.0
    print(f"\nfetched {have}/{len(urls)} ({rate:.1%})  new={ok} already-cached={skipped} "
          f"failed={len(failures)}")

    if failures:
        tally = {}
        for f in failures:
            tally[" > ".join(f["attempts"]) or "none"] = tally.get(
                " > ".join(f["attempts"]) or "none", 0) + 1
        print("FAILURE MODES -- read these before changing the retry strategy:")
        for k, v in sorted(tally.items(), key=lambda x: -x[1]):
            print(f"  {v:4d}  {k}")
        if a.failures:
            pathlib.Path(a.failures).write_text(
                "\n".join(json.dumps(f) for f in failures), encoding="utf-8")
            print(f"  written to {a.failures} -- re-run with that as the url list")

    if rate < a.require_rate:
        print(f"\nNOT COMPLETE: {rate:.1%} is below the required {a.require_rate:.0%}.")
        print("DO NOT SCORE THIS CORPUS. A partial harvest is not a small harvest --")
        print("the gaps are not random, so any frequency read off it is skewed and")
        print("nothing downstream will say so. Re-run to resume from the cache.")
        return 1
    print("COMPLETE -- safe to score.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
