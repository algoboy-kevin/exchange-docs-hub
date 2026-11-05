# Progress

## Status (P1)

- Four venues: Binance, Hyperliquid, Aster, Polymarket.
- 13 sources in `catalog.json`: 13 verified, 0 unverified, 0 blocked.
- Generated: `CATALOG.md`, `llms.txt`, from `catalog.json` by `scripts/render.py`.
- Tooling: `scripts/validate.py` (offline, stdlib), `scripts/render.py` (with `--check`).

## Verification (2026-11-05)

Each source was fetched with a bounded GET (20-second timeout, one retry at most) and its
body was checked for documentation content, not an app shell or challenge page. Every
fetch returned HTTP 200.

| Venue | Source | Kind | Body check |
| --- | --- | --- | --- |
| Binance | developers.binance.com/en/docs/llms.txt | llms-index | Documentation index |
| Binance | developers.binance.com/en/docs/llms-full.txt | llms-full | Documentation text (about 8 MB) |
| Binance | …/products/derivatives-trading-usds-futures/general-info.md | markdown | Markdown API general info (served as octet-stream) |
| Hyperliquid | hyperliquid.gitbook.io/hyperliquid-docs/llms.txt | llms-index | Documentation index |
| Hyperliquid | …/llms-full.txt | llms-full | Part 1 of 2 (pages 1–100 of 149) is documentation |
| Hyperliquid | …/for-developers/api.md | markdown | Public API overview |
| Aster | docs.asterdex.com/llms.txt | llms-index | Documentation index |
| Aster | docs.asterdex.com/llms-full.txt | llms-full | Part 1 of 3 (pages 1–100 of 204) is documentation |
| Aster | …/for-developers/aster-api/api-documentation.md | markdown | Markdown page |
| Polymarket | docs.polymarket.com/llms.txt | llms-index | Documentation index |
| Polymarket | docs.polymarket.com/llms-full.txt | llms-full | Documentation text (about 1.8 MB) |
| Polymarket | docs.polymarket.com/_llms/en/api-reference.txt | llms-index | API reference index with OpenAPI links |
| Polymarket | docs.polymarket.com/api-spec/clob-openapi.yaml | openapi | OpenAPI 3.1.0, Polymarket CLOB API |

Large downloads were kept in the scratch directory and not committed.

## Acceptance results

- `python3 scripts/validate.py`: `validation ok: 4 exchanges, 13 sources` (exit 0).
- `python3 scripts/render.py --check`: `ok` for `CATALOG.md` and `llms.txt` (exit 0).
- Negative checks: `render.py --check` reports drift after an edit to `CATALOG.md`
  (exit 1). `validate.py` rejects an http URL, an invalid status, and a verified source
  with no `checked_at` (exit 1).

## Limitations

- `checked_at` is one batch timestamp (`2026-11-05T06:47:19Z`) taken after the fetches
  ran, not a per-request time. Individual fetches ran roughly in the 06:45–06:47 UTC
  window.
- Only part 1 of the paginated Hyperliquid and Aster `llms-full.txt` files was checked.
  Later parts were not fetched.
- The validator checks schema and consistency only. It does not re-fetch URLs, so
  `verified` reflects the recorded check, not a live state.
- Reachability and documentation-body checks do not establish API correctness or
  completeness. Sources remain authoritative.
- No exchange API calls, credentials, or account endpoints were used.
