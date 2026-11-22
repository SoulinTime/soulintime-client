# Changelog

Statement format and public API. Dates are UTC.

## 2026-11-23
- Agent card now starts with the signed-out request curl and a curl that verifies an existing statement.
- Responses carry `X-SoulInTime-Request-Id` and `X-Statement-Spec: sit-statement/0.1`; a failed calendar submit answers `"calendar_submit":"failed"`.
- `firsts.json` (confirmed statements only) at https://soulintime.com/firsts.json; live list `v1Statement?firsts=1` (optional `since`).
- Plain-text export `v1Statement?hash=<sha256>&format=text`; status `v1Statement?health=1` and https://soulintime.com/status.
- Verifier test vectors (valid, tampered, wrong key, refused) in `verifier/vectors/`; verifier release 0.1.0 hashes in `verifier/RELEASE.md`.
- Examples: createStatement (Python, JS), git hook, GitHub Action (example only), email-inbound and share-target sketches.
- Spec v0.1 pinned; size and field limits and the export URL pattern added (no field changes).

## 2026-11-22
- `sit-statement/0.1` live: signed statements on confirmation, signed refusals, signing key `0a64aa45b8ce17a7` and its fingerprint dated at block 977076.
