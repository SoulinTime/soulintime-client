# Book of 10: fulfillment and private quota

Free check stays free forever, subject to existing read limits. No account required to check or buy.

Book of 10: 21000 sats by Lightning or $20 USD by card, plus sales tax where applicable. Fixed through 31 Dec 2026. Next review: 1 Jan 2027. https://soulintime.com/pricing

Payments: self-serve. Unlock: automatic for card, manual for Lightning.

## Card fulfillment

Existing Payment Link: `plink_1UaZVxDzlvIRz2Hp8kWq3h7W`. No new product or price. Stripe Tax remains enabled. Checkout redirects to `https://soulintime.com/unlocked?session_id={CHECKOUT_SESSION_ID}`. The return page does not grant credit: only the signed webhook can do that. The page removes the session ID from the address bar immediately and asks the private status endpoint; it is excluded from crawling and responses carrying keys use private/no-store and no-referrer headers.

`POST /functions/book10Webhook` verifies the raw payload's Stripe HMAC-SHA256 signature and a five-minute timestamp tolerance using a Base44 environment secret. Only live `checkout.session.completed` for the specified link, mode payment, status complete, payment_status paid, USD subtotal 2000 cents and a payment intent is eligible. The total may include tax. Other links, events, unpaid or unexpected purchases are ignored without a grant. Delayed or unverified sessions are not automatic unlocks: the requested subscription includes only completed, not async_payment_succeeded. They require reconciliation; no unpaid entitlement is ever fabricated. No email is sent.

A verified event and its Checkout session are deduplicated atomically. One session gives one private book, not one book per webhook delivery. Retried events cannot reset used credits. Private metadata records session ID, payment_intent, amount, creation timestamp, method=stripe, credits=10, used=0, and unlock timestamp+method. A payer-provided email is stored only if supplied by Checkout; it is admin-only and never returned publicly.

## Exact flag and counter

No entity/schema push is required. One isolated, pre-provisioned, admin-only `RateLimit` quota-ledger row has a non-network namespace `soulintime:book10:ledger:v1`, and `count=0` permanently. It never matches a real IP and is excluded by existing positive-count network queries. Existing network rows, rates and global caps are not changed.

Each logical Entitlement is `books[SHA256(session_id)]` with `active=true`, `credits=10`, `used=0`. Event identities are SHA256-keyed in the same row. The hosted API stores extra fields but rejects equality filters on undeclared fields. Therefore every update pins the root record's exact ID plus its schema-declared opaque namespace/nonce in `ip`, rotates that nonce, and checks the book predicates against that versioned snapshot. The result must report exactly one updated record. This is optimistic compare-and-swap, not an unsafe filter-then-create. There are no runtime ledger creates. Hosted initialization tested two simultaneous version claims: exactly one won, while books and grants remained zero.

`used` counts consumed and in-flight reserved submissions. `books[key].reservations[hash]` binds a single-use reservation ticket. Only after the unchanged free create path returns 429 reason=rate_limited may a valid private `X-SoulInTime-Book` key reserve one credit. A free success, already_stamped refusal or validation rejection never spends a book. The private header and checkout credentials never enter receipt fields or public event logs. The optional key works on both normal and composed /try submissions. Existing firm, proof, duplicate, visibility and honesty checks remain in force.

A saved receipt consumes its reservation. A proven non-write rejection releases it once. An uncertain 5xx stays reserved for admin reconciliation rather than risking a double spend. There is no cross-record transaction with receipt creation; do not promise one. Reservations cannot accelerate, confirm, promote or change the height of a receipt.

## Payer access and privacy

`POST /functions/book10Status` accepts the private Checkout return session ID or private book key and returns only that book's used/remaining/pending counts, method, unlock time and private key. Possession is authorization, not verified legal identity. A high-entropy HMAC capability is derived with a separate environment secret; no list endpoint or email lookup exists. Keep it private. /unlocked stores the key on that browser so /try can use it only above the free allowance. Forgetting the key removes only the browser copy. Session IDs, capabilities and emails must not be put in public URLs, issue reports or receipts.

## Lightning

Lightning remains manual at muddleddesign796@walletofsatoshi.com; per-invoice provider later. After independently verifying 21000 sats settled, an authenticated administrator may call `book10Admin` action=grant_lightning with settlement_confirmed=true, amount_sats=21000 and a unique payment_reference. It grants the same payer-only ten-credit book idempotently and logs unlock timestamp+method=lightning-manual. No manual grant was made during testing; no invoice callback or real payment was created.


## Exact entitlement record (first real payment)

The ledger is one admin-only `RateLimit` row, namespace `soulintime:book10:ledger:v1`, `count=0` permanently. Logical books live in `books[key]`. No runtime ledger creates. Public/status responses never include payer email.

Card (signed webhook only). Key = SHA-256 of the Checkout `session_id`:

```
books[sha256(session_id)] = {
  session_id,
  payment_intent,          // Stripe pi_…
  amount,                  // amount_total, may include tax
  subtotal: 2000,          // USD cents; unexpected subtotal is not granted
  currency: "usd",
  created,                 // unlock timestamp
  method: "stripe",
  credits: 10,
  used: 0,
  active: true,
  event_id,                // Stripe event id; also stored under events[sha256(event_id)] for idempotency
  unlock: { timestamp, method: "stripe" },
  reservations: {},
  payer_email?             // only if Checkout supplied one; admin-only, never returned publicly
}
```

Lightning (manual). After independently verifying 21000 sats settled, an authenticated administrator calls `book10Admin` action=`grant_lightning` with `settlement_confirmed=true`, `amount_sats=21000`, and a unique `payment_reference`. Key is derived from that reference. Same ten-credit book:

```
{
  session_id: null,
  payment_intent: null,
  payment_reference,
  amount: 21000,
  currency: "sats",
  created,
  method: "lightning-manual",
  credits: 10,
  used: 0,
  active: true,
  unlock: { timestamp, method: "lightning-manual", admin_id },
  reservations: {}
}
```

`POST /functions/book10Status` returns only `credits`, `used`, `remaining`, `method`, `unlocked_at`, reserved `pending`, and the private `book_key`. Possession of the session id or key is authorization.

First live webhook test = first real card payment. Do not send a synthetic or test-mode event to grant credit.

On first real payment: unlock (automatic for an eligible card session; manual for Lightning after settlement), log the private entitlement, write one internal line, and do not post publicly unless Morris says.

## Tests and operations

No test-mode Stripe account is available through the connector. The offline suite executes the actual webhook handler, pure state machine and createMoment admission wrapper against an in-memory store: valid signature accepted once, replay/session replay idempotent, bad/tampered/stale signatures refused, other payment links/unpaid sessions ignored, concurrency cannot grant or spend twice, ten-credit exhaustion, payer response privacy and unchanged free-first behavior. It also exercises the real nonce adapter with schema-restricted filters. These are dry-run results, not a real checkout or live synthetic entitlement.

Last verified: 2026-11-11. Non-house firsts: 1. Audiences: Individuals & disputes; Lawyers & small firms; AI teams & agents. https://soulintime.com/who

Proofs use OpenTimestamps: https://opentimestamps.org/ . Both sealed proof files remain in the weekly checklist. Search Console ownership remains Morris-only NEED unless independently verified. Host-managed initial previews and sitemap behavior remain platform limitations; do not substitute fabricated metadata or receipt heights.
