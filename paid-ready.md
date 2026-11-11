# Monthly and Starter: payment and access

Free check stays free forever. No account required to check or buy.

Recommended: Monthly — 100 stamps / 30 days, $99 USD plus applicable tax by card: https://buy.stripe.com/eVqcN55pH73n2Kyfms8IU01. One payment, 30 days. No auto-renew. Buy again to continue. Lightning reference price: 168,000 sats; Lightning checkout is paused, do not pay. Starter pack — 10 stamps / 90 days: $20 USD plus applicable tax by card (https://buy.stripe.com/7sY6oH9FXcnH1Gu7U08IU00); Lightning reference price 21,000 sats. https://soulintime.com/pricing. Next review: 1 Jan 2027. No account required to check or buy. Verified card payment unlocks your private balance at https://soulintime.com/unlocked. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.

Only a signed, eligible, paid Stripe Checkout event grants the purchased stamp balance. A return URL alone never grants access. The webhook recognizes the two fixed Payment Links and their prices; other prices, unpaid sessions and malformed events grant nothing. Events and sessions are deduplicated atomically; replay cannot reset a balance or expiry.

Monthly expires 30 days from payment. Starter expires 90 days from payment. Expired balances cannot reserve more stamps. The private record contains product, product_id, price_id, stamps, credits, used, expires_at, payment reference, currency, paid timestamp, unlock method and reservations. Only that balance is returned to its private-key holder. Never publish its private key.

The unchanged free path runs first. Above-free reservations use the existing private quota ledger; free and global rate limits do not change. No payment can confirm a receipt or change its Bitcoin height. Keep the original and OpenTimestamps proof together. Cite only when confirmed plus proofFile; otherwise refuse.

First live webhook test = first real card payment. No test purchase, receipt, stamp or production entitlement was created. Offline fixtures are not live payment verification.

Last verified: 2026-11-11. Whitepaper lead example: https://soulintime.com/moment/moment-ao91b5a0 . Door remains the agent evaluation object. Protocol: https://opentimestamps.org/ .

## Entitlement format

`books[SHA256(session_id)] = {product, product_id, price_id, stamps:100|10, credits:100|10, used:0, expires_at:payment+30d|90d, created:payment_time, method:"stripe", session_id, payment_intent, amount, subtotal:9900|2000, currency:"usd", active:true, event_id, unlock:{timestamp,method}, reservations:{}}`. Payer email, if Checkout supplies it, stays admin-only and is never returned by status. Event identities are SHA256-keyed in the same private ledger. No real customer record appears in this document.

Expiry is enforced at reservation time. Only the fixed link/price pair and matching subtotal qualify; a signed event naming an unknown price grants nothing. The existing namespace/nonce CAS preserves idempotency. Free/global limits are unchanged.
