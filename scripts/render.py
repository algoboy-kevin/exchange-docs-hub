#!/usr/bin/env python3
"""Deterministically render CATALOG.md and llms.txt from catalog.json (stdlib only).

Usage:
  python3 scripts/render.py          # write CATALOG.md and llms.txt
  python3 scripts/render.py --check  # exit 1 if committed files differ from the output
"""
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import validate_catalog  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "catalog.json"
OUTPUTS = {"CATALOG.md": ROOT / "CATALOG.md", "llms.txt": ROOT / "llms.txt"}

STATUS_LABEL = {
    "verified": "VERIFIED",
    "unverified": "UNVERIFIED (candidate, not checked)",
    "blocked": "BLOCKED (fetch failed or inaccessible)",
}


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def _summary(exchanges):
    counts = {"verified": 0, "unverified": 0, "blocked": 0}
    for ex in exchanges:
        for src in ex["sources"]:
            counts[src["status"]] += 1
    return counts


def render_catalog_md(data):
    exchanges = data["exchanges"]
    counts = _summary(exchanges)
    total = sum(counts.values())
    lines = [
        "# Exchange API documentation catalog",
        "",
        "Generated from `catalog.json` by `scripts/render.py`. Do not edit by hand.",
        "",
        "Links only: this catalog points to official documentation and does not mirror it.",
        "A `verified` status means the URL returned a documentation body at the recorded",
        "check time; it does not establish API correctness or completeness.",
        "",
        f"Sources: {total} total; {counts['verified']} verified, "
        f"{counts['unverified']} unverified, {counts['blocked']} blocked.",
        "",
    ]
    for ex in exchanges:
        lines += [f"## {ex['name']} (`{ex['id']}`)", "",
                  "| Kind | Status | Checked (UTC) | Content sha256 | URL | Description | Notes |",
                  "| --- | --- | --- | --- | --- | --- | --- |"]
        for src in ex["sources"]:
            sha = src.get("content_sha256")
            lines.append(
                f"| {_cell(src['kind'])} | {_cell(STATUS_LABEL[src['status']])} "
                f"| {_cell(src.get('checked_at') or '-')} "
                f"| {_cell(sha[:12] if sha else '-')} "
                f"| {_cell(src['url'])} | {_cell(src['description'])} | {_cell(src['notes'])} |"
            )
        lines.append("")
    return "\n".join(lines)


def render_llms_txt(data):
    exchanges = data["exchanges"]
    counts = _summary(exchanges)
    lines = [
        "# Exchange Docs Hub",
        "",
        "> Links to official exchange API documentation in LLM-friendly formats "
        "(Binance, Hyperliquid, Aster, Polymarket). Links only; no mirrored content.",
        "> Status labels: verified = body checked at recorded time; unverified = candidate "
        "not yet checked; blocked = fetch failed.",
        f"> Sources: {sum(counts.values())} total; {counts['verified']} verified, "
        f"{counts['unverified']} unverified, {counts['blocked']} blocked.",
        "",
    ]
    for ex in exchanges:
        lines.append(f"## {ex['name']}")
        lines.append("")
        for src in ex["sources"]:
            lines.append(
                f"- [{src['kind']}: {src['description']}]({src['url']}) "
                f"[{src['status']}]"
            )
        lines.append("")
    return "\n".join(lines)


def render_all(data):
    return {
        "CATALOG.md": render_catalog_md(data).rstrip("\n") + "\n",
        "llms.txt": render_llms_txt(data).rstrip("\n") + "\n",
    }


def main(argv):
    check = "--check" in argv[1:]
    unknown = [a for a in argv[1:] if a != "--check"]
    if unknown:
        print(f"ERROR: unknown arguments: {unknown}")
        return 2
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors = validate_catalog(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}")
        print("refusing to render: catalog.json is invalid")
        return 1
    rendered = render_all(data)
    if not check:
        for name, text in rendered.items():
            OUTPUTS[name].write_bytes(text.encode("utf-8"))
            print(f"wrote {name}")
        return 0
    drift = False
    for name, text in rendered.items():
        path = OUTPUTS[name]
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current != text:
            drift = True
            print(f"DRIFT: {name} is out of date with catalog.json")
            diff = difflib.unified_diff(current.splitlines(), text.splitlines(),
                                        f"{name} (on disk)", f"{name} (rendered)", lineterm="")
            for line in list(diff)[:40]:
                print(line)
        else:
            print(f"ok: {name} matches catalog.json")
    if drift:
        print("run: python3 scripts/render.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
