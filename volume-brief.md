# SoulInTime volume brief

```
curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'
```

**1. Test without creating.** Check the sealed example first; nothing below creates a receipt. Sealed hash `019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f`, receipt https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305 (block 965906). Over plain HTTP: `curl -s 'https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f'` should return `"status":"confirmed"`, `"blockHeight":965906` and a `proofFile`. Over the hosted MCP endpoint (https://soulintime.com/functions/mcp, stateless Streamable HTTP, no key), call the read-only `verify` tool: `curl -s -X POST https://soulintime.com/functions/mcp -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' --data '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"verify","arguments":{"hash":"019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"}}}'`. The proof file is at https://soulintime.com/functions/v1Proof?id=a-hash-is-a-door-that-2026-019bd305&ots=1 and verifies without this host: `ots verify -d 019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f a-hash-is-a-door-that-2026-019bd305.ots`. Do not call `stamp` or POST createMoment to test; both create a receipt.

**2. Free limits, as the code enforces them today.** Creating (createMoment, and the MCP `stamp` tool that calls it): one fresh hash per network per hour. A hash that already has a receipt answers `429` with `reason: already_stamped`; that is permanent and does not clear when the hour resets, so read the existing receipt instead. Checking (v1Verify, and the MCP `verify` tool): 120 lookups per IP per 60 seconds, best effort per server instance; every reply carries `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset` (Unix seconds). v1FirstAt has no endpoint limit of its own; platform limits may still apply. Hosted MCP calls share the backend's egress, so they may share the upstream allowance. On a rate-limited `429` (not `already_stamped`), wait until `X-RateLimit-Reset` and do not tight-loop. Checking stays free. There is no paid volume offer today and no price.

Legacy v1Anchor has a separate anonymous cap of 100 over a rolling 24 hours, counted from public, pending, ownerless rows rather than all anchors. This is not the createMoment allowance; no reset available.

**3. What to email.** If you need more than this, email morris@mifalai.com with: one hash you have already stamped or checked (the SHA-256, never the file), what you are dating and why, and how many fresh hashes per hour you expect (typical and peak). We answer by email. Nothing is charged, and no volume is promised, until terms are sent to you and you agree to them.

Expected free limits: one fresh hash per network per hour; v1Verify 120 checks per IP per 60 seconds, best effort per instance.  
“More” means rate / book / webhook; terms are not set and no paid capability is offered yet.  
Email morris@mifalai.com for address and price.
Issues welcome: https://github.com/SoulinTime/soulintime-client/issues
