# Indexes

Where agents and tools can find SoulInTime. Checked weekly (Mondays). Every "listed" URL must resolve; a broken one is fixed or removed the same day.

Read-only check every listing should carry:

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

| Index | URL | Status | Checked |
|---|---|---|---|
| Official MCP Registry | https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest | Listed (`io.github.MorrisMoe/soulintime`, active). Description field max 100 characters, so it cannot hold the curl | 2026-11-15 |
| mcpservers.org | https://mcpservers.org/servers/soulintime/soulintime-client | Listed; shows this README with both read-only curls; links resolve | 2026-11-15 |
| Glama (connector) | https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime | Listed; endpoint healthy | 2026-11-15 |
| awesome-remote-mcp-servers | https://github.com/punkpeye/awesome-remote-mcp-servers/pull/4785 | Submitted; pull request open, CI labels endpoint-ok and has-connector, no review yet | 2026-11-15 |
| MCP.Directory | https://mcp.directory/submit | Not listed yet. The public form (no account) reports "This repository has already been submitted. We'll review it soon!" — in their review queue | 2026-11-15 |
| awesome-mcp-servers | https://github.com/punkpeye/awesome-mcp-servers | Not submitted. Its CI requires a Glama server page (glama.ai/mcp/servers/SoulinTime/soulintime-client), which does not exist yet | 2026-11-15 |
| Smithery | https://smithery.ai | Not listed. Publishing needs a Smithery account | 2026-11-15 |

Agent test: [AGENT_TEST.md](AGENT_TEST.md). People: https://soulintime.com/check
