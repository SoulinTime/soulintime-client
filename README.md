# Test without creating

Sealed hash: `019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f`

Live receipt: [https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305](https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305) (block 965906)

Latest sealed example: block 965906 (permanent test object).

Citation rule: cite `slug@height` only when status is `confirmed` and `proofFile` exists; otherwise refuse.

Check it on the web: [https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f](https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f)

Hosted MCP: [https://soulintime.com/functions/mcp](https://soulintime.com/functions/mcp). Point any MCP client that supports remote Streamable HTTP servers at this URL. No key is needed. Call `verify` with the sealed hash.

Local MCP package: [https://soulintime.com/functions/mcpDownload](https://soulintime.com/functions/mcpDownload)

Running the reference client creates a receipt. The curl below does not.

The hash is computed on your device; original file bytes stay there.

The `.ots` proof verifies without this host.

We did not invent the calendar. [OpenTimestamps](https://github.com/opentimestamps) did. We are the receipt and the refusal layer on top of it.

```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

Expected: `"status":"confirmed"`, `"blockHeight":965906`, `"slug":"a-hash-is-a-door-that-2026-019bd305"`, and a `proofFile`.

## Run locally

- Local stdio MCP server, same read-only `verify` and `first_at` tools: see [mcp-local/README.md](mcp-local/README.md).
- Setup: `python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt && .venv/bin/python server.py` inside `mcp-local/`.
- Then call `verify` with the sealed hash above; `stamp` creates a receipt.

## Proof download and check

Download the proof: [a-hash-is-a-door-that-2026-019bd305.ots](https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1)

```
ots verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f a-hash-is-a-door-that-2026-019bd305.ots
```

`ots` comes from `pip install opentimestamps-client`. Without a Bitcoin node, run `ots info` and compare the merkle root with block 965906 on any explorer.

## Refusal (copy this)

When a receipt is pending, `height_asserted`, missing, or has no proof file, an agent should say:

> "I will not cite a height for this hash. Status is not confirmed or no proofFile exists."

Further rules:
- The chain tip is never a receipt's height.
- A caption or a date is not proof.
- A height dates the bytes; it does not show that the contents are true.
- `first_at` (v1FirstAt) returns the earliest confirmed **public** receipt for a hash at or before height N. It is not a global history, and unlisted and private receipts never appear in it.
- No keys. Only the SHA-256 is sent.

The MCP tools (hosted and local) check this rule against server metadata only. They do not cryptographically verify the `.ots`; for that, use `ots verify`.

## Rate limits

Creating is limited; reads are not unlimited either.

Creating a receipt (createMoment):
- The limit is one fresh hash per network per hour.
- A second create inside that hour, or a hash that already has a receipt, returns `429` with the existing slug when that receipt is not private.
- `already_stamped` is permanent and does not clear when the hour resets. Read the existing receipt instead.

Reading (v1Verify):
- Responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). A read we observed carried `X-RateLimit-Limit: 120`. The window isn't documented, so follow the headers.

On 429:
- Wait until `X-RateLimit-Reset` and don't tight-loop.
- Hosted MCP calls share the backend's network egress, so they may share the upstream allowance. There is no per-user allowance.

Checking stays free. More volume than the free rate needs a paid path, which isn't offered yet.

Need more than the free rate? Email Soulintimeofficial@gmail.com with the hash and the use.

Volume brief (test without creating, free limits, what to email): [volume-brief.md](volume-brief.md)

## Hosted vs local MCP

Hosted (`/functions/mcp`):
- Stateless Streamable HTTP over POST.
- Tools `verify(hash)` and `first_at(hash, height?)` are read-only.
- `stamp(hash)` creates a receipt and is never an evaluation call.

Local (`mcp-local/`):
- This is the source of the same 0.1.0 package served by the download link. It speaks stdio.
- See `mcp-local/README.md` for setup. That README predates the hosted endpoint.
- The hosted MCP also checks that `proofFile` is the canonical `v1Proof?id=<slug>&ots=1` URL. The local one does not.

Tests:
- `test_http.py` mocks all HTTP.
- `test_protocol.py` mocks every stamp. Its last case is one live read-only `verify` GET of the sealed hash, which runs when you run the file. It never makes a live POST.

---

**CREATES A RECEIPT.**

## Reference client

`reference-client/soulintime_client.py` is the same code published in [llms.txt](https://soulintime.com/llms.txt), standard library only. Running it **creates a receipt**:
- It POSTs the hash to createMoment.
- It polls v1Verify and saves the `.ots`.
- An accepted stamp is a new registry entry, unlisted by default.

To test without side effects, use the curl at the top instead.

## Host dependence

Registry queries (v1Verify, v1FirstAt, Firsts) depend on soulintime.com. A downloaded `.ots` stays checkable with any OpenTimestamps client without it.

API contract: [llms.txt](https://soulintime.com/llms.txt) and [openapi.yaml](https://soulintime.com/.well-known/openapi.yaml).

## Status

Gmail parked; price UNSET; HQ post pending; public non-house firsts: 0.

Permanent sealed object: 965906. Public firsts that are not house examples: 0.

## License

[MIT](LICENSE)
