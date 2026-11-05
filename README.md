# Exchange Docs Hub

A small, public gateway to official exchange API documentation in LLM-friendly formats.
Links and original annotations only: this repository does not mirror third-party documentation.

## Status

The initial four-venue catalog is complete: Binance, Hyperliquid, Aster, and Polymarket.
13 sources are listed. All 13 were checked on 2026-11-05 with a bounded GET, and each
response body was checked to be documentation rather than an app shell. None are blocked.
Only the first part of the paginated Hyperliquid and Aster `llms-full.txt` files was
checked. See `docs/PROGRESS.md` for the exact results and limitations.

Reachability checks do not establish API correctness or completeness.

## Usage

Validate the catalog offline (standard library only):

```sh
python3 scripts/validate.py
```

Regenerate `CATALOG.md` and `llms.txt` from `catalog.json`:

```sh
python3 scripts/render.py
```

Check that the generated files match the catalog (exits nonzero on drift):

```sh
python3 scripts/render.py --check
```

Check the official sources for changes (network; hashes each body, stores no text):

```sh
python3 scripts/check_updates.py                  # report only
python3 scripts/check_updates.py --apply          # record and append CHANGELOG.md
```

Run `validate` and `render` after `--apply`.

## Retrieval order

1. Start with the official `llms.txt` index.
2. Download `llms-full.txt` once when available; search it locally.
3. Follow selected Markdown, raw text, OpenAPI/Swagger YAML or JSON links.
4. Use HTML only as a documented fallback.

An HTTP 200 alone is not verification: check the body for documentation rather than an app shell or challenge.

## Layout

- `catalog.json`: canonical link registry (source of truth).
- `CATALOG.md`, `llms.txt`: generated from `catalog.json`; do not edit by hand.
- `scripts/validate.py`: offline schema validator.
- `scripts/render.py`: generator, with `--check` mode.
- `docs/SPEC.md`: catalog fields, scope, and acceptance criteria.
- `docs/PROGRESS.md`: validation results and limitations.
- `CONTRIBUTING.md`: provenance rules, schema, and contribution steps.
- `HANDOVER.md`: completion handoff.

Sources remain authoritative.
