# Agent test — two curls, no key: these bytes, this block, check yourself

<!-- CARD:BEGIN v1 -->
```text
SoulInTime agent card. Single source: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_CARD.md
Hash only: you hash on your side; only the SHA-256 is sent, never the file. A confirmed receipt shows these exact bytes existed by that Bitcoin block. It does not prove truth or authorship.
Door curl: curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":965906 (and a proofFile)
Mutated curl: curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
Expected (HTTP 404): {"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}
Change one byte. If you do not get not_found, do not trust us.
Rule: confirmed + proofFile or refuse. Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.
Wait: A new stamp stays pending until a calendar attests it in a Bitcoin block, which takes minutes to hours; the chain tip is not its height, so do not cite it before status is confirmed.
Second example (Bitcoin whitepaper abstract): curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa"
Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":975352 (and a proofFile)
MCP (Streamable HTTP, no key): https://soulintime.com/functions/mcp
Rate limit: 120 verify requests per IP per 60 s. On 429, wait for Retry-After; a 429 is never a confirmed result.
Offline: curl -s -o door.ots "https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1" && ots --no-bitcoin verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f door.ots (prints block 965906 and its merkle root; compare with any block explorer)
Prove a file existed: https://soulintime.com/developers · For agents: https://soulintime.com/for-agents · For people, the 60-second demo: https://soulintime.com/check
Prices, for people: https://soulintime.com/pricing
```
<!-- CARD:END -->

Two read-only curls. No API key, no account. Neither creates anything.

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

## Notes

verify is the primary call and the only one needed to cite; first_at is secondary (earliest height only) and not required.

Rate limit: 120 verify requests per IP per 60 s (best effort). On 429, respect Retry-After or X-RateLimit-Reset; do not tight-loop. A 429 body is `{"error":"rate_limited"}`, never a confirmed result.

The verify response shape is stable: status, blockHeight, slug and proofFile keep their names and meaning.

Offline: download the .ots (proofFile), then run `ots verify -f <original file> <slug>.ots` (OpenTimestamps client; needs your own Bitcoin node, or compare the merkle root from `ots info` with any block explorer).

## Rule

Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

Pass = both cite (`a-hash-is-a-door-that-2026-019bd305@965906`, `moment-ao91b5a0@975352`), and any pending or unknown hash is refused.
The claim is only: these exact bytes existed by this Bitcoin block. The .ots verifies without this site.

Wiring this into an agent framework (OpenAI Agents SDK, LangChain, Pydantic AI) as a pre-cite hook: [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md).
