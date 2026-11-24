# Agent checklist

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

1. Call verify or first_at before citing.
2. Cite only status confirmed with proofFile.
3. Otherwise refuse.
4. You may attach the .ots URL.

## The two curls (no API key)

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":965906 (and a proofFile)

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

Expected (HTTP 404): {"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}

Change one byte. If you do not get not_found, do not trust us. not_found means not confirmed: do not cite.

Refusal: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

Use verify to cite; first_at only for earliest height. Agent test: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_TEST.md

## Boundary (precise)

This is the one place, with https://soulintime.com/protocol (law 6), where the boundary is written out in full.
A confirmed receipt proves one thing: these exact bytes existed by that Bitcoin block. It does not prove that the contents are true, who wrote or sent them, where a device was, or any legal conclusion.
A pending receipt has no height and is never cited. A location hash (gps-v1) dates the location bytes, not a presence.
Citation rule: Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

## Reference

Check: https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
API: https://soulintime.com/functions/v1Verify?hash=<sha256>
proofFile: https://soulintime.com/functions/v1Proof?id=<slug>&ots=1
No API key.
Do not retry already_stamped; read the slug.
MCP Registry: https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest
Last updated: 2026-11-12

Permanent test object: Door at block 965906. Last verified: 2026-11-15.

### Second reference: public example, Bitcoin whitepaper abstract

moment-ao91b5a0@975352
SHA-256: d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa
Check: https://soulintime.com/verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa
Receipt: https://soulintime.com/moment/moment-ao91b5a0
proofFile: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1
Last verified: 2026-11-15. People can check it in the browser in 60 seconds: https://soulintime.com/check

## Pricing and private book status

Free check stays free forever, subject to existing read limits. No account required to check. Verify free forever. Create a statement when you need one. First one free, no account needed.

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
