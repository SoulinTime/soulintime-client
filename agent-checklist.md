# Agent checklist

<!-- CARD:BEGIN v1 -->
```text
SoulInTime agent card. Single source: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_CARD.md
One curl, no key. Check these bytes against Bitcoin yourself.
Door curl: curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":965906 (and a proofFile)
These exact bytes existed by Bitcoin block 965906. Same file. Same hash. Check it yourself.
AI can change the file. It cannot change the block.
Hash only: you hash on your side; only the SHA-256 is sent, never the file. Bitcoin is the clock: a confirmed receipt shows these exact bytes existed by that Bitcoin block.
Mutated curl: curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
Expected (HTTP 404): {"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}
Change one byte. If you do not get not_found, do not trust us.
not_found means not confirmed: do not cite.
Rule: confirmed + proofFile or refuse. Cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.
Use verify to cite; first_at only for earliest height.
Wait: A new stamp stays pending until a calendar attests it in a Bitcoin block, which takes minutes to hours; the chain tip is not its height, so do not cite it before status is confirmed.
Second example (Bitcoin whitepaper abstract): curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa"
Expected (HTTP 200, verified block): "status":"confirmed","blockHeight":975352 (and a proofFile)
MCP (Streamable HTTP, no key): https://soulintime.com/functions/mcp
No API key and no account for verify, first_at or MCP.
Rate limit: 120 verify requests per IP per 60 s (per server instance, best effort). On 429 (rate_limited), wait for Retry-After; a 429 is never a confirmed result.
Offline: curl -s -o door.ots "https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1" && ots --no-bitcoin verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f door.ots (prints block 965906 and its merkle root; compare with any block explorer). Does not need this host.
Agent test with expected outputs: https://github.com/SoulinTime/soulintime-client/blob/main/AGENT_TEST.md
Prove a file existed: https://soulintime.com/developers · For agents: https://soulintime.com/for-agents · For people, the 60-second demo: https://soulintime.com/check
Create: Verify free forever. Create a receipt when you need one. First one free after sign-in.
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

Free check stays free forever, subject to existing read limits. No account required to check. Verify free forever. Create a receipt when you need one. First one free after sign-in.

Paid stamp balances, one-time (buy again to continue) unless you choose Yearly auto-renew ($399/year, cancel any time): Monthly — 100 stamps / 30 days, $49 USD; Yearly — 1500 stamps / 365 days, $399 USD, best for teams and agents; or Yearly auto-renew — $399 USD per year, 1500 new stamps each year, cancel any time; Starter pack — 10 stamps / 90 days, $20 USD. Card prices plus applicable tax. Unused stamps expire at the end of the period. They do not roll over. Lightning: coming soon. Prices and checkout: https://soulintime.com/pricing. Prices effective 12 Nov 2026. Next review: 1 Feb 2027. No account required to check. Account required to see what you paid for. Verified card payment attaches your stamps to the email used at Checkout; sign in with Google at https://soulintime.com/account to see stamps left, expiry, receipts and a download of all proofs. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.

Prices effective 12 Nov 2026. Next review: 1 Feb 2027.

Payments: self-serve by card at https://soulintime.com/pricing. Lightning: coming soon.

After verified card payment, sign in with Google at https://soulintime.com/account to see stamps left, expiry, receipts and download all proofs. Checking never needs an account.

Signed-in browsers spend account stamps automatically; API callers send `X-SoulInTime-Book: <balance key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt.

## How agents find us

How agents find us: the official MCP Registry (io.github.MorrisMoe/soulintime), mcpservers.org (https://mcpservers.org/servers/soulintime/soulintime-client), Glama (https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime), and llms.txt (https://soulintime.com/llms.txt). For agents: https://soulintime.com/for-agents · For firms: https://soulintime.com/for-firms

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Last verified (both sealed examples): 2026-11-15.

Proofs use OpenTimestamps: https://opentimestamps.org/
