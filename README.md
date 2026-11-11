# Test without creating

Two sealed examples now exist. **Non-house example: Bitcoin whitepaper abstract**, [`moment-ao91b5a0@975352`](https://soulintime.com/moment/moment-ao91b5a0). SHA-256 `d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa`. [Download .ots](https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1). Last verified: 2026-11-11.

The Door below remains the permanent test object at block 965906.

Sealed hash: `019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f`

Live receipt: [https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305](https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305) (block 965906)

Latest sealed example: Bitcoin whitepaper abstract, moment-ao91b5a0 at block 975352 (non-house). Door: block 965906 (permanent test object).

Citation rule: cite `slug@height` only when status is `confirmed` and `proofFile` exists; otherwise refuse.

Check it on the web: [https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f](https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f)

Hosted MCP: [https://soulintime.com/functions/mcp](https://soulintime.com/functions/mcp). Point any MCP client that supports remote Streamable HTTP servers at this URL. No key is needed. Call `verify` with the sealed hash.

Local MCP package: [https://soulintime.com/functions/mcpDownload](https://soulintime.com/functions/mcpDownload)

Running the reference client creates a receipt. The curl below does not.

The hash is computed on your device; original file bytes stay there.

The `.ots` proof verifies without this host.

We did not invent the calendar. [OpenTimestamps](https://github.com/opentimestamps) did. We are the receipt and the refusal layer on top of it.

<!-- last verified 2026-11-11 -->
```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

Before citing: call verify or first_at. Cite only status confirmed with proofFile; otherwise refuse. You may attach the .ots URL.
Pending receipts are never cited.
Agent checklist: https://soulintime.com/agent-checklist.md

Expected: `"status":"confirmed"`, `"blockHeight":965906`, `"slug":"a-hash-is-a-door-that-2026-019bd305"`, and a `proofFile`.

<!-- last verified 2026-11-11 -->
Second example (read only):
```sh
curl -s 'https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa'
```
Expected: status confirmed, blockHeight 975352 and proofFile.

/yours supports signed-out device receipts; account-owned receipts require sign-in.

## Pricing and private stamp balance

Free check stays free forever, subject to existing read limits. No account required to check or buy.

Recommended: Monthly — 100 stamps / 30 days, $99 USD plus applicable tax by card: https://buy.stripe.com/eVqcN55pH73n2Kyfms8IU01. One payment, 30 days. No auto-renew. Buy again to continue. Lightning reference price: 168,000 sats; Lightning checkout is paused, do not pay. Starter pack — 10 stamps / 90 days: $20 USD plus applicable tax by card (https://buy.stripe.com/7sY6oH9FXcnH1Gu7U08IU00); Lightning reference price 21,000 sats. https://soulintime.com/pricing. Next review: 1 Jan 2027. No account required to check or buy. Verified card payment unlocks your private balance at https://soulintime.com/unlocked. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.


Keep the returned private book key securely. Browser submissions use the saved key; API callers send `X-SoulInTime-Book: <private book key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt. See https://soulintime.com/paid-ready.md for exact counters and the signed fulfillment path.

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Non-house firsts: 1. Last verified (both sealed examples): 2026-11-11.

Proofs use OpenTimestamps: https://opentimestamps.org/


## Public destinations

- [Whitepaper discussion](https://github.com/SoulinTime/soulintime-client/discussions/1) — curl + moment link only.
- [Who this is for](https://soulintime.com/who) · [Benefits JSON](https://soulintime.com/benefits.json) · [Payment/unlock status](https://soulintime.com/status)
- [Private balance return page](https://soulintime.com/unlocked) (keep its key private).
- Listed on: the [official MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest) (`io.github.MorrisMoe/soulintime`) and [Glama](https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime).

- [Homepage: whitepaper first, permanent Door beneath](https://soulintime.com/)
- [Developers and Pricing](https://soulintime.com/developers) · [Pricing](https://soulintime.com/pricing)
- [Agent contract](https://soulintime.com/agents.json) · [Discovery JSON](https://soulintime.com/.well-known/soulintime.json)
- [Sitemap](https://soulintime.com/sitemap.xml) (both sealed examples).

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
- No account or key is required to check. A private Book of 10 key is optional only when intentionally creating above the free allowance; original file bytes are not sent.

The MCP tools (hosted and local) check this rule against server metadata only. They do not cryptographically verify the `.ots`; for that, use `ots verify`.

## Rate limits

Creating is limited; reads are not unlimited either.

Creating a receipt (createMoment):
- The free allowance is one fresh hash per network per hour. Optional private Book of 10 credits apply only above that allowance through REST; MCP tools are unchanged.
- A second create inside that hour, or a hash that already has a receipt, returns `429` with the existing slug when that receipt is not private.
- `already_stamped` is permanent and does not clear when the hour resets. Read the existing receipt instead.

Reading (v1Verify):
- Responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). A read we observed carried `X-RateLimit-Limit: 120`. The best-effort per-instance window is 120 checks per IP per 60 seconds; follow the headers.

On 429:
- For a true rate limit, wait until `X-RateLimit-Reset` and don't tight-loop. `already_stamped` instead means read the existing slug.
- Hosted MCP calls share the backend's network egress, so they may share the upstream allowance. There is no per-user allowance.

Checking stays free forever. See the public Book of 10 price above; fulfilment is manual and never changes receipt status.

Need more than the free rate? Email morris@mifalai.com with the hash and the use.

Volume brief (test without creating, free limits, what to email): [volume-brief.md](volume-brief.md)

Issues welcome: https://github.com/SoulinTime/soulintime-client/issues

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

Two sealed examples now exist. Bitcoin whitepaper abstract: moment-ao91b5a0@975352 (non-house); Door: 965906 (permanent test object). Contact morris@mifalai.com. Book of 10 = 21000 sats. HQ posts: [posts.md](posts.md). non-house firsts: 1. Last verified: 2026-11-11.

Permanent test object: Door at 965906. Non-house sealed example: moment-ao91b5a0@975352. Public firsts that are not house examples: 1.

## License

[MIT](LICENSE)
