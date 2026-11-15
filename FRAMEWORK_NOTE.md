# Framework note — calling verify before citing

A sketch, not an integration. SoulInTime ships no SDK or adapter. The hosted MCP server is `https://soulintime.com/functions/mcp` (Streamable HTTP, no key, no account). Its `verify` tool is read-only and creates nothing.

## Three clients that support remote HTTP MCP, tested 2026-11-15

Each was pointed at the hosted URL and called `verify` with the Door hash. No LLM, no key. Method: [How it was tested](#how-it-was-tested).

| Framework / client | Version | Can call verify today | Evidence |
|---|---|---|---|
| OpenAI Agents SDK (`agents.mcp.MCPServerStreamableHttp`) | openai-agents 0.24.0 | **yes** | `list_tools` → `stamp, verify, first_at`; `call_tool("verify")` → `citable: true`, `a-hash-is-a-door-that-2026-019bd305@965906`, status `confirmed` |
| LangChain / LangGraph (`langchain_mcp_adapters.client.MultiServerMCPClient`, `transport="streamable_http"`) | langchain-mcp-adapters 0.3.2 | **yes** | same tools; `verify.ainvoke` → same citation, status `confirmed` |
| Pydantic AI (`pydantic_ai.mcp.MCPToolset(url)`) | pydantic-ai-slim 2.68.0 | **yes** | same tools; `direct_call_tool("verify")` → same citation, status `confirmed`. Note: v2 removed `MCPServerStreamableHTTP`; use `MCPToolset` |

Not tested here: Claude (remote connectors, Claude Code `--transport http`) and Cursor (`url` in `mcp.json`) document remote HTTP MCP, but calling them needs an account. Status: **unknown**.

## Pre-cite hook (5 lines)

```python
r = mcp.call_tool("verify", {"hash": h})        # or GET https://soulintime.com/functions/v1Verify?hash=<h>
b = r.get("body", r)                             # MCP wraps the REST body in "body"
if b.get("status") == "confirmed" and b.get("proofFile") and http_get(b["proofFile"]).ok:
    cite(f'{b["slug"]}@{b["blockHeight"]}')
else: refuse("I will not cite a height for this hash. Status is not confirmed or no proofFile exists.")
```

A 404 `{"error":"not_found"}`, a 429 `{"error":"rate_limited"}`, or any status other than `confirmed` takes the refuse branch. A one-byte change to the input takes it too (see [AGENT_TEST.md](AGENT_TEST.md), section 3).

## What would make a framework adopt it

A framework adopts a hook like this when it is a few lines, needs no key, and can't produce a false citation. The hook above is already that. What's missing is a reason to reach for it: a tool or retrieval step that returns content with a SHA-256 attached and a "cite with provenance" option the developer turns on. Inclusion in that framework's MCP or tool catalog, plus a copy-paste example that passes with the Door hash, is enough. No partnership or SDK is needed.

## What's missing

Visibility and demand. Since 2026-11-15 the server tags every verify call internally as door, whitepaper or other, with own probes excluded. Before that, an outside verify couldn't be told apart from our own. The first "other" (a hash we didn't put in the docs) is the signal that someone is using the hook on their own bytes. The hook is the adoption shape. What's missing is a caller with dated hashes to check. Only after "other" is above zero is a framework-specific example worth writing.

## Traffic already seen

None identifiable. The AI-traffic log shows only crawlers (ClaudeBot, GPTBot, Googlebot, Meta-ExternalAgent) on the sitemap, RSS and status pages. Before 2026-11-15 the server stored no user agent for verify calls, and this pass stores none. Glama shows a listing and endpoint health but no per-client usage.

## How it was tested

`pip install openai-agents langchain-mcp-adapters pydantic-ai-slim[mcp]`, then each client connected to the hosted URL and called `verify` with hash `019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f`. The test sent the `X-SoulInTime-Probe: 1` header so it doesn't count as outside use. Nothing was created.

The claim is only: these exact bytes existed by this Bitcoin block.
