# SoulInTime local MCP adapter (0.1.0)

Standalone source, tested locally with official `mcp==2.3.0` on Python 3.13. Python 3.11+ recommended. No hosted MCP endpoint, public package listing, or published download is claimed. No GitHub account/repository or hosting required to run locally.

Calling `stamp` creates a receipt. `verify` and `first_at` do not. Test with the sealed hash below; do not call `stamp` to evaluate.

## Install and launch
Unzip into a directory you control. Create a virtual environment and install the pinned SDK:

```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python server.py
```

The last command speaks MCP over stdin/stdout; waiting silently is normal. Windows: use `.venv\Scripts\python.exe`. `requirements.lock.txt` records all versions from the tested environment (platform-specific dependencies may differ). No key/account is required. Internet is needed for dependency installation and explicit tool requests.

Example host configuration (replace paths with your absolute extracted paths):

```json
{"mcpServers":{"soulintime":{"command":"/absolute/path/soulintime-mcp/.venv/bin/python","args":["/absolute/path/soulintime-mcp/server.py"]}}}
```

No shell activation needed. Configuration field names vary by host; this is the common mcpServers format.

## Test without creating
Invoke `verify` with:

```json
{"hash":"019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"}
```

Existing Door: https://soulintime.com/moment/a-hash-is-a-door-that-2026-019bd305 — block 965906 at the tested read. Re-check before citing. This is a GET, not a new stamp. Our test is our probe, not evidence of external use/M1.

## Tools and rules
- `stamp(hash)`: explicit invocation POSTs hash only to createMoment. Never invoked on startup/listing, never used in live tests. Default server behavior is unlisted. Requires user intent to create. May return pending, failed, 400 or 429. Tool response is the upstream status/body, not a claim of confirmation.
- `verify(hash)`: GET existing receipt; adds `citable`, `citation`, and reason. Cite `slug@height` only when v1Verify returns confirmed, nonempty proofFile, matching hash, slug, and positive integer height. Pending, height_asserted and missing proof refuse citing. This checks server metadata; it does not download or cryptographically validate the proof. Keep file and .ots for independent OpenTimestamps verification.
- `first_at(hash,height?)`: GET earliest confirmed PUBLIC receipt; excludes unlisted/private. Optional nonnegative strict integer maps to atOrBefore. Zero returns no possible confirmed receipt locally without a request (upstream only accepts positive heights). Rechecks v1Verify for proofFile, same slug/height and requested bound before providing a citation. Null/disagreement/missing proof refuses.

Fixed origin https://soulintime.com; redirects disabled. 15-second HTTP timeout; response cap 1 MiB. HTTP status, decoded raw body, parsed JSON/body, X-RateLimit-Reset and Retry-After preserved for bounded responses. Oversize/network failures return explicit errors. No retry, loop, polling, background job, persistence, telemetry, file uploads or keys. On 429 respect reset (Unix seconds) before a future intentional retry. `already_stamped` does not clear: inspect existing slug instead. Standard-library HTTP trusts the OS TLS CA configuration; system proxy environment may apply. Bounded reads are not a global wall-clock execution deadline.

Height is not a truth claim. Tip is never this file’s height. API availability still depends on this host; downloaded .ots can be checked independently.

## Tests
```
.venv/bin/python test_http.py
.venv/bin/python test_protocol.py
```
`test_protocol.py` runs real official SDK client → stdio subprocess server → initialize/tools/list/tools/call. All stamp calls are fixture-mocked, with unexpected requests rejected. It ends with ONE LIVE GET verify probe for Door, writes door_probe.json, and never does a live POST. Do not count that as M1. `test_http.py` mocks transport and checks bounded body, fixed origin, timeout, 429 body/reset preservation, one request and redirects. Actual output included.
