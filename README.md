# Exchange Docs Hub

A small, public gateway to official exchange API documentation in LLM-friendly formats.
Links and original annotations only: this repository does not mirror third-party documentation.

## Status

Scaffold published. Initial catalog verification is in progress; candidate URLs are not yet certified reachable.
Initial scope: Binance, Hyperliquid, Aster, and Polymarket.

## Retrieval order

1. Start with the official `llms.txt` index.
2. Download `llms-full.txt` once when available; search it locally.
3. Follow selected Markdown, raw text, OpenAPI/Swagger YAML or JSON links.
4. Use HTML only as a documented fallback.

An HTTP 200 alone is not verification: check the body for documentation rather than an app shell or challenge.

## Layout

- `catalog.json`: canonical link registry; seed candidates initially marked unverified.
- `docs/SPEC.md`: catalog fields, scope, and acceptance criteria.
- `HANDOVER.md`: completion handoff.
- Planned: `CATALOG.md`, `llms.txt`, contribution guidance and an offline validator.

Sources remain authoritative. Reachability checks do not establish API correctness or completeness.
