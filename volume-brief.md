# SoulInTime volume brief

Evaluate with the Door hash before creating. Two sealed examples now exist. Door is the permanent test object; Bitcoin whitepaper abstract is the non-house example. non-house firsts: 1. Last verified (both): 2026-11-11.

<!-- last verified 2026-11-11 -->

```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

**1. Test without creating.** Check the sealed example first; nothing below creates a receipt. Sealed hash `019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f`, receipt https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305 (block 965906). Over plain HTTP: `curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'` should return `"status":"confirmed"`, `"blockHeight":965906` and a `proofFile`. Over the hosted MCP endpoint (https://soulintime.com/functions/mcp, stateless Streamable HTTP, no key), call the read-only `verify` tool: `curl -s -X POST https://soulintime.com/functions/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"verify","arguments":{"hash":"019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"}}}'`. The proof file is at https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1 and verifies without this host: `ots verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f a-hash-is-a-door-that-2026-019bd305.ots`. Do not call `stamp` or POST createMoment to test; both create a receipt.

Confirmed Door verify response (exact observed keys and example values; optional fields vary by receipt). Types: sha256Hash: string, hash: string, status: string, blockHeight: integer, proofFile: string, submitted: boolean, slug: string, url: string, firsts_url: string, proof: object, checkYourself: array of strings.

```json
{
  "sha256Hash": "019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f",
  "hash": "019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f",
  "status": "confirmed",
  "blockHeight": 965906,
  "proofFile": "https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1",
  "submitted": true,
  "slug": "a-hash-is-a-door-that-2026-019bd305",
  "url": "https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305",
  "firsts_url": "https://soulintime.com/functions/v1FirstAt?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f",
  "proof": {
    "mempoolUrl": "https://mempool.space/block-height/965906",
    "verifyUrl": "https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
  },
  "checkYourself": [
    "curl -L -o proof.ots \"https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1\"",
    "pip install opentimestamps-client || pipx install opentimestamps-client",
    "ots verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f proof.ots",
    "Without a node, run ots info proof.ots and compare the merkle root it prints for block 965906 with the same block on any block explorer."
  ]
}
```

### Second reference: Bitcoin whitepaper abstract (non-house)

`moment-ao91b5a0@975352`; SHA-256 `d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa`. Receipt: https://soulintime.com/moment/moment-ao91b5a0
proofFile: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1

<!-- last verified 2026-11-11 -->
```sh
curl -s 'https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa'
```
Expected: status confirmed, blockHeight 975352, proofFile. The Door at 965906 stays unchanged.

**2. Free limits, as the code enforces them today.** Creating (createMoment, and the MCP `stamp` tool that calls it): one fresh hash per network per hour. A hash that already has a receipt answers `429` with `reason: already_stamped`; that is permanent and does not clear when the hour resets, so read the existing receipt instead. Checking (v1Verify, and the MCP `verify` tool): 120 lookups per IP per 60 seconds, best effort per server instance; every reply carries `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). v1FirstAt has no endpoint limit of its own; platform limits may still apply. Hosted MCP calls share the backend's egress, so they may share the upstream allowance. On a rate-limited `429` (not `already_stamped`), wait until `X-RateLimit-Reset` and do not tight-loop. Checking stays free. Book of 10 pricing is public below; free checking remains free forever.

Legacy v1Anchor has a separate anonymous cap of 100 over a rolling 24 hours, counted from public, pending, ownerless rows rather than all anchors. This is not the createMoment allowance; no reset available.

**3. What to email.** If you need more than this, email morris@mifalai.com with: one hash you have already stamped or checked (the SHA-256, never the file), what you are dating and why, and how many fresh hashes per hour you expect (typical and peak). For a Lightning Book of 10, send the payment reference for manual settlement verification; card Checkout unlocks a private book automatically after verified payment.

Expected free limits: one fresh hash per network per hour; v1Verify 120 checks per IP per 60 seconds, best effort per instance.  
Book of 10 covers ten additional submissions for the verified payer only, above the normal free rate. A signed Stripe webhook unlocks paid card books; global limits stay unchanged.
Price and Lightning address are public at https://soulintime.com/pricing.
Issues welcome: https://github.com/SoulinTime/soulintime-client/issues

## Pricing and private book status

Free check stays free forever, subject to existing read limits. No account required to check or buy.

Book of 10 = **21000 sats** to **muddleddesign796@walletofsatoshi.com** (Lightning, Wallet of Satoshi), or **$20 USD by card**, plus sales tax where applicable: https://buy.stripe.com/7sY6oH9FXcnH1Gu7U08IU00 (one-time Stripe Checkout). Price: https://soulintime.com/pricing

Prices fixed through 31 Dec 2026. Next review: 1 Jan 2027. Reviewed quarterly.

Payments: self-serve. Unlock: automatic for card, manual for Lightning.

Successful verified card Checkout automatically unlocks a private Book of 10 at https://soulintime.com/unlocked. Lightning stays manual after verified settlement; email morris@mifalai.com the payment reference, never original files. Per-invoice provider later. No automatic email is sent. Private book credits apply only above the normal free per-network allowance; no global limit changes.

Keep the returned private book key securely. Browser submissions use the saved key; API callers send `X-SoulInTime-Book: <private book key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt. See https://soulintime.com/paid-ready.md for exact counters and the signed fulfillment path.

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Non-house firsts: 1. Last verified (both sealed examples): 2026-11-11.

Proofs use OpenTimestamps: https://opentimestamps.org/
