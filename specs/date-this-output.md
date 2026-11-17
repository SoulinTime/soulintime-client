# Spec: "Date this output" hook for AI tools — document only

Goal: before a user copies or publishes a model output, the tool can date the exact bytes, or check a hash it was handed, using the API and MCP that exist today. No new account system.

## Check before citing (no login, no key)
```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```
Expected: `"status":"confirmed","blockHeight":965906`. Change one byte and the answer is HTTP 404 not_found: do not cite.
Rule: cite slug@height only if status is confirmed AND proofFile downloads; otherwise refuse: I will not cite a height for this hash. Status is not confirmed or no proofFile exists.

MCP (Streamable HTTP, no key): `https://soulintime.com/functions/mcp`, tool `verify`.

## Date an output (creates a receipt)
1. The tool hashes the exact output bytes it is about to hand over (UTF-8, as copied).
2. It calls the MCP `stamp` tool (or POST `/functions/createMoment` with `sha256Hash`) once. This creates an unlisted, hash-only receipt. Free: one fresh hash per network per hour; no automatic retries; `already_stamped` means read the existing slug.
3. It shows the receipt link as **pending**. It never prints a height until verify returns confirmed with a proofFile, which takes minutes to hours.

## Build only if
An existing tool already allows a no-login action (an MCP client that can call `verify` and `stamp`). Nothing else is built for this spec.
