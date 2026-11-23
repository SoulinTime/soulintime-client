# Agent test — two curls, no key: these bytes, this block, check yourself

<!-- CARD:BEGIN v1 -->
```text
SoulInTime agent card. Single source: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_CARD.md
Request a signed statement (signed out, no account, first one free): curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
Cite line (once confirmed; one line, paste it as-is, do not wrap): sha256 <hash> existed by Bitcoin block <N>. Statement: https://soulintime.com/statement?hash=<hash>  Get it: curl -s "https://soulintime.com/functions/v1Statement?hash=<hash>&format=cite"
Cite example (Door): sha256 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f existed by Bitcoin block 965906. Statement: https://soulintime.com/statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
Expected (HTTP 200; a receipt, not yet a statement): {"slug":"moment-…","proofFile":"https://soulintime.com/functions/v1Proof?id=moment-…&ots=1","status":"in_calendar"}
Refused (HTTP 429, never a statement): {"error":"Already stamped or rate limited. Check the existing receipt.","reason":"rate_limited","statement":null,"cite":null,"do_not_cite":"No statement exists for this request. Do not cite a block for this hash.",…} plus Retry-After. Already stamped (HTTP 429): "reason":"already_stamped" and the existing "slug"; only when that hash is already confirmed does it also carry its "statement" and "cite". Do not retry.
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
Card updated 2026-11-23 · Spec https://github.com/SoulinTime/soulintime-client/blob/main/SPEC-statement-v0.1.md · Verifier https://github.com/SoulinTime/soulintime-client/tree/main/verifier · Firsts https://soulintime.com/firsts.json · Status https://soulintime.com/status
```
<!-- CARD:END -->

Two read-only curls. No API key, no account. Neither creates anything.

## 0. Request a statement, then check one (one block)

```sh
# request (signed out; only the hash leaves your machine)
curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
# check an existing statement (the Door): fetch it and paste it back
curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f" | curl -s -X POST https://soulintime.com/functions/v1Statement -H "Content-Type: application/json" -d @-
```

Exact answers to the request (a receipt or a refusal; none of them is a statement):

```text
HTTP 200  {"slug":"moment-…","proofFile":"https://…","status":"in_calendar"}                       receipt, pending
HTTP 200  {"slug":"moment-…","proofFile":null,"status":"in_calendar","calendar_submit":"failed","statement":null,"note":"…"}   calendar did not answer; re-post the same hash after the hour
HTTP 429  {"error":"…","reason":"rate_limited","statement":null,…}                                  one fresh hash per network per hour is free
HTTP 429  {"error":"…","reason":"already_stamped","statement":null,…}                               this hash already has a receipt; fetch its statement instead
```

Headers on every answer: `X-SoulInTime-Request-Id` (quote it in an issue) and `X-Statement-Spec: sit-statement/0.1`.
Once Bitcoin confirms (usually 1 to 6 hours), `GET /functions/v1Statement?hash=<sha256>` returns the statement; paste this statement as-is when you cite it.

A refusal (signed, HTTP 404; never cite a block from it):

```json
{"v":"sit-statement/0.1","sha256":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab","status":"refused","reason":"not_found","block_height":977116,"block_hash":"000000000000000000006d6dfbea8ca8be4156fe5792925ab270db9637c89233","ots_sha256":null,"issued_at":"2026-11-22T23:05:11Z","issuer":"soulintime.com","kid":"0a64aa45b8ce17a7","sig":"C-5bDultziWpVA5bP1liXWnjTJ5XjO93xtwXFoDGPwYwHeFQguMhm7UesqOoYO-aHhwYD1Y-H8DR11Mem49MBA"}
```

### Poll confirmed statements

```sh
curl -s https://soulintime.com/firsts.json                                    # snapshot, newest block first, "latest" on top
curl -s "https://soulintime.com/functions/v1Statement?firsts=1&since=977000"  # live, only rows at or above that block height
```

Poll at most every 10 minutes (the live list is cached 5 minutes). Size limit: 500 rows per answer.

### Check yourself (no SoulInTime at all)

```sh
python3 verifier/verify_statement.py door.statement.json --hash 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f   # RESULT: all checks passed
```

## Two-curl contract

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected (HTTP 200): `"status":"confirmed","blockHeight":965906` (and a proofFile)

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

Expected (HTTP 404): `{"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}`

Change one byte. If you do not get not_found, do not trust us.

Drop-in snippets for OpenAI Agents SDK, LangChain and Pydantic AI: [FRAMEWORK_SNIPPET.md](FRAMEWORK_SNIPPET.md). Works with any HTTP or MCP agent.

## 1. Door (permanent test object)

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected: `"status":"confirmed","blockHeight":965906` — plus `"slug":"a-hash-is-a-door-that-2026-019bd305"` and a `proofFile`.
.ots: https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1

## 2. Bitcoin whitepaper abstract

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa"
```

Expect: `"status":"confirmed"`, `"blockHeight":975352`, `"slug":"moment-ao91b5a0"`, and a `proofFile`.
.ots: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1

## 3. Optional: one-byte mutation (expect refusal)

Change one byte of the abstract or hash and verify returns HTTP 404 `{"error":"not_found"}`: not confirmed, do not cite.

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

Returns (HTTP 404): `{"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}` — no `status`, no `blockHeight`, no `proofFile`, so the rule below refuses. (Last hex digit of the whitepaper hash changed from `a` to `b`.)

## 4. Signed statement (Door) and a signed refusal

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected (HTTP 200), exactly:

```json
{"v":"sit-statement/0.1","sha256":"019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f","status":"confirmed","block_height":965906,"block_hash":"00000000000000000001b1d2e4220a0d1600a59bd2d3753743fa3654679b5130","ots_sha256":"0661ce7e66b59e8d594b379f33e7512f7e0e7e3f22ec6d8ab0477a5b15400294","issued_at":"2026-11-22T15:43:53Z","issuer":"soulintime.com","kid":"0a64aa45b8ce17a7","sig":"zhvCuFJVGbow3scYxBseprsS_oEBw5cOOXn5VaFYrfoyFudZRrhi75rety4SjDVGCiEeO9jvrJsaTvxrw4FjBw"}
```

Check it offline: `python3 verifier/verify_statement.py door.statement.json --hash 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f` → last line `RESULT: all checks passed`.

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

Expected (HTTP 404): a signed refusal, `"status":"refused"`, `"reason":"not_found"`, `"ots_sha256":null`, `block_height` = the chain tip when asked, `"kid":"0a64aa45b8ce17a7"`. Refuse to cite. Pending is not a statement.

## 5. Cite line (echo it untruncated)

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f&format=cite"
```

Expected (HTTP 200, `text/plain`, one line of 218 ASCII characters, then a newline):

```
sha256 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f existed by Bitcoin block 965906. Statement: https://soulintime.com/statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
```

Pass: your answer contains that exact line, unwrapped and unshortened. Paste the cite line exactly as returned, on one line, unchanged: `sha256 <hash> existed by Bitcoin block <N>. Statement: <url>`. It says only that these exact bytes existed by that block; it does not say who made them or that they are true. Cite only a confirmed statement: pending, rate-limited and refused answers carry `"cite":null` and must not be cited. Anyone can check the statement offline with the public key and the .ots, and it still verifies if we disappear.

Refusal fixture (HTTP 429 from `createMoment`; `"cite":null`, never cite): [examples/fixtures/refusal-rate-limited.json](examples/fixtures/refusal-rate-limited.json). A 429 `already_stamped` for a confirmed hash instead carries that hash's existing `statement` and `cite`.

## 6. Firsts since a block

```sh
curl -s "https://soulintime.com/functions/v1Statement?firsts=1&since=977000"
```

Expected: only confirmed statements with `block_height >= 977000` (today the signing-key fingerprint, block 977076), each row with its `cite`. Static file: `jq '.firsts|map(select(.block_height>=977000))' firsts.json`.

## 7. API v1 (JSON; same free rule)

```sh
# verify, read-only, no key (the Door)
curl -s "https://soulintime.com/functions/apiV1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
# create (signed out; only the hash leaves your machine; first one free, then one fresh hash per network per hour)
curl -s -X POST https://soulintime.com/functions/apiV1Receipts -H "Content-Type: application/json" -d "{\"hash\":\"$(sha256sum yourfile | cut -c1-64)\",\"source\":\"yourapp\"}"
```

Expected verify (HTTP 200): `"anchored":true`, `"height":965906`, `"status":"anchored"` and the cite line in `"cite"`. Change one character of the hash: HTTP 404, `"anchored":false`, `"status":"not_found"`, `"cite":null`.
Expected create (HTTP 201): `"status":"in_calendar"` (or `"pending"`), `"height":null`, `"cite":null`, `next_action.do` = `verify_later`. Same hash again: HTTP 409 with the `receipt_id`. Over the free rate: HTTP 429 with only the error and `reset_at` (no `receipt_id`, no `statement_url`, no `cite`: nothing was created). Never cite a 201, 409 without `cite`, or 429.

## Notes

verify is the primary call and the only one needed to cite; first_at is secondary (earliest height only) and not required.

Rate limit: 120 verify requests per IP per 60 s (best effort). On 429, respect Retry-After or X-RateLimit-Reset; do not tight-loop. A 429 body is `{"error":"rate_limited"}`, never a confirmed result.

The verify response shape is stable: status, blockHeight, slug and proofFile keep their names and meaning.

Offline: download the .ots (proofFile), then run `ots verify -f <original file> <slug>.ots` (OpenTimestamps client; needs your own Bitcoin node, or compare the merkle root from `ots info` with any block explorer).

Feed (optional, read-only): `curl -s "https://soulintime.com/functions/v1FirstAt?list=1&feed=1"` lists newly confirmed public receipts as NDJSON (hash, blockHeight, slug, proofFile, confirmedAt). A feed line is not a citation: run verify on the hash first.

## Rule

Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

Pass = both cite (`a-hash-is-a-door-that-2026-019bd305@965906`, `moment-ao91b5a0@975352`), and any pending or unknown hash is refused.
The claim is only: these exact bytes existed by this Bitcoin block. The .ots verifies without this site.

Wiring this into an agent framework (OpenAI Agents SDK, LangChain, Pydantic AI) as a pre-cite hook: [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md).
