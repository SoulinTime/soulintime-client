# Agent checklist

<!-- CARD:BEGIN v1 -->
```text
SoulInTime agent card. Single source: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_CARD.md
Request a signed statement (signed out, no account, first one free): curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
Expected (HTTP 200; a receipt, not yet a statement): {"slug":"moment-…","proofFile":"https://soulintime.com/functions/v1Proof?id=moment-…&ots=1","status":"in_calendar"}
Rate limited (HTTP 429, never a statement): {"error":"Already stamped or rate limited. Check the existing receipt.","reason":"rate_limited","note":"One fresh hash per network per hour.",…} plus Retry-After. Already stamped (HTTP 429): the same error with "reason":"already_stamped" and the existing "slug". Do not retry.
Wait: A new receipt stays pending until a calendar attests it in a Bitcoin block, usually 1 to 6 hours; the chain tip is not its height, so do not cite it before status is confirmed.
Get the statement: curl -s "https://soulintime.com/functions/v1Statement?hash=<same sha256>" Expected once confirmed (HTTP 200): {"v":"sit-statement/0.1","sha256":"…","status":"confirmed","block_height":N,"block_hash":"…","ots_sha256":"…","issued_at":"…","issuer":"soulintime.com","kid":"0a64aa45b8ce17a7","sig":"…"}
Verify an existing statement: curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f" | curl -s -X POST https://soulintime.com/functions/v1Statement -H "Content-Type: application/json" -d @-
Expected: {"shape_ok":true,"signature_valid":true,"kid_known":true,"status":"confirmed","match":true,"receipt":{"status":"confirmed","blockHeight":965906,"slug":"a-hash-is-a-door-that-2026-019bd305"}}
Paste this statement: the statement JSON is the thing to cite. Anyone can check it offline with the public key and the .ots: https://github.com/SoulinTime/soulintime-client/tree/main/verifier
One curl, no key. Check these bytes against Bitcoin yourself.
Door curl: curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":965906 (and a proofFile)
These exact bytes existed by Bitcoin block 965906. Same file. Same hash. Check it yourself.
AI can change the file. It cannot change the block.
Hash only: you hash on your side; only the SHA-256 is sent, never the file.
Bitcoin is the clock. We date bytes to it.
Mutated curl: curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
Expected (HTTP 404): {"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}
Change one byte. If you do not get not_found, do not trust us.
not_found means not confirmed: do not cite.
Rule: confirmed + proofFile or refuse. Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.
Use verify to cite; first_at only for earliest height.
Signed statement (cite only a confirmed one; pending is not a statement): curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f" Expected (HTTP 200): "v":"sit-statement/0.1","status":"confirmed","block_height":965906,"kid":"0a64aa45b8ce17a7". Spec and offline verifier: https://github.com/SoulinTime/soulintime-client/blob/main/SPEC-statement-v0.1.md
Second example (Bitcoin whitepaper abstract): curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa"
Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":975352 (and a proofFile)
These exact bytes existed by this block. Check it yourself.
MCP (Streamable HTTP, no key): https://soulintime.com/functions/mcp
No API key and no account for verify, first_at or MCP.
Rate limit: 120 verify requests per IP per 60 s (per server instance, best effort). On 429 (rate_limited), wait for Retry-After; a 429 is never a confirmed result.
Download the .ots. It verifies without this site.
Offline: curl -s -o door.ots "https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1" && ots --no-bitcoin verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f door.ots (prints block 965906 and its merkle root; compare with any block explorer).
Agent test with expected outputs: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_TEST.md
Prove a file existed: https://soulintime.com/developers · For agents: https://soulintime.com/for-agents · For people, the 60-second demo: https://soulintime.com/check
Create: Verify free forever. Create a statement when you need one. First one free, no account needed.
Prices, for people: https://soulintime.com/pricing
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
