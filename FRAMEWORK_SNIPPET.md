# Framework snippets: verify before you cite

Works with any HTTP or MCP agent. Grok, ChatGPT, Claude or your own agent: if it can make an HTTP request or call an MCP tool, it can verify. There is no separate product for any vendor or for sovereign agents, just the same endpoint. No package, no SDK, no key, no account. Nothing is created.

Hosted MCP server: `https://soulintime.com/functions/mcp` (Streamable HTTP). Tool: `verify` (read-only). Hash only: your bytes stay on your side.

## Two-curl contract

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

Expected (HTTP 200): `"status":"confirmed","blockHeight":965906` (and a proofFile)

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"
```

Expected (HTTP 404): `{"error":"not_found","hash":"d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab"}` (the whitepaper abstract hash with its last character changed from a to b)

Change one byte. If you do not get not_found, do not trust us.

## The rule every snippet follows

Cite `slug@height` only if status is confirmed AND a proofFile exists. Otherwise refuse with: "I will not cite a height for this hash. Status is not confirmed or no proofFile exists."

Each `cite(h)` below is five lines. Test it with the Door hash (it must cite) and the mutated hash (it must refuse):

```python
import asyncio
print(asyncio.run(cite("019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f")))  # a-hash-is-a-door-that-2026-019bd305@965906
print(asyncio.run(cite("d3871457c0fd628a796f1a61437d9e56ed8c0dcb886c7dca154a00e9602e16ab")))  # I will not cite a height for this hash. ...
```

### OpenAI Agents SDK (`pip install openai-agents`, tested 0.24.0)

```python
from agents.mcp import MCPServerStreamableHttp; import json
async def cite(h):  # cite only confirmed + proofFile, else refuse
    async with MCPServerStreamableHttp(params={"url": "https://soulintime.com/functions/mcp"}, name="soulintime") as s:
        b = json.loads((await s.call_tool("verify", {"hash": h})).content[0].text).get("body") or {}
    return f'{b["slug"]}@{b["blockHeight"]}' if b.get("status") == "confirmed" and b.get("proofFile") else "I will not cite a height for this hash. Status is not confirmed or no proofFile exists."
```

### LangChain / LangGraph (`pip install langchain-mcp-adapters`, tested 0.3.2)

```python
from langchain_mcp_adapters.client import MultiServerMCPClient; import json
async def cite(h):  # cite only confirmed + proofFile, else refuse
    tools = await MultiServerMCPClient({"soulintime": {"url": "https://soulintime.com/functions/mcp", "transport": "streamable_http"}}).get_tools()
    out = await next(t for t in tools if t.name == "verify").ainvoke({"hash": h}); b = json.loads(out if isinstance(out, str) else out[0]["text"]).get("body") or {}
    return f'{b["slug"]}@{b["blockHeight"]}' if b.get("status") == "confirmed" and b.get("proofFile") else "I will not cite a height for this hash. Status is not confirmed or no proofFile exists."
```

### Pydantic AI (`pip install "pydantic-ai-slim[mcp]"`, tested 2.68.0)

```python
from pydantic_ai.mcp import MCPToolset; import json
async def cite(h):  # cite only confirmed + proofFile, else refuse
    async with MCPToolset("https://soulintime.com/functions/mcp") as s:
        r = await s.direct_call_tool("verify", {"hash": h}); b = (r if isinstance(r, dict) else json.loads(r)).get("body") or {}
    return f'{b["slug"]}@{b["blockHeight"]}' if b.get("status") == "confirmed" and b.get("proofFile") else "I will not cite a height for this hash. Status is not confirmed or no proofFile exists."
```

All three were run on 2026-11-16 against the hosted server: the Door hash returned `a-hash-is-a-door-that-2026-019bd305@965906` and the mutated hash returned the refusal. The test runs sent the `X-SoulInTime-Probe: 1` header so they do not count as outside use.

## Pre-send variant

Before your agent sends a file, a contract or an AI answer, it hashes the exact bytes it is about to send (SHA-256, locally) and calls `verify` on that hash. If the result is confirmed with a proofFile, it attaches `slug@height` and the proofFile URL. If not, it sends without any height claim, or it creates a receipt first and says plainly that the receipt is pending. It never states a block it has not seen confirmed.

The refusal is the feature. The claim is only: these exact bytes existed by this Bitcoin block. It does not prove who sent it or that the content is true. More: [AGENT_TEST.md](AGENT_TEST.md) · [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md) · https://soulintime.com/developers
