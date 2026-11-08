# SoulInTime client and MCP

SoulInTime dates bytes by Bitcoin block height. The receipt shows that these exact bytes existed by that block. It does not show that the contents are true.

## Test without creating

This reads an existing sealed receipt. It does not create anything, and it needs no account or key:

```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

Expected: `"status":"confirmed"`, `"blockHeight":965906`, slug `a-hash-is-a-door-that-2026-019bd305`, and a `proofFile`.
Receipt page: https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305

Check it yourself, without us:

```
curl -L -o door.ots 'https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1'
ots verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f door.ots
```

(`pip install opentimestamps-client` gives you `ots`. Without a Bitcoin node, run `ots info door.ots` and compare the merkle root it prints with block 965906 on any block explorer.)

## Citation rule (refuse otherwise)

- Cite `slug@height` only when v1Verify returns `status` `confirmed`, a positive `blockHeight` and a `proofFile`. Example: `a-hash-is-a-door-that-2026-019bd305@965906`.
- If a receipt is pending, `height_asserted`, missing, or has no proof file, refuse to cite it. Say it is pending or missing.
- The chain tip is never a receipt's height. A caption or date is not proof.
- `first_at` (v1FirstAt) returns the earliest confirmed public receipt for a hash at or before height N. It is not a global history of the bytes. Unlisted and private receipts never appear in it.
- No keys. Only the SHA-256 is sent; your file bytes stay with you. Checking is free.

## Hosted MCP

`https://soulintime.com/functions/mcp`: stateless Streamable HTTP (POST). It has three tools:
- `verify(hash)`: read-only.
- `first_at(hash, height?)`: read-only.
- `stamp(hash)`: creates a receipt. It is never an evaluation call.

Notes:
- To evaluate, use `verify` with the hash above.
- Hosted calls share the backend's network egress and may share the upstream rate limit. There is no per-user allowance. Respect 429 and `X-RateLimit-Reset`.

## Local MCP (`mcp-local/`)

This is the source of the same 0.1.0 package that is downloadable from https://soulintime.com/functions/mcpDownload. It speaks stdio. See `mcp-local/README.md` for install, host configuration and tests.

The packaged README text predates the hosted endpoint and says no hosted endpoint is claimed. The hosted MCP above now exists, and it is separate.

Differences from the hosted MCP:
- Both only check the citation against server metadata. Neither downloads or cryptographically verifies the `.ots`.
- The hosted MCP also requires `proofFile` to be the canonical `https://soulintime.com/functions/v1Proof?id=<slug>&ots=1` URL. The local package does not check this.

Tests: `test_http.py` mocks all HTTP. `test_protocol.py` mocks every stamp and every case but the last one, which is one live read-only `verify` GET of the hash above. It never makes a live POST.

## Reference client (`reference-client/soulintime_client.py`)

This is the same code that is published in https://soulintime.com/llms.txt, and it uses the standard library only.

How it works:
- It hashes locally and **POSTs the hash to createMoment, so running it creates a receipt.**
- It then polls v1Verify until the receipt is confirmed or failed, and saves the `.ots`.
- It prints CONFIRMED only for `confirmed` with a `proofFile`.

Effects:
- One fresh hash per network per hour.
- An accepted stamp is a new registry entry, unlisted by default, and it will get calendar commitments.
- To test without side effects, use the curl above, not this script.

## Limits

- Registry queries (v1Verify, v1FirstAt, Firsts) depend on soulintime.com. A downloaded `.ots` stays checkable with any OpenTimestamps client if this host disappears.
- Stamp is covered only by mocked tests here. These tests make no real stamps.
- API contract: https://soulintime.com/llms.txt and https://soulintime.com/.well-known/openapi.yaml

## License

Not yet chosen by the owner. No license is granted.
