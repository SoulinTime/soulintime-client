# SoulInTime statement format, v0.1 (`sit-statement/0.1`)

Status: v0.1, **pinned** (dated 22 Nov 2026; live on soulintime.com since that day). Fields and rules in this file do not change; any change ships as a new version (`sit-statement/0.2`) next to this one. Anyone may issue statements in this format with their own key. Changes to the API around it: [CHANGELOG.md](CHANGELOG.md).

A **statement** is a small signed JSON object: *these exact bytes were confirmed (or refused) at Bitcoin block N.*
The time comes from Bitcoin through an OpenTimestamps `.ots` proof. The signature says who issued the statement.
Checking needs neither the issuer nor its website.

## Fields

| field | type | meaning |
|---|---|---|
| `v` | string | always `"sit-statement/0.1"` |
| `sha256` | 64 lowercase hex | SHA-256 of the file (the bytes being dated) |
| `status` | `"confirmed"` or `"refused"` | there is no pending statement |
| `block_height` | integer > 0 | confirmed: the Bitcoin block the `.ots` attests. refused: the chain tip the issuer saw when it refused |
| `block_hash` | 64 lowercase hex | hash of that block (check it against your own node or any explorer) |
| `ots_sha256` | 64 hex, or `null` | SHA-256 of the `.ots` file bytes the issuer serves. `null` on a refusal |
| `issued_at` | `YYYY-MM-DDTHH:MM:SSZ` | when the issuer signed (UTC). Not the date of the file |
| `issuer` | string | `"soulintime.com"` for statements from this service |
| `kid` | string | key id: first 16 hex characters of SHA-256 of the raw 32-byte Ed25519 public key |
| `reason` | `"not_found"` or `"not_confirmed"` | refusals only |
| `priority` | `true` | optional; present only on a statement issued from a Priority purchase |
| `sig` | base64url, no padding | Ed25519 signature (see below) |

No other fields are allowed in v0.1. Unknown versions must be rejected.

## Signature

1. Take every field except `sig`.
2. Serialize with RFC 8785 (JSON Canonicalization Scheme): keys sorted by UTF-16 code units, no whitespace, integers as plain digits, strings JSON-escaped.
3. Sign the UTF-8 bytes with Ed25519. `sig` = base64url(signature) without `=` padding.

## Rules

- **Pending never yields a statement.** A statement is issued only after the `.ots` proof's Bitcoin attestation matches block `block_height`'s merkle root.
- A **refusal** has the same shape: `status: "refused"`, a `reason`, `ots_sha256: null`, and the chain tip the issuer saw. It means "not confirmed as of that block". Never cite a block from a refusal.
- Cite only a confirmed statement whose signature verifies against a published key.
- The `.ots` proof is the time evidence; it verifies without the key and without the issuer.

## Verify (offline)

1. `sha256(file) == sha256`.
2. Ed25519-verify `sig` over JCS(all fields but `sig`) with the public key for `kid`; check `kid` = first 16 hex of SHA-256(public key).
3. `sha256(proof.ots) == ots_sha256`, then `ots verify -d <sha256> proof.ots` names `block_height`; that block's hash equals `block_hash`.

Reference verifiers (one file each, no dependencies): [`verifier/verify_statement.py`](verifier/verify_statement.py), [`verifier/verify_statement.mjs`](verifier/verify_statement.mjs).

## Keys

Current key (see [`keys/`](keys/), also on https://soulintime.com/protocol#statements):

- kid `0a64aa45b8ce17a7`
- Ed25519 public key (raw, base64url) `GrcQ1ZzlNQAtU8GyezaWCmyFjzjP2NEknvkAd5CQXxc`
- fingerprint sha256(raw public key) `0a64aa45b8ce17a781b91c1196907961f8ec27479a34a8f39c557e2b0b2797ee`

Retired keys stay listed forever with the period they signed, so old statements keep verifying.

## Size and field limits

- A statement is a single JSON object under 1 KB (about 480 bytes in practice). `sha256`, `block_hash` and `ots_sha256` are exactly 64 lowercase hex characters; `sig` is 86 base64url characters; `kid` is 16 hex.
- `block_height` is a positive integer below 2^53. `issued_at` has whole seconds and a `Z`.
- `POST /functions/v1Statement` accepts a pasted statement of at most 4 KB. No other fields are allowed in v0.1.
- The request takes only a SHA-256 (64 hex); a large file and a small file cost the same, because only the hash is sent.

## Request one (signed out)

```sh
curl -s -X POST https://soulintime.com/functions/createMoment -H "Content-Type: application/json" -d "{\"sha256Hash\":\"$(sha256sum yourfile | cut -c1-64)\"}"
```

The answer is a receipt (`{"slug":"moment-…","proofFile":"…","status":"in_calendar"}`), not a statement. One fresh hash per network per hour is free and needs no account; a 429 (`reason` `rate_limited` or `already_stamped`) is never a statement. Once Bitcoin confirms (usually 1 to 6 hours), `GET /functions/v1Statement?hash=<sha256>` returns the statement. Responses carry `X-SoulInTime-Request-Id` and `X-Statement-Spec: sit-statement/0.1`. Code: [examples/](examples/README.md).

## How to cite

Paste the cite line exactly as returned, on one line, unchanged: `sha256 <hash> existed by Bitcoin block <N>. Statement: <url>`. It says only that these exact bytes existed by that block; it does not say who made them or that they are true. Cite only a confirmed statement: pending, rate-limited and refused answers carry `"cite":null` and must not be cited. Anyone can check the statement offline with the public key and the .ots, and it still verifies if we disappear.

The cite line is not part of the signed statement (v0.1 allows no extra fields); it is derived from `sha256` and `block_height` and delivered beside it:

- `GET /functions/v1Statement?hash=<sha256>&format=cite`: the line as `text/plain`, then a newline. Confirmed only; otherwise the signed refusal (HTTP 404).
- Header `X-SoulInTime-Cite` on every confirmed `v1Statement?hash=` answer. The default JSON body is the statement, byte for byte.
- `?with=cite`: `{"statement":{...},"cite":"...","statement_url":"...","card_url":"...","text_url":"...","offline_steps":[...],"still_verifies":"..."}`.
- `createMoment` 429 `already_stamped` for a confirmed hash: the existing `statement` and its `cite`. Every other refusal: `"statement":null,"cite":null` and `do_not_cite` ([fixture](examples/fixtures/refusal-rate-limited.json)).
- MCP `stamp`, the plain-text export and the Forward text carry the same line.

Format: `sha256 ` + 64 lowercase hex + ` existed by Bitcoin block ` + decimal height + `. Statement: https://soulintime.com/statement?hash=` + the same hex. ASCII, one line, 218 characters. Example: [cite-door.txt](examples/fixtures/cite-door.txt).

## Share message format

Forward text: the cite line, then `These exact bytes existed by block <N>; it does not prove who made them or that they are true. Check it yourself, even offline: <statement url>`.

- Card URL (unfurls with the hash and block): `https://soulintime.com/functions/statementCard?hash=<sha256>` (`og:title` `sha256 <12 hex>… existed by Bitcoin block <N>`; 404 if no confirmed statement).
- Markdown: `[sha256 <12 hex>… existed by Bitcoin block <N>](https://soulintime.com/statement?hash=<sha256>)`
- HTML: `<a href="https://soulintime.com/statement?hash=<sha256>">sha256 <12 hex>… existed by Bitcoin block <N></a>`

The claim is always and only "existed by block N".

Badge (concept only, not built): a shields-style badge `existed by | block <N>` linking to the statement URL, rendered only for a confirmed statement.

## Firsts filter

`GET /functions/v1Statement?firsts=1&since=<height>` (alias `min_block`) lists confirmed statements with `block_height >= height`, each row with its `cite`; for the static file: `jq '.firsts|map(select(.block_height>=<height>))' firsts.json`.

## Export URL pattern

- Human-readable: `https://soulintime.com/statement?hash=<sha256>` (the hand-off: Forward text, QR to `/check`, `.ots` and statement downloads, offline steps).
- Plain text (terminals and agents): `https://soulintime.com/functions/v1Statement?hash=<sha256>&format=text`.
- Machine-readable: `https://soulintime.com/functions/v1Statement?hash=<sha256>` (the statement JSON itself).
- All confirmed public statements: `https://soulintime.com/firsts.json` (snapshot) and `https://soulintime.com/functions/v1Statement?firsts=1&since=<height>` (live).

## Endpoints (soulintime.com)

- `GET https://soulintime.com/functions/v1Statement?hash=<sha256>`: 200 + statement, or 404 + signed refusal.
- `POST https://soulintime.com/functions/v1Statement` with `{"statement":{...}}`: `signature_valid`, `match` against the receipt.
- `GET https://soulintime.com/functions/v1Verify?hash=<sha256>`: a confirmed receipt also carries `statement` next to `proofFile`.
- Human page: `https://soulintime.com/statement?hash=<sha256>` (export, QR, `.ots`, forward).
- `GET https://soulintime.com/functions/v1Statement?firsts=1` (confirmed statements list), `?health=1` (status), `?key=1` (public key).

Test vectors: [`verifier/vectors/`](verifier/vectors/) (valid, tampered, wrong key, refused).

## Examples

The Door, block 965906:

```json
{
 "v": "sit-statement/0.1",
 "sha256": "019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f",
 "status": "confirmed",
 "block_height": 965906,
 "block_hash": "00000000000000000001b1d2e4220a0d1600a59bd2d3753743fa3654679b5130",
 "ots_sha256": "0661ce7e66b59e8d594b379f33e7512f7e0e7e3f22ec6d8ab0477a5b15400294",
 "issued_at": "2026-11-22T15:43:53Z",
 "issuer": "soulintime.com",
 "kid": "0a64aa45b8ce17a7",
 "sig": "zhvCuFJVGbow3scYxBseprsS_oEBw5cOOXn5VaFYrfoyFudZRrhi75rety4SjDVGCiEeO9jvrJsaTvxrw4FjBw"
}
```

The Bitcoin whitepaper abstract ([whitepaper-abstract.txt](whitepaper-abstract.txt)), block 975352:

```json
{
 "v": "sit-statement/0.1",
 "sha256": "d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16aa",
 "status": "confirmed",
 "block_height": 975352,
 "block_hash": "000000000000000000005e5f7c5aa92d5000598462f7a7d85e7a0db4fe7cfb15",
 "ots_sha256": "5ae13dcdbdafd843fe310ef71e90a5a1c76f99dfb99099e30154e6ce6ffd54f6",
 "issued_at": "2026-11-22T15:43:53Z",
 "issuer": "soulintime.com",
 "kid": "0a64aa45b8ce17a7",
 "sig": "toMwxRs4sjXz3lgGda7bsfFY-sa7J0eNCvly2mYbhiYQtz6kCuULsbsnm7qGMy6y9ocG8it3zKI4M-lXt6ufCA"
}
```

Refusal (shape; values depend on the tip when asked):

```json
{"v":"sit-statement/0.1","sha256":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab","status":"refused","reason":"not_found","block_height":977000,"block_hash":"<tip hash>","ots_sha256":null,"issued_at":"2026-11-22T16:00:00Z","issuer":"soulintime.com","kid":"0a64aa45b8ce17a7","sig":"<base64url>"}
```
