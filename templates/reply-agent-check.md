# Reply template: "how can an agent check a file existed?" (draft, not posted)

Use only on an exact fit: someone asks how an agent (any HTTP or MCP client) can check, before citing, that a file existed by a date. Max two replies a week, as MorrisMoe. Hold if unsure.

---

Have the agent hash the exact bytes (SHA-256) and check the hash before it cites a date:

```
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

It may cite `slug@height` only if the reply says `"status":"confirmed"` and has a `proofFile`; otherwise it refuses. Change one byte and the same call returns not_found:

```
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

No key, no account; MCP: https://soulintime.com/functions/mcp. It shows these exact bytes existed by that Bitcoin block, not who wrote them or that they are true. Drop-in snippets: https://github.com/SoulinTime/soulintime-client/blob/main/FRAMEWORK_SNIPPET.md
