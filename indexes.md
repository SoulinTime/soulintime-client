# Indexes

Where agents and tools can find SoulInTime. Checked weekly (Mondays). Every "listed" URL must resolve; a broken one is fixed or removed the same day.

Read-only check every listing should carry:

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

| Index | URL | Status | Checked |
|---|---|---|---|
| Official MCP Registry | https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest | Listed (`io.github.MorrisMoe/soulintime`, version 0.1.1, active, remote https://soulintime.com/functions/mcp). Description field max 100 characters, so it cannot hold the curl; changing it needs a republish with a login, so unchanged | 2026-11-16 |
| mcpservers.org | https://mcpservers.org/servers/soulintime/soulintime-client | Listed; shows this README with both read-only curls; links resolve (200) | 2026-11-16 |
| Glama (connector) | https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime | Listed; page shows Healthy, uptime 100.0% over the last 24 hours (unclaimed listing) | 2026-11-16 |
| awesome-remote-mcp-servers | https://github.com/punkpeye/awesome-remote-mcp-servers/pull/4785 | Submitted; pull request open, mergeable, CI labels endpoint-ok and has-connector, no review or comments yet (unchanged) | 2026-11-16 |
| MCP.Directory | https://mcp.directory/submit | Not listed yet. The public form (no account) reports "This repository has already been submitted. We'll review it soon!" — in their review queue; no public listing page yet | 2026-11-16 |
| awesome-mcp-servers | https://github.com/punkpeye/awesome-mcp-servers | Not submitted. Its CI requires a Glama server page (glama.ai/mcp/servers/SoulinTime/soulintime-client), which does not exist yet (404) | 2026-11-16 |
| PulseMCP | https://www.pulsemcp.com/servers?q=soulintime | Not listed (search 0). Submissions are paused (their /submit page, last updated 2026-09-03); they say they ingest the Official MCP Registry, where SoulInTime is listed. Still paused on 2026-11-16. Nothing to submit | 2026-11-16 |
| Smithery | https://smithery.ai | Not listed. Publishing needs a Smithery account | 2026-11-15 |

Agent test: [AGENT_TEST.md](AGENT_TEST.md). Framework hook: [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md). People: https://soulintime.com/check
