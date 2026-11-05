# Catalog specification

## Goal and scope
Provide a minimal gateway to official exchange API docs, not a connector, a mirror or an API tutorial.
Complete the initial four venues only: Binance, Hyperliquid, Aster, Polymarket.

## Use cases (owner, 2026-11-05)
1. Quick LLM reference: `llms.txt` and the llms-full links, so an agent can find exchange docs in one fetch.
2. Versioned updates: `scripts/check_updates.py` hashes each source body (SHA-256, body discarded). A changed hash
   means the docs changed; `--apply` records it and appends `CHANGELOG.md`. Version = the content hash plus
   the check time, not a copied document.
3. Adding exchanges: new venues are added by editing `catalog.json` (see CONTRIBUTING.md "Adding a venue"). The
   owner approves each venue; the four current venues are the starting set, not a limit.

## Canonical schema
`catalog.json` is an object with `schema_version: 1` and `exchanges` array.
Each exchange has unique `id`, `name`, and nonempty `sources` array.
Each source has `url`, `kind` (llms-index, llms-full, markdown, text, openapi, html), `description`,
`status` (verified, unverified, blocked), `checked_at` (UTC ISO timestamp or null),
and `notes`. Optionally add `http_status` and `final_url` from actual fetches.
Use official URLs only. No duplicate URLs within one exchange. Never invent verification dates.
Seeds are candidates, not verified facts. For a failed fetch report the actual limitation; do not infer nonexistence.

## Completion deliverables
1. Verify or explicitly mark blocked each seed, prefer llms indexes/full text, and add up to two useful official raw Markdown/spec fallbacks per venue if discoverable quickly.
2. Produce CATALOG.md and llms.txt from the canonical data. Preserve blocked/unverified labels in both; no manual conflicting counts.
3. Add CONTRIBUTING.md explaining provenance, schema, bounded GET/body checks, and no secrets.
4. Add a small stdlib-only scripts/validate.py: offline validation of required fields, unique IDs/URLs, HTTPS, allowed enums, timestamp/status consistency. Exit nonzero on errors.
5. Add scripts/render.py to deterministically generate CATALOG.md and llms.txt from catalog.json, with --check mode to reject drift.
6. Update README with working usage commands and accurate scope/status; add docs/PROGRESS.md with actual validation results and limitations.

## Constraints and verification
No API credentials, account endpoints or order operations. Fetch public documentation only.
No dependency installation or browser automation needed. Max two parallel requests, bounded timeouts (20 seconds), at most one retry per URL. Download larger content once to scratch, never commit it.
Do not spend time on broader prior-art research or add more exchanges.
Acceptance: `python3 scripts/validate.py`; `python3 scripts/render.py --check`.
Both must run successfully. Do not label unreachable endpoints verified; honest blocked entries are acceptable.
