# Changelog

Statement format and public API. Dates are UTC.

## 2026-11-23
- API v1 (JSON, CORS, no key): `POST /functions/apiV1Receipts`, `GET /functions/apiV1Verify?hash=`, `GET /functions/apiV1Receipts?id=`. Statuses `pending|in_calendar|anchored`; `height` only when anchored; `cite` only with a signed statement; `next_action` in every answer; 409 for an existing hash, 429 with `reset_at`. OpenAPI 3.1 at `/.well-known/openapi-v1.yaml`. At `/functions/` because Base44 has no custom `/api` routes. Older endpoints unchanged.
- MCP `stamp` results carry `next_action` (`cite`, `verify_later`, `retry_after`).
- Firsts `since` filter fixed: it now dedupes by earliest block before filtering (`since=977100` no longer returns the fingerprint at a later block).
- `create_statement.py`/`.mjs`: `--watch`, print the cite line and statement URL once confirmed. GitHub Action example: warning, release-tag pattern, "date these files" sketch.
- Cite line: `sha256 <hash> existed by Bitcoin block <N>. Statement: <url>` via `v1Statement?hash=&format=cite`, header `X-SoulInTime-Cite`, `?with=cite`, MCP `stamp`, the plain-text export and the Forward text. The signed statement is unchanged.
- Refusals from `createMoment` carry `"statement":null,"cite":null` and `do_not_cite`; `already_stamped` for a confirmed hash carries the existing statement and cite.
- Statement card URL `functions/statementCard?hash=` (unfurls with hash and block); Markdown and HTML snippets.
- Firsts rows carry `cite`; `min_block` alias for `since`.
- GitHub Action example completed: hash each release asset, request signed out, print the cite line (example only).
- Agent card now starts with the signed-out request curl and a curl that verifies an existing statement.
- Responses carry `X-SoulInTime-Request-Id` and `X-Statement-Spec: sit-statement/0.1`; a failed calendar submit answers `"calendar_submit":"failed"`.
- `firsts.json` (confirmed statements only) at https://soulintime.com/firsts.json; live list `v1Statement?firsts=1` (optional `since`).
- Plain-text export `v1Statement?hash=<sha256>&format=text`; status `v1Statement?health=1` and https://soulintime.com/status.
- Verifier test vectors (valid, tampered, wrong key, refused) in `verifier/vectors/`; verifier release 0.1.0 hashes in `verifier/RELEASE.md`.
- Examples: createStatement (Python, JS), git hook, GitHub Action (example only), email-inbound and share-target sketches.
- Spec v0.1 pinned; size and field limits and the export URL pattern added (no field changes).

## 2026-11-22
- `sit-statement/0.1` live: signed statements on confirmation, signed refusals, signing key `0a64aa45b8ce17a7` and its fingerprint dated at block 977076.
