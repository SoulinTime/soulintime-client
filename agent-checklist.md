# Agent checklist

1. Call verify or first_at before citing.
2. Cite only status confirmed with proofFile.
3. Otherwise refuse.
4. You may attach the .ots URL.

## Reference

Check: https://soulintime.com/verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f
API: https://soulintime.com/functions/v1Verify?hash=<sha256>
proofFile: https://soulintime.com/functions/v1Proof?id=<slug>&ots=1
No API key.
Do not retry already_stamped; read the slug.
MCP Registry: https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest
Last updated: 2026-11-12

Permanent test object: Door at block 965906. Last verified: 2026-11-12.

### Second reference: non-house Bitcoin whitepaper abstract

moment-ao91b5a0@975352
SHA-256: d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa
Check: https://soulintime.com/verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa
Receipt: https://soulintime.com/moment/moment-ao91b5a0
proofFile: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1
Last verified: 2026-11-12. non-house firsts: 1.

## Pricing and private book status

Free check stays free forever, subject to existing read limits. No account required to check. Account recommended after payment to see your stamps.

Paid stamp balances, each a one-time payment with no auto-renew (buy again to continue): Monthly — 100 stamps / 30 days, $49 USD; Yearly — 1500 stamps / 365 days, $399 USD, best for teams and agents; Starter pack — 10 stamps / 90 days, $20 USD. Card prices plus applicable tax. Lightning: coming soon. Prices and checkout: https://soulintime.com/pricing. Prices effective 12 Nov 2026. Next review: 1 Feb 2027. No account required to check. Account recommended after payment to see your stamps. Verified card payment attaches your stamps to the email used at Checkout; sign in with Google at https://soulintime.com/account to see stamps left, expiry, receipts and a download of all proofs. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.

Prices effective 12 Nov 2026. Next review: 1 Feb 2027.

Payments: self-serve by card at https://soulintime.com/pricing. Lightning: coming soon.

After verified card payment, sign in with Google at https://soulintime.com/account to see stamps left, expiry, receipts and download all proofs. Checking never needs an account.

Signed-in browsers spend account stamps automatically; API callers send `X-SoulInTime-Book: <balance key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt.

## How agents find us

How agents find us: the official MCP Registry (io.github.MorrisMoe/soulintime), mcpservers.org (https://mcpservers.org/servers/soulintime/soulintime-client), Glama (https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime), and llms.txt (https://soulintime.com/llms.txt). For agents: https://soulintime.com/for-agents · For firms: https://soulintime.com/for-firms

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Non-house firsts: 1. Last verified (both sealed examples): 2026-11-12.

Proofs use OpenTimestamps: https://opentimestamps.org/
