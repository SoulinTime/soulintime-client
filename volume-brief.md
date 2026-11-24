# SoulInTime volume brief

<!-- CARD:BEGIN v1 -->
```text
SoulInTime agent card. Single source: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_CARD.md · Full page: https://soulintime.com/integrate
Test without creating (verify, no key, creates nothing; the Door): curl -s "https://soulintime.com/functions/apiV1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
Expected (HTTP 200): {"anchored":true,"receipt_id":"a-hash-is-a-door-that-2026-019bd305",…,"height":965906,…,"status":"anchored",…,"cite":"sha256 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f existed by Bitcoin block 965906. Statement: https://soulintime.com/statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f",…}
CREATES A RECEIPT (signed out, no account; first one free, then one fresh hash per network per hour): curl -s -X POST https://soulintime.com/functions/apiV1Receipts -H "Content-Type: application/json" -d "{\"hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
Expected (HTTP 201; a receipt, not yet a statement): {"receipt_id":"moment-…","status":"in_calendar","height":null,"cite":null,…,"next_action":{"do":"verify_later",…}} Waiting for Bitcoin: confirmation takes hours (usually 1 to 6). Verify the same hash later.
Rule: cite only when "anchored" is true and "cite" is set, and paste that cite line as-is, on one line. Pending, a 409 without cite, a 404 and a 429 are not statements: refuse to cite a block for them.
Cite line format: sha256 <hash> existed by Bitcoin block <N>. Statement: https://soulintime.com/statement?hash=<hash>
409 (hash already has a receipt): receipt_id, and cite only once anchored. 429 (free limit reached): only the error, reset_at, reset_unix and a pricing link; no receipt_id, no statement_url, no cite. Respect Retry-After and X-RateLimit-Reset.
Not found (HTTP 404): "anchored":false,"status":"not_found","cite":null. Change one byte of the hash and you get not_found. If you do not, do not trust us.
What it says: these exact bytes existed by that Bitcoin block. Not who made them, not that they are true, not legal advice.
Hash only: you hash on your side; only the SHA-256 is sent, never the file.
Second example (Bitcoin whitepaper abstract): curl -s "https://soulintime.com/functions/apiV1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa" Expected: "anchored":true, "height":975352
Third example (signing-key fingerprint): curl -s "https://soulintime.com/functions/apiV1Verify?hash=8245c5d39ca6bb836ea1d7cb62dbb379d7de4ab65e49b176ddf02c638a019c25" Expected: "anchored":true, "height":977076
Signed statement (sit-statement/0.1, Ed25519 over JCS, kid 0a64aa45b8ce17a7): curl -s "https://soulintime.com/functions/v1Statement?hash=<sha256>" Spec: https://soulintime.com/sit-statement-0.1.md
Offline (no SoulInTime at all): keep the statement JSON and the .ots; run the verifier https://github.com/SoulinTime/soulintime-client/tree/main/verifier and ots --no-bitcoin verify -d <sha256> file.ots, then compare the block with any block explorer.
MCP (Streamable HTTP, no key): https://soulintime.com/functions/mcp · tools: verify (use it to cite), stamp (creates), first_at (earliest height only)
OpenAPI 3.1: https://soulintime.com/.well-known/openapi-v1.yaml · llms.txt: https://soulintime.com/llms.txt · Health: https://soulintime.com/functions/v1Statement?health=1
Limits: create, one fresh hash per network per hour on the free path; verify, no key and no create, best effort (older v1Verify: 120 requests per IP per 60 s per server instance). Verify is free forever. Create is free for light use and paid at volume: https://soulintime.com/pricing
Older endpoints keep working: POST /functions/createMoment {"sha256Hash":"<hash>"}, GET /functions/v1Verify?hash=<hash>.
Agent test with expected outputs: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_TEST.md
Card updated 2026-11-24 · Verifier https://github.com/SoulinTime/soulintime-client/tree/main/verifier · Firsts https://soulintime.com/firsts.json · Status https://soulintime.com/status
```
<!-- CARD:END -->

These exact bytes existed by Bitcoin block N: SoulInTime dates files to Bitcoin. For companies: Add a Bitcoin height to the file you already produce. The user keeps the file and the receipt. Verify free forever. Create a statement when you need one. First one free, no account needed.

Evaluate with the Door hash before creating. Two sealed examples now exist. Door is the permanent test object; Bitcoin whitepaper abstract is the public example (a text SoulInTime did not write). Last verified (both): 2026-11-17.

<!-- last verified 2026-11-12 -->

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

### Feed and embed

Feed of newly confirmed public receipts (read-only, no key): curl -s "https://soulintime.com/functions/v1FirstAt?list=1&feed=1" returns NDJSON, newest block first, one line per receipt: hash, blockHeight, slug, proofFile, confirmedAt (block header time, UTC, when stored). Confirmed public receipts only: no pending, no private, no unlisted; the Door and whitepaper reference receipts and the seeded examples are left out (other public receipts, including ones the SoulInTime team made, can appear). limit=1..500 (default 50). Rate limit: 30 feed requests per IP per 60 s (per server instance, best effort); 429 is rate_limited. A feed line is not a citation: run verify on the hash before citing.

Embed a confirmed receipt (free, creates nothing, no script, no tracking): HTML <a href="https://soulintime.com/moment/<slug>">Confirmed at block <N> — check</a> or Markdown [Confirmed at block <N> — check](https://soulintime.com/moment/<slug>). Every confirmed receipt page has an Embed this button with both, filled in.

### Second reference: Bitcoin whitepaper abstract (public example)

`moment-ao91b5a0@975352`; SHA-256 `d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa`. Receipt: https://soulintime.com/moment/moment-ao91b5a0
proofFile: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1

<!-- last verified 2026-11-12 -->
```sh
curl -s 'https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa'
```
Expected: status confirmed, blockHeight 975352, proofFile. The Door at 965906 stays unchanged.

**2. Free limits, as the code enforces them today.** Creating (createMoment, and the MCP `stamp` tool that calls it): one fresh hash per network per hour. A hash that already has a receipt answers `429` with `reason: already_stamped`; that is permanent and does not clear when the hour resets, so read the existing receipt instead. Checking (v1Verify, and the MCP `verify` tool): 120 lookups per IP per 60 seconds, best effort per server instance; every reply carries `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). v1FirstAt has no endpoint limit of its own; platform limits may still apply. Hosted MCP calls share the backend's egress, so they may share the upstream allowance. On a rate-limited `429` (not `already_stamped`), wait until `X-RateLimit-Reset` and do not tight-loop. Checking stays free. Monthly and Starter pricing is public below; free checking remains free forever.

Legacy v1Anchor has a separate anonymous cap of 100 over a rolling 24 hours, counted from public, pending, ownerless rows rather than all anchors. This is not the createMoment allowance; no reset available.

**3. Ongoing volume.** Choose Monthly for 100 statements / 30 days, or Starter for 10 statements / 90 days. https://github.com/SoulinTime/soulintime-client/issues is the questions path; never post private payment data.

Expected free limits: one fresh hash per network per hour; v1Verify 120 checks per IP per 60 seconds, best effort per instance.  
Monthly, Yearly and Starter supply additional statements only above the existing free per-network allowance, for the verified payer. Global limits stay unchanged.
Prices are public at https://soulintime.com/pricing.
Issues welcome: https://github.com/SoulinTime/soulintime-client/issues

## Pricing and private book status

Free check stays free forever, subject to existing read limits. No account required to check. Account required to see what you paid for.

Paid statement balances, one-time (buy again to continue) unless you choose Yearly auto-renew ($399/year, cancel any time): Monthly — 100 statements / 30 days, $49 USD; Yearly — 1500 statements / 365 days, $399 USD, best for teams and agents; or Yearly auto-renew — $399 USD per year, 1500 new statements each year, cancel any time; Starter pack — 10 statements / 90 days, $20 USD. Card prices plus applicable tax. Unused statements expire at the end of the period. They do not roll over. Prices and checkout: https://soulintime.com/pricing. Prices effective 12 Nov 2026. Next review: 1 Feb 2027. No account required to check. Account required to see what you paid for. Verified card payment attaches your statements to the email used at Checkout; sign in with Google at https://soulintime.com/account to see statements left, expiry, receipts and a download of all proofs. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.

Prices effective 12 Nov 2026. Next review: 1 Feb 2027.

Payments: self-serve by card at https://soulintime.com/pricing.

After verified card payment, sign in with Google at https://soulintime.com/account to see statements left, expiry, receipts and download all proofs. Checking never needs an account.

Signed-in browsers spend account statements automatically; API callers send `X-SoulInTime-Book: <balance key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt.

## How agents find us

How agents find us: the official MCP Registry (io.github.MorrisMoe/soulintime), mcpservers.org (https://mcpservers.org/servers/soulintime/soulintime-client), Glama (https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime), and llms.txt (https://soulintime.com/llms.txt). For agents: https://soulintime.com/for-agents · For firms: https://soulintime.com/for-firms

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Last verified (both sealed examples): 2026-11-15.

Proofs use OpenTimestamps: https://opentimestamps.org/
