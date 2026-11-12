# Test without creating

Two sealed examples now exist. **Non-house example: Bitcoin whitepaper abstract**, [`moment-ao91b5a0@975352`](https://soulintime.com/moment/moment-ao91b5a0). SHA-256 `d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa`. [Download .ots](https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1). Last verified: 2026-11-12.

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

<!-- last verified 2026-11-12 -->
```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

Before citing: call verify or first_at. Cite only status confirmed with proofFile; otherwise refuse. You may attach the .ots URL.
Pending receipts are never cited.
Agent checklist: https://soulintime.com/agent-checklist.md

Expected: `"status":"confirmed"`, `"blockHeight":965906`, `"slug":"a-hash-is-a-door-that-2026-019bd305"`, and a `proofFile`.

<!-- last verified 2026-11-12 -->
Second example (read only):
```sh
curl -s 'https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa'
```
Expected: status confirmed, blockHeight 975352 and proofFile.

/yours supports signed-out device receipts; account-owned receipts require sign-in.

## Pricing and your account

Free check stays free forever, subject to existing read limits. No account required to check. Account recommended after payment to see your stamps.

Paid stamp balances, each a one-time payment with no auto-renew (buy again to continue): Monthly — 100 stamps / 30 days, $49 USD; Yearly — 1500 stamps / 365 days, $399 USD, best for teams and agents; Starter pack — 10 stamps / 90 days, $20 USD. Card prices plus applicable tax. Lightning: coming soon. Prices and checkout: https://soulintime.com/pricing. Prices effective 12 Nov 2026. Next review: 1 Feb 2027. No account required to check. Account recommended after payment to see your stamps. Verified card payment attaches your stamps to the email used at Checkout; sign in with Google at https://soulintime.com/account to see stamps left, expiry, receipts and a download of all proofs. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.


After payment, sign in with Google at https://soulintime.com/account to see stamps left, expiry, receipts and a download of all proofs. Signed-in browsers spend account stamps automatically. Browser submissions use the saved key; API callers send `X-SoulInTime-Book: <balance key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt.

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Two public receipts, sealed in Bitcoin. Last verified: 2026-11-12.

Proofs use OpenTimestamps: https://opentimestamps.org/


## Public destinations

- [Whitepaper discussion](https://github.com/SoulinTime/soulintime-client/discussions/1) — curl + moment link only.
- [Who this is for](https://soulintime.com/who) · [Benefits JSON](https://soulintime.com/benefits.json) · [Payment/unlock status](https://soulintime.com/status)
- [Your account after payment](https://soulintime.com/account) (Sign in with Google)
- [For agents](https://soulintime.com/for-agents) · [For firms](https://soulintime.com/for-firms)
- Listed on: the [official MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest) (`io.github.MorrisMoe/soulintime`), [mcpservers.org](https://mcpservers.org/servers/soulintime/soulintime-client) and [Glama](https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime).
- How agents find us: MCP Registry, mcpservers.org, Glama, and [llms.txt](https://soulintime.com/llms.txt).

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
- No account or key is required to check. Paid stamps are optional and used only when intentionally creating above the free allowance (signed in at https://soulintime.com/account in a browser, or with a balance key over REST); original file bytes are not sent.

The MCP tools (hosted and local) check this rule against server metadata only. They do not cryptographically verify the `.ots`; for that, use `ots verify`.

## Rate limits

Creating is limited; reads are not unlimited either.

Creating a receipt (createMoment):
- The free allowance is one fresh hash per network per hour. Optional paid stamps apply only above that allowance through REST; MCP tools are unchanged.
- A second create inside that hour, or a hash that already has a receipt, returns `429` with the existing slug when that receipt is not private.
- `already_stamped` is permanent and does not clear when the hour resets. Read the existing receipt instead.

Reading (v1Verify):
- Responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). A read we observed carried `X-RateLimit-Limit: 120`. The best-effort per-instance window is 120 checks per IP per 60 seconds; follow the headers.

On 429:
- For a true rate limit, wait until `X-RateLimit-Reset` and don't tight-loop. `already_stamped` instead means read the existing slug.
- Hosted MCP calls share the backend's network egress, so they may share the upstream allowance. There is no per-user allowance.

Checking stays free forever. See Monthly, Yearly and Starter pricing above. Verified card payment unlocks only the purchased stamp balance and never changes receipt status. Lightning: coming soon.

Need more than the free rate? Monthly, Yearly or Starter at https://soulintime.com/pricing. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish a balance key or payment reference.

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

Two sealed examples now exist. Bitcoin whitepaper abstract: moment-ao91b5a0@975352 (non-house); Door: 965906 (permanent test object). Questions: https://github.com/SoulinTime/soulintime-client/issues. Monthly is the primary offer; Starter remains available at https://soulintime.com/pricing. HQ posts: [posts.md](posts.md). non-house firsts: 1. Last verified: 2026-11-12.

Permanent test object: Door at 965906. Non-house sealed example: moment-ao91b5a0@975352. Public firsts that are not house examples: 1.

## License

[MIT](LICENSE)
