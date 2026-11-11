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
Last updated: 2026-11-11

Permanent test object: Door at block 965906. Last verified: 2026-11-11.

### Second reference: non-house Bitcoin whitepaper abstract

moment-ao91b5a0@975352
SHA-256: d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa
Check: https://soulintime.com/verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa
Receipt: https://soulintime.com/moment/moment-ao91b5a0
proofFile: https://soulintime.com/functions/v1Proof?id=moment-ao91b5a0&ots=1
Last verified: 2026-11-11. non-house firsts: 1.

## Pricing and private book status

Free check stays free forever, subject to existing read limits. No account required to check or buy.

Recommended: Monthly — 100 stamps / 30 days, $99 USD plus applicable tax by card: https://buy.stripe.com/eVqcN55pH73n2Kyfms8IU01. One payment, 30 days. No auto-renew. Buy again to continue. Lightning reference price: 168,000 sats; Lightning checkout is paused, do not pay. Starter pack — 10 stamps / 90 days: $20 USD plus applicable tax by card (https://buy.stripe.com/7sY6oH9FXcnH1Gu7U08IU00); Lightning reference price 21,000 sats. https://soulintime.com/pricing. Next review: 1 Jan 2027. No account required to check or buy. Verified card payment unlocks your private balance at https://soulintime.com/unlocked. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.

Prices fixed through 31 Dec 2026. Next review: 1 Jan 2027. Reviewed quarterly.

Payments: self-serve by card. Lightning checkout is paused.

Verified card Checkout unlocks the purchased private stamp balance on /unlocked. No account required. Keep the private key secure.

Keep the returned private book key securely. Browser submissions use the saved key; API callers send `X-SoulInTime-Book: <private book key>` when intentionally creating. The free path runs first. Only a `rate_limited` refusal can reserve a paid credit; duplicate, validation and proof/citation rules are unchanged. A known pre-write failure releases the reservation; an uncertain write stays reserved for reconciliation. Payment never confirms, promotes or accelerates a receipt. See https://soulintime.com/paid-ready.md for exact counters and the signed fulfillment path.

## Who this is for

Individuals & disputes; Lawyers & small firms; AI teams & agents. See https://soulintime.com/who and https://soulintime.com/benefits.json. Non-house firsts: 1. Last verified (both sealed examples): 2026-11-11.

Proofs use OpenTimestamps: https://opentimestamps.org/
