# Request a signed statement with one curl: these exact bytes existed by a Bitcoin block.

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

## Signed statement (request this)

A statement is a signed JSON object: these exact bytes were confirmed at Bitcoin block N. Cite only a confirmed statement. Pending is not a statement.

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected (HTTP 200):

```json
{"v":"sit-statement/0.1","sha256":"019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f","status":"confirmed","block_height":965906,"block_hash":"00000000000000000001b1d2e4220a0d1600a59bd2d3753743fa3654679b5130","ots_sha256":"0661ce7e66b59e8d594b379f33e7512f7e0e7e3f22ec6d8ab0477a5b15400294","issued_at":"2026-11-22T15:43:53Z","issuer":"soulintime.com","kid":"0a64aa45b8ce17a7","sig":"zhvCuFJVGbow3scYxBseprsS_oEBw5cOOXn5VaFYrfoyFudZRrhi75rety4SjDVGCiEeO9jvrJsaTvxrw4FjBw"}
```

Unknown or not confirmed: HTTP 404 and a signed refusal (`"status":"refused"`, `"reason":"not_found"` or `"not_confirmed"`, `"ots_sha256":null`).
Verify it offline: [`verifier/`](verifier/) (one file, Python or JS). Format: [SPEC-statement-v0.1.md](SPEC-statement-v0.1.md). Key: [`keys/`](keys/) (kid `0a64aa45b8ce17a7`).
Public firsts as one file: [JSON](https://soulintime.com/functions/v1FirstAt?list=1&format=json) · [CSV](https://soulintime.com/functions/v1FirstAt?list=1&format=csv).
Confirmed statements as one file: [firsts.json](https://soulintime.com/firsts.json) (newest block first; live: `https://soulintime.com/functions/v1Statement?firsts=1&since=<height>`). Status: https://soulintime.com/status.

## How to cite

Paste the cite line exactly as returned, on one line, unchanged: `sha256 <hash> existed by Bitcoin block <N>. Statement: <url>`. It says only that these exact bytes existed by that block; it does not say who made them or that they are true. Cite only a confirmed statement: pending, rate-limited and refused answers carry `"cite":null` and must not be cited. Anyone can check the statement offline with the public key and the .ots, and it still verifies if we disappear.

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f&format=cite"
```

```
sha256 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f existed by Bitcoin block 965906. Statement: https://soulintime.com/statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
```

Refusal (never cite): [examples/fixtures/refusal-rate-limited.json](examples/fixtures/refusal-rate-limited.json). Share formats, card URL and the firsts filter: [SPEC](SPEC-statement-v0.1.md#how-to-cite). Release assets: [GitHub Action example](examples/github-action/README.md).

## Verify a statement yourself (offline)

```sh
curl -s "https://soulintime.com/functions/v1Statement?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f" > door.statement.json
python3 verifier/verify_statement.py door.statement.json --hash 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
node verifier/verify_statement.mjs door.statement.json --hash 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
```

Last line `RESULT: all checks passed`, exit 0; any changed byte, height or signature prints `RESULT: FAILED`, exit 1. Add `--file yourfile` and `--ots proof.ots` for the full check, then `ots verify -d <sha256> proof.ots` for the block. Test vectors: [verifier/vectors](verifier/vectors/). The verifier makes no network call. How to check the signing key itself: [keys/fingerprint-stamp.md](keys/fingerprint-stamp.md) (dated at block 977076).

## Code and examples

createStatement in [Python](examples/create_statement.py) and [JS](examples/create_statement.mjs), a [git hook](examples/git-hook-post-commit.sh), a [GitHub Action example](examples/github-action/release-statement.yml) (not enabled, not published as an Action) and two sketches: [examples/README.md](examples/README.md). Changes: [CHANGELOG.md](CHANGELOG.md). Problems with a statement: [open an issue](https://github.com/SoulinTime/soulintime-client/issues/new?template=statement-problem.md) (support is issues-only).


Bitcoin is the clock. We date bytes to it. AI can change the file. It cannot change the block.

## Test without creating

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected: `"status":"confirmed","blockHeight":965906`

Change one byte of the abstract or hash and verify returns HTTP 404 `{"error":"not_found"}`: not confirmed, do not cite.

Mutated-hash curl (the whitepaper abstract hash with its last character changed from a to b):

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

Expected (HTTP 404): `{"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}`

Change one byte. If you do not get not_found, do not trust us.

Agents: Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists. Two-curl agent test: [AGENT_TEST.md](AGENT_TEST.md). Pre-cite hook for OpenAI Agents SDK, LangChain and Pydantic AI (each tested against the hosted MCP): [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md). Five-line drop-in snippets: [FRAMEWORK_SNIPPET.md](FRAMEWORK_SNIPPET.md). verify is the primary call and the only one needed to cite; first_at is secondary (earliest height only) and not required. Rate limit: 120 verify requests per IP per 60 s (best effort). On 429, respect Retry-After or X-RateLimit-Reset; do not tight-loop. A 429 body is `{"error":"rate_limited"}`, never a confirmed result. The verify response shape is stable: status, blockHeight, slug and proofFile keep their names and meaning. Offline: download the .ots (proofFile), then run `ots verify -f <original file> <slug>.ots` (OpenTimestamps client; needs your own Bitcoin node, or compare the merkle root from `ots info` with any block explorer).

**People: check a real receipt in 60 seconds, in your browser, no account: https://soulintime.com/check**

Verify free forever. Create a statement when you need one. First one free, no account needed. For companies: Add a Bitcoin height to the file you already produce. The user keeps the file and the receipt.

Two sealed examples now exist. **Public example: Bitcoin whitepaper abstract** (a text SoulInTime did not write), [`moment-ao91b5a0@975352`](https://soulintime.com/moment/moment-ao91b5a0). SHA-256 `d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa`. [Download .ots](https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1). Last verified: 2026-11-15.

The Door below remains the permanent test object at block 965906.

Sealed hash: `019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f`

Live receipt: [https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305](https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305) (block 965906)

Latest sealed example: Bitcoin whitepaper abstract, moment-ao91b5a0 at block 975352 (public example). Door: block 965906 (permanent test object).

Citation rule: Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

Check it on the web: [https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f](https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f)

Hosted MCP: [https://soulintime.com/functions/mcp](https://soulintime.com/functions/mcp). Point any MCP client that supports remote Streamable HTTP servers at this URL. No key is needed. Call `verify` with the sealed hash.

Local MCP package: [https://soulintime.com/functions/mcpDownload](https://soulintime.com/functions/mcpDownload)

Running the reference client creates a receipt. The curl below does not.

The hash is computed on your device; original file bytes stay there.

Download the .ots. It verifies without this site.

We did not invent the calendar. [OpenTimestamps](https://github.com/opentimestamps) did. We are the receipt and the refusal layer on top of it.

The proof is OpenTimestamps: anyone can check a `.ots` with the [OpenTimestamps client](https://github.com/opentimestamps/opentimestamps-client). If soulintime.com is gone tomorrow, a downloaded `.ots` and the original bytes still check against Bitcoin.

<!-- last verified 2026-11-12 -->
```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

Before citing: call verify. Cite only status confirmed with proofFile; otherwise refuse. You may attach the .ots URL.
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

Outside Matches this week: 0. Completed payments: 0. (22 Nov 2026; the Match counter started that day.)

## Pricing and your account

Free check stays free forever, subject to existing read limits. No account required to check. Account required to see what you paid for.

Paid statement balances: Monthly — 100 statements / 30 days, $49 USD, one-time; Yearly — 1500 statements / 365 days, $399 USD, best for teams and agents, one-time or auto-renew (cancel any time in the Stripe billing portal linked from https://soulintime.com/account); Starter pack — 10 statements / 90 days, $20 USD, one-time. Card prices plus applicable tax. Prices and checkout: https://soulintime.com/pricing. Prices effective 12 Nov 2026. Next review: 1 Feb 2027. No account required to check. Account required to see what you paid for. Verified card payment attaches your statements to the email used at Checkout; sign in with Google at https://soulintime.com/account to see statements left, expiry, receipts and a download of all proofs. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Unused statements expire at the end of the period. They do not roll over. Problem seeing your statements? Open a GitHub issue: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.


After payment, sign in with Google at https://soulintime.com/account to see statements left, expiry, receipts and a download of all proofs. Signed-in browsers spend account statements automatically. Browser submissions use the saved key; API callers send `X-SoulInTime-Book: <balance key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt.

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Two public receipts, sealed in Bitcoin. Last verified: 2026-11-15. Example texts to try: [examples/](examples/).

Proofs use OpenTimestamps: https://opentimestamps.org/


## Public destinations

- [Whitepaper discussion](https://github.com/SoulinTime/soulintime-client/discussions/1) — curl + moment link only.
- [Who this is for](https://soulintime.com/who) · [Benefits JSON](https://soulintime.com/benefits.json) · [Payment/unlock status](https://soulintime.com/status)
- [Your account after payment](https://soulintime.com/account) (Sign in with Google)
- [For agents](https://soulintime.com/for-agents) · [For firms](https://soulintime.com/for-firms)
- Listed on: the [official MCP Registry](https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest) (`io.github.MorrisMoe/soulintime`), [mcpservers.org](https://mcpservers.org/servers/soulintime/soulintime-client) and [Glama](https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime).
- How agents find us: MCP Registry, mcpservers.org, Glama, and [llms.txt](https://soulintime.com/llms.txt). Index list with status: [indexes.md](indexes.md).

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
- No account or key is required to check. Paid statements are optional and used only when intentionally creating above the free allowance (signed in at https://soulintime.com/account in a browser, or with a balance key over REST); original file bytes are not sent.

The MCP tools (hosted and local) check this rule against server metadata only. They do not cryptographically verify the `.ots`; for that, use `ots verify`.

## Rate limits

Creating is limited; reads are not unlimited either.

Creating a receipt (createMoment):
- The free allowance is one fresh hash per network per hour. Optional paid statements apply only above that allowance through REST; MCP tools are unchanged.
- A second create inside that hour, or a hash that already has a receipt, returns `429` with the existing slug when that receipt is not private.
- `already_stamped` is permanent and does not clear when the hour resets. Read the existing receipt instead.

Reading (v1Verify):
- Responses carry `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). A read we observed carried `X-RateLimit-Limit: 120`. The best-effort per-instance window is 120 checks per IP per 60 seconds; follow the headers.

On 429:
- For a true rate limit, wait until `X-RateLimit-Reset` and don't tight-loop. `already_stamped` instead means read the existing slug.
- Hosted MCP calls share the backend's network egress, so they may share the upstream allowance. There is no per-user allowance.

Checking stays free forever. See Monthly, Yearly and Starter pricing above. Verified card payment unlocks only the purchased statement balance and never changes receipt status.

Need more than the free rate? Monthly, Yearly or Starter at https://soulintime.com/pricing. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish a balance key or payment reference.

Volume brief (test without creating, free limits, what to email): [volume-brief.md](volume-brief.md)

Issues welcome: https://github.com/SoulinTime/soulintime-client/issues

## Hosted vs local MCP

Hosted (`/functions/mcp`):
- Stateless Streamable HTTP over POST.
- Tools `verify(hash)` and `first_at(hash, height?)` are read-only.
- `stamp(hash)` creates a receipt and is never an evaluation call.

Client config (Claude, Cursor, VS Code and other MCP clients that take a remote URL; no key):

```json
{"mcpServers": {"soulintime": {"url": "https://soulintime.com/functions/mcp"}}}
```

Local (`mcp-local/`):
- This is the source of the same 0.1.0 package served by the download link. It speaks stdio.
- See `mcp-local/README.md` for setup. That README predates the hosted endpoint.
- The hosted MCP also checks that `proofFile` is the canonical `v1Proof?id=<slug>&ots=1` URL. The local one does not.

Tests:
- `test_http.py` mocks all HTTP.
- `test_protocol.py` mocks every statement. Its last case is one live read-only `verify` GET of the sealed hash, which runs when you run the file. It never makes a live POST.

---

**CREATES A RECEIPT.**

## Reference client

`reference-client/soulintime_client.py` is the same code published in [llms.txt](https://soulintime.com/llms.txt), standard library only. Running it **creates a receipt**:
- It POSTs the hash to createMoment.
- It polls v1Verify and saves the `.ots`.
- An accepted statement is a new registry entry, unlisted by default.

To test without side effects, use the curl at the top instead.

## Feed (newly confirmed public receipts)

```
curl -s "https://soulintime.com/functions/v1FirstAt?list=1&feed=1"
```

NDJSON, newest block first, one line per receipt: `hash`, `blockHeight`, `slug`, `proofFile`, `confirmedAt` (block header time, UTC, when stored). Confirmed public receipts only: no pending, private or unlisted; the Door and whitepaper reference receipts and the seeded examples are left out. `limit=1..500` (default 50). 30 feed requests per IP per 60 s (per server instance, best effort); 429 is `{"error":"rate_limited"}`. A feed line is not a citation: run verify on the hash before citing.

## Embed a confirmed receipt

Free, creates nothing, no script, no tracking. Every confirmed receipt page has an **Embed this** button with both forms filled in:

```html
<a href="https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305">Confirmed at block 965906 — check</a>
```

```markdown
[Confirmed at block 965906 — check](https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305)
```

## Specs (not built)

- [Telegram bot](specs/telegram-bot.md)
- [Date this output](specs/date-this-output.md)
- [Browser extension](specs/browser-extension.md)

## Host dependence

Registry queries (v1Verify, v1FirstAt, Firsts) depend on soulintime.com. A downloaded `.ots` stays checkable with any OpenTimestamps client without it.

API contract: [llms.txt](https://soulintime.com/llms.txt) and [openapi.yaml](https://soulintime.com/.well-known/openapi.yaml).

## Status

Two sealed examples now exist. Bitcoin whitepaper abstract: moment-ao91b5a0@975352 (public example); Door: 965906 (permanent test object). Questions: https://github.com/SoulinTime/soulintime-client/issues. Monthly is the primary offer; Starter remains available at https://soulintime.com/pricing. HQ posts: [posts.md](posts.md). Last verified: 2026-11-17.

Permanent test object: Door at 965906. Public sealed example: moment-ao91b5a0@975352. Check it in 60 seconds: https://soulintime.com/check

## License

[MIT](LICENSE)
