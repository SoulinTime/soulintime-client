# Agent card

This is the single source for the SoulInTime agent contract. README, AGENT_TEST.md, every llms.txt copy, agents.json (`agent_card.lines`), the OpenAPI `v1Verify` description, the MCP `verify` description, the top of https://soulintime.com/developers and the top of https://soulintime.com/for-agents copy the block between the markers. Drift from this block is a bug; a daily check (`card_sync`) compares every surface with it and restores it. No prices live here.

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

Block numbers are the verified blocks for these two permanent receipts; the curls are the live check. Receipts: [RECEIPTS.md](RECEIPTS.md).
