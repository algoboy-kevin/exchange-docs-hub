# Exchange API documentation catalog

Generated from `catalog.json` by `scripts/render.py`. Do not edit by hand.

Links only: this catalog points to official documentation and does not mirror it.
A `verified` status means the URL returned a documentation body at the recorded
check time; it does not establish API correctness or completeness.

Sources: 20 total; 20 verified, 0 unverified, 0 blocked.

## Binance (`binance`)

| Kind | Status | Checked (UTC) | Content sha256 | URL | Description | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| llms-index | VERIFIED | 2026-11-05T06:56:52Z | 2101155962c8 | https://developers.binance.com/en/docs/llms.txt | Official documentation index (Binance Developer Docs) | Body checked: Markdown index with links to documentation pages. |
| llms-full | VERIFIED | 2026-11-05T06:56:54Z | 7fe8634d231e | https://developers.binance.com/en/docs/llms-full.txt | Complete Binance Developer Docs as one text file (about 8 MB) | Body checked: documentation text, not a JS shell. Large; download once and search locally. |
| markdown | VERIFIED | 2026-11-05T06:56:52Z | 7026aa5ae78b | https://developers.binance.com/en/docs/products/derivatives-trading-usds-futures/general-info.md | USDS-M Futures general API information (raw Markdown) | Body checked: Markdown API general information for USDS-M futures. |

## Hyperliquid (`hyperliquid`)

| Kind | Status | Checked (UTC) | Content sha256 | URL | Description | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| llms-index | VERIFIED | 2026-11-05T06:56:53Z | 1c712a65803e | https://hyperliquid.gitbook.io/hyperliquid-docs/llms.txt | Official Hyperliquid documentation index | Body checked: Markdown index including the public API section. |
| llms-full | VERIFIED | 2026-11-05T06:56:54Z | fb6cc4d6a297 | https://hyperliquid.gitbook.io/hyperliquid-docs/llms-full.txt | Hyperliquid documentation as one text file, paginated | Body checked: part 1 of 2 (pages 1-100 of 149) is documentation. Only part 1 was checked; follow the paging links for the rest. |
| markdown | VERIFIED | 2026-11-05T06:56:54Z | 156b8b0074c1 | https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api.md | Hyperliquid public API overview (raw Markdown) | Body checked: short overview page that links to endpoint pages such as the info endpoint. |

## Aster (`aster`)

| Kind | Status | Checked (UTC) | Content sha256 | URL | Description | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| llms-index | VERIFIED | 2026-11-05T07:23:22Z | ecc0f4aac4f6 | https://docs.asterdex.com/llms.txt | Official Aster documentation index | Body checked: Markdown index with links to documentation pages. |
| llms-full | VERIFIED | 2026-11-05T07:23:22Z | 534b6dcc62b3 | https://docs.asterdex.com/llms-full.txt | Aster documentation as one Markdown file, paginated | Body checked: part 1 of 3 (pages 1-100 of 204) is documentation. Only part 1 was checked; follow the paging links for the rest. |
| markdown | VERIFIED | 2026-11-05T07:23:22Z | 3ff00569be0a | https://docs.asterdex.com/for-developers/aster-api/api-documentation.md | Aster API documentation page (raw Markdown) | Body checked: Markdown page that points to the external API reference site for futures endpoints. |
| markdown | VERIFIED | 2026-11-05T07:23:22Z | 9be32a9a3565 | https://raw.githubusercontent.com/asterdex/api-docs/master/V3%28Recommended%29/EN/aster-finance-spot-api-v3.md | Aster Spot API v3 (sapi.asterdex.com, /api/v3), official asterdex GitHub repo | Candidate added from search 2026-11-05. Recommended spot API version per the repo folder name. |
| html | VERIFIED | 2026-11-05T07:23:23Z | 3ad08217f500 | https://asterdex.github.io/aster-api-website/spot-v3/general-info | Aster Spot API v3 general info (base URL, auth types, order statuses) | Candidate from search 2026-11-05. HTML spec page; fallback only. |

## Polymarket (`polymarket`)

| Kind | Status | Checked (UTC) | Content sha256 | URL | Description | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| llms-index | VERIFIED | 2026-11-05T07:23:22Z | fa077764b491 | https://docs.polymarket.com/llms.txt | Official Polymarket documentation index | Body checked: Markdown index with links to pages, the API reference index and OpenAPI specs. |
| llms-full | VERIFIED | 2026-11-05T07:23:23Z | 7d64aeb99088 | https://docs.polymarket.com/llms-full.txt | Polymarket documentation as one text file (about 1.8 MB) | Body checked: documentation text. Large; download once and search locally. |
| llms-index | VERIFIED | 2026-11-05T07:23:23Z | e8b2d4d24b50 | https://docs.polymarket.com/_llms/en/api-reference.txt | Polymarket English API reference index, with per-section text files and OpenAPI links | Body checked: Markdown index listing API reference sections and OpenAPI/AsyncAPI specs. |
| openapi | VERIFIED | 2026-11-05T07:23:23Z | 19268516978f | https://docs.polymarket.com/api-spec/clob-openapi.yaml | Polymarket CLOB API OpenAPI 3.1 specification (YAML) | Body checked: starts with openapi 3.1.0 and the Polymarket CLOB API title. |
| llms-index | VERIFIED | 2026-11-05T07:23:24Z | caa486bc0571 | https://docs.polymarket.com/_llms/en/api-reference/perps.txt | Polymarket Perps API reference index (about 102 pages) | Candidate from docs.polymarket.com/llms.txt entry (English / API Reference / Perps). |
| markdown | VERIFIED | 2026-11-05T07:23:24Z | ccafec27a6cb | https://docs.polymarket.com/api-reference/perps/overview.md | Polymarket Perps API overview (HTTP and WebSocket endpoints) | Candidate from search 2026-11-05. Lists api.perpetuals and ws.perpetuals hosts. |
| openapi | VERIFIED | 2026-11-05T07:23:24Z | 2f22b131a3f5 | https://docs.polymarket.com/api-spec/perps-openapi.json | Polymarket Perps OpenAPI spec | Candidate from docs.polymarket.com/llms.txt (perps-openapi). |
| openapi | VERIFIED | 2026-11-05T07:23:25Z | 5db88635f63f | https://docs.polymarket.com/asyncapi-perps.json | Polymarket Perps AsyncAPI spec (WebSocket channels and auth) | Candidate from docs.polymarket.com/llms.txt (asyncapi-perps). |
| openapi | VERIFIED | 2026-11-05T07:23:26Z | 94f937068bab | https://ws-live-v2.polymarket.com/asyncapi.json | Polymarket RTDS v2 AsyncAPI spec (replaces ws-live-data host) | Candidate from docs.polymarket.com/llms.txt (asyncapi). Host from the llms-full migration note. |
