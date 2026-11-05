#!/usr/bin/env python3
"""Check official documentation sources for changes (stdlib only).

Each source gets one bounded GET (20 s timeout, one retry, at most two in parallel).
The body is streamed into SHA-256 and discarded, so no upstream text is stored.
A change is a different SHA-256 than the one recorded in catalog.json.

Usage:
  python3 scripts/check_updates.py                  # report only, writes nothing
  python3 scripts/check_updates.py --apply          # record results, append CHANGELOG.md
  python3 scripts/check_updates.py --exchange binance --apply

Exit codes: 0 every checked source passed; 1 at least one fetch failed; 2 bad arguments.
Failed fetches never change the recorded state; the report says why.
"""
import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
CHANGELOG = ROOT / "CHANGELOG.md"
TIMEOUT_S = 20
RETRIES = 1
MAX_WORKERS = 2
MAX_BYTES = 64 * 1024 * 1024
USER_AGENT = "exchange-docs-hub-check/1 (+https://github.com/algoboy-kevin/exchange-docs-hub)"
SHELL_PREFIXES = (b"<!doctype", b"<html")
CHANGELOG_HEADER = (
    "# Changelog\n\n"
    "Append-only log written by `scripts/check_updates.py --apply`. It records URLs, hashes\n"
    "and sizes only, never upstream text.\n\n"
)


class FetchError(Exception):
    pass


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(url, timeout=TIMEOUT_S, retries=RETRIES):
    """Bounded GET. Returns body metadata; raises FetchError after the last attempt."""
    last_error = "unknown error"
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                digest = hashlib.sha256()
                size = 0
                head = b""
                while True:
                    chunk = resp.read(65536)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > MAX_BYTES:
                        raise FetchError(f"body larger than {MAX_BYTES} bytes")
                    if len(head) < 256:
                        head = (head + chunk)[:256]
                    digest.update(chunk)
                return {
                    "http_status": resp.status,
                    "final_url": resp.geturl(),
                    "content_bytes": size,
                    "content_sha256": digest.hexdigest(),
                    "etag": resp.headers.get("ETag"),
                    "last_modified": resp.headers.get("Last-Modified"),
                    "head": head,
                }
        except FetchError:
            raise  # size limit: retrying would not help
        except urllib.error.HTTPError as exc:
            last_error = f"HTTP {exc.code}"
        except (urllib.error.URLError, OSError) as exc:  # TimeoutError is an OSError
            last_error = f"{type(exc).__name__}: {getattr(exc, 'reason', exc)}"
    raise FetchError(last_error)


def check_source(src):
    """Fetch one source and apply the body check. Returns {'state': ..., ...}."""
    try:
        meta = fetch(src["url"])
    except FetchError as exc:
        return {"state": "failed", "reason": str(exc)}
    head = meta.pop("head")
    if meta["http_status"] != 200:
        return {"state": "failed", "reason": f"HTTP {meta['http_status']}"}
    if src["kind"] != "html" and head.lower().lstrip().startswith(SHELL_PREFIXES):
        return {"state": "failed", "reason": "body is an HTML shell, not documentation"}
    meta["checked_at"] = utc_now()
    return {"state": "ok", "meta": meta}


def classify(src, meta):
    old = src.get("content_sha256")
    if old is None:
        return "baseline"
    return "unchanged" if old == meta["content_sha256"] else "changed"


def apply_result(src, meta):
    src["status"] = "verified"
    src["checked_at"] = meta["checked_at"]
    src["http_status"] = meta["http_status"]
    if meta["final_url"] != src["url"]:
        src["final_url"] = meta["final_url"]
    else:
        src.pop("final_url", None)
    src["content_sha256"] = meta["content_sha256"]
    src["content_bytes"] = meta["content_bytes"]
    for key in ("etag", "last_modified"):
        if meta.get(key):
            src[key] = meta[key]
        else:
            src.pop(key, None)


def changelog_line(exchange_id, src, kind, meta):
    old_sha = src.get("content_sha256")
    old_bytes = src.get("content_bytes")
    old_txt = old_sha[:12] if old_sha else "-"
    old_size = f"{old_bytes:,}" if old_bytes is not None else "-"
    return (
        f"- {meta['checked_at']} | {kind} | {exchange_id} | {src['url']} | "
        f"sha256 {old_txt} -> {meta['content_sha256'][:12]} | "
        f"{old_size} -> {meta['content_bytes']:,} bytes\n"
    )


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check official doc sources for changes.")
    ap.add_argument("--apply", action="store_true", help="record results in catalog.json and CHANGELOG.md")
    ap.add_argument("--exchange", action="append", default=[], help="limit to an exchange id (repeatable)")
    args = ap.parse_args(argv)

    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    jobs = [
        (ex, src)
        for ex in data["exchanges"]
        if not args.exchange or ex["id"] in args.exchange
        for src in ex["sources"]
    ]
    if not jobs:
        print("ERROR: no sources matched")
        return 2

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        results = list(pool.map(lambda job: check_source(job[1]), jobs))

    failed = 0
    counts = {"baseline": 0, "unchanged": 0, "changed": 0}
    log_lines = []
    for (ex, src), res in zip(jobs, results):
        if res["state"] == "failed":
            failed += 1
            print(f"FAILED    {ex['id']:<11} {src['url']}  ({res['reason']})")
            continue
        meta = res["meta"]
        kind = classify(src, meta)
        counts[kind] += 1
        print(f"{kind.upper():<9} {ex['id']:<11} {src['url']}  sha256 {meta['content_sha256'][:12]}"
              f"  {meta['content_bytes']:,} bytes")
        if kind in ("baseline", "changed"):
            log_lines.append(changelog_line(ex["id"], src, kind, meta))

    print(f"\nchecked {len(jobs)}: baseline {counts['baseline']}, unchanged {counts['unchanged']}, "
          f"changed {counts['changed']}, failed {failed}")

    if args.apply:
        for (ex, src), res in zip(jobs, results):
            if res["state"] == "ok":
                apply_result(src, res["meta"])
        CATALOG.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if log_lines:
            if not CHANGELOG.exists():
                CHANGELOG.write_text(CHANGELOG_HEADER, encoding="utf-8")
            with CHANGELOG.open("a", encoding="utf-8") as fh:
                fh.writelines(log_lines)
        print("applied: catalog.json updated"
              + (f", {len(log_lines)} line(s) appended to CHANGELOG.md" if log_lines else ""))
        print("next: python3 scripts/validate.py && python3 scripts/render.py")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
