# Monthly, Yearly and Starter: payment and access

Free check stays free forever. No account required to check or buy.

Paid stamp balances, each a one-time payment with no auto-renew (buy again to continue): Monthly — 100 stamps / 30 days, $49 USD; Yearly — 1500 stamps / 365 days, $399 USD, best for teams and agents; Starter pack — 10 stamps / 90 days, $20 USD. Card prices plus applicable tax. Lightning: coming soon. Prices and checkout: https://soulintime.com/pricing. Prices effective 12 Nov 2026. Next review: 1 Feb 2027. No account required to check or buy. Verified card payment unlocks your private balance at https://soulintime.com/unlocked. Credits apply only above the existing free per-network allowance; global limits stay unchanged. Payment never confirms, promotes or accelerates a receipt. Questions: https://github.com/SoulinTime/soulintime-client/issues. Never publish private payment references or keys.

Only a signed, eligible, paid Stripe Checkout event grants the purchased stamp balance. A return URL alone never grants access. The webhook recognizes the fixed Payment Links and their prices (Monthly $49, Yearly $399, Starter $20; the retired $99 Monthly link is deactivated but still honoured for a Checkout already started); other prices, unpaid sessions and malformed events grant nothing. Events and sessions are deduplicated atomically; replay cannot reset a balance or expiry.

Monthly expires 30 days from payment. Yearly expires 365 days from payment. Starter expires 90 days from payment. Expired balances cannot reserve more stamps. The private record contains product, product_id, price_id, stamps, credits, used, expires_at, payment reference, currency, paid timestamp, unlock method and reservations. Only that balance is returned to the holder of its private balance key. There is no account login yet.

The unchanged free path runs first. Above-free reservations use the existing private quota ledger; free and global rate limits do not change. No payment can confirm a receipt or change its Bitcoin height. Keep the original and OpenTimestamps proof together. Cite only when confirmed plus proofFile; otherwise refuse.

First live webhook test = first real card payment. No test purchase, receipt, stamp or production entitlement was created. Offline fixtures are not live payment verification.

Last verified: 2026-11-12. Whitepaper lead example: https://soulintime.com/moment/moment-ao91b5a0 . Door remains the agent evaluation object. Protocol: https://opentimestamps.org/ .

## Entitlement format

`books[SHA256(session_id)] = {product, product_id, price_id, stamps:100|1500|10, credits:100|1500|10, used:0, expires_at:payment+30d|365d|90d, created:payment_time, method:"stripe", session_id, payment_intent, amount, subtotal:4900|39900|2000 (legacy 9900), currency:"usd", active:true, event_id, unlock:{timestamp,method}, reservations:{}}`. Payer email, if Checkout supplies it, stays admin-only and is never returned by status. Event identities are SHA256-keyed in the same private ledger. No real customer record appears in this document.

Expiry is enforced at reservation time. Only the fixed link/price pair and matching subtotal qualify; a signed event naming an unknown price grants nothing. The existing namespace/nonce CAS preserves idempotency. Free/global limits are unchanged.
