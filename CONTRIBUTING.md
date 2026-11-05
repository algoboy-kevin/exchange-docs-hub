# Contributing

This repository is a link catalog. It points to official exchange API documentation and
does not mirror, copy, or summarize third-party content.

## Provenance

- Use only official URLs published by the exchange (its developer docs site, its
  documented OpenAPI/AsyncAPI specs, or its documented `llms.txt` index).
- Record a source as `verified` only after a bounded GET returned a documentation body
  (not an app shell, login page, or challenge page) and the check time was recorded.
- Seed or candidate URLs stay `unverified` until checked. A failed fetch is recorded as
  `blocked` with the actual limitation (status code, timeout, shell page). Do not infer
  that a page does not exist.
- Never invent `checked_at` values. Use the UTC time of the actual check.

## Schema

`catalog.json` is the only source of truth. `CATALOG.md` and `llms.txt` are generated.

- Top level: `schema_version` (must be `1`) and `exchanges` (nonempty array).
- Each exchange: `id` (lowercase, unique), `name`, and a nonempty `sources` array.
- Each source:
  - `url`: absolute `https://` URL, unique across the catalog.
  - `kind`: one of `llms-index`, `llms-full`, `markdown`, `text`, `openapi`, `html`.
  - `description`: short, nonempty.
  - `status`: one of `verified`, `unverified`, `blocked`.
  - `checked_at`: UTC ISO timestamp (`YYYY-MM-DDTHH:MM:SSZ`) or `null`.
    `verified` requires a timestamp; `unverified` requires `null`.
  - `notes`: string describing what was checked or why it is blocked.
  - `http_status` (optional): integer from the actual fetch. `verified` requires 200.
  - `final_url` (optional): `https://` URL after redirects.

## Checking a source

- Prefer the `llms.txt` index, then `llms-full.txt`. Download a large file once to a
  scratch directory, search it locally, and do not commit it.
- Other fallbacks are raw Markdown pages, text, or OpenAPI specs. Use HTML only as a
  last resort.
- Limit requests: at most two in parallel, a 20-second timeout per request, and at most
  one retry per URL.
- Check the response body, not only the status code.
- Only public documentation GET requests are allowed. Do not call exchange API
  endpoints, account or order endpoints, or anything that needs credentials.

## Making a change

1. Edit `catalog.json`.
2. Run `python3 scripts/validate.py`. It is offline, uses only the standard library, and
   exits nonzero on any error.
3. Run `python3 scripts/render.py` to regenerate `CATALOG.md` and `llms.txt`.
4. Run `python3 scripts/render.py --check` to confirm the generated files match.
5. Do not add secrets, credentials, private local paths, or session details to any file.

## Checking for updates

    python3 scripts/check_updates.py                 # report only
    python3 scripts/check_updates.py --apply         # record hashes, append CHANGELOG.md
    python3 scripts/check_updates.py --exchange binance --apply

Each source is fetched once (20 s timeout, one retry, two in parallel). The body is hashed and
discarded. Results: `BASELINE` (first hash), `UNCHANGED`, `CHANGED`, `FAILED` (with the reason).
A failed fetch never changes recorded state. After `--apply`, run validate and render.

Fields added by the checker: `content_sha256` (64 hex), `content_bytes`, optional `etag`,
`last_modified`. `verified` sources require `content_sha256`.

## Adding a venue

1. Confirm the official docs URLs (llms index first, then llms-full, then markdown or OpenAPI).
2. Add the entry to `catalog.json` with `status: unverified` and `checked_at: null`.
3. Run `python3 scripts/check_updates.py --exchange <id> --apply`. Sources move to verified only
   after the body check passes.
4. Update the venue list in `docs/SPEC.md` and `README.md`, then validate and render.

## Scope

Starting set: Binance, Hyperliquid, Aster, Polymarket. Other venues are added through the
steps above. The owner approves each venue.
