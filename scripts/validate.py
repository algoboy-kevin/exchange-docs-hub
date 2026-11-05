#!/usr/bin/env python3
"""Offline validator for catalog.json (stdlib only, no network access).

Usage: python3 scripts/validate.py [path/to/catalog.json]
Exits 0 when the catalog is valid, 1 otherwise.
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

KINDS = {"llms-index", "llms-full", "markdown", "text", "openapi", "html"}
STATUSES = {"verified", "unverified", "blocked"}
ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SOURCE_REQUIRED = ("url", "kind", "description", "status", "checked_at", "notes")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OPTIONAL_TEXT = ("etag", "last_modified")

DEFAULT_PATH = Path(__file__).resolve().parent.parent / "catalog.json"


def _valid_timestamp(value):
    if not isinstance(value, str) or not TIMESTAMP_RE.match(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return False
    return True


def _check_https(url, where, errors):
    parts = urlsplit(url) if isinstance(url, str) else None
    if not parts or parts.scheme != "https" or not parts.netloc:
        errors.append(f"{where}: url must be an absolute https URL: {url!r}")


def validate_catalog(data):
    """Return a list of error strings for a parsed catalog (empty when valid)."""
    errors = []
    if not isinstance(data, dict):
        return ["top level must be an object"]
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    exchanges = data.get("exchanges")
    if not isinstance(exchanges, list) or not exchanges:
        errors.append("exchanges must be a nonempty array")
        return errors

    seen_ids = set()
    seen_urls = {}
    for i, ex in enumerate(exchanges):
        label = f"exchanges[{i}]"
        if not isinstance(ex, dict):
            errors.append(f"{label}: must be an object")
            continue
        ex_id = ex.get("id")
        if not isinstance(ex_id, str) or not ID_RE.match(ex_id):
            errors.append(f"{label}: id must match {ID_RE.pattern}: {ex_id!r}")
        else:
            label = f"exchange '{ex_id}'"
            if ex_id in seen_ids:
                errors.append(f"{label}: duplicate id")
            seen_ids.add(ex_id)
        if not isinstance(ex.get("name"), str) or not ex.get("name", "").strip():
            errors.append(f"{label}: name must be a nonempty string")
        sources = ex.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{label}: sources must be a nonempty array")
            continue
        for j, src in enumerate(sources):
            where = f"{label} sources[{j}]"
            if not isinstance(src, dict):
                errors.append(f"{where}: must be an object")
                continue
            for field in SOURCE_REQUIRED:
                if field not in src:
                    errors.append(f"{where}: missing field '{field}'")
            url = src.get("url")
            _check_https(url, where, errors)
            if isinstance(url, str):
                if url in seen_urls:
                    errors.append(f"{where}: duplicate url (also at {seen_urls[url]})")
                else:
                    seen_urls[url] = where
            if src.get("kind") not in KINDS:
                errors.append(f"{where}: kind must be one of {sorted(KINDS)}")
            if not isinstance(src.get("description"), str) or not src.get("description", "").strip():
                errors.append(f"{where}: description must be a nonempty string")
            if not isinstance(src.get("notes"), str):
                errors.append(f"{where}: notes must be a string")
            status = src.get("status")
            if status not in STATUSES:
                errors.append(f"{where}: status must be one of {sorted(STATUSES)}")
            checked_at = src.get("checked_at")
            if checked_at is not None and not _valid_timestamp(checked_at):
                errors.append(f"{where}: checked_at must be null or a UTC ISO timestamp like 2026-01-02T03:04:05Z")
            if status == "verified":
                if checked_at is None:
                    errors.append(f"{where}: verified source needs checked_at")
                if src.get("http_status") != 200:
                    errors.append(f"{where}: verified source needs http_status 200")
            if status == "unverified" and checked_at is not None:
                errors.append(f"{where}: unverified source must have checked_at null")
            if "http_status" in src and (
                not isinstance(src["http_status"], int) or isinstance(src["http_status"], bool)
            ):
                errors.append(f"{where}: http_status must be an integer")
            if "final_url" in src:
                _check_https(src["final_url"], f"{where} final_url", errors)
            sha = src.get("content_sha256")
            if status == "verified" and sha is None:
                errors.append(f"{where}: verified source needs content_sha256 "
                              "(run scripts/check_updates.py --apply)")
            if sha is not None and not (isinstance(sha, str) and SHA256_RE.match(sha)):
                errors.append(f"{where}: content_sha256 must be 64 lowercase hex characters")
            if "content_bytes" in src and (
                not isinstance(src["content_bytes"], int)
                or isinstance(src["content_bytes"], bool)
                or src["content_bytes"] < 0
            ):
                errors.append(f"{where}: content_bytes must be a non-negative integer")
            if sha is None and "content_bytes" in src:
                errors.append(f"{where}: content_bytes without content_sha256")
            for key in OPTIONAL_TEXT:
                if key in src and (not isinstance(src[key], str) or not src[key].strip()):
                    errors.append(f"{where}: {key} must be a nonempty string when present")
    return errors


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read {path}: {exc}")
        return 1
    errors = validate_catalog(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        print(f"validation failed: {len(errors)} error(s)")
        return 1
    total = sum(len(ex["sources"]) for ex in data["exchanges"])
    print(f"validation ok: {len(data['exchanges'])} exchanges, {total} sources")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
