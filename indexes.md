# Indexes

Where agents and tools can find SoulInTime. Checked weekly (Mondays). Every "listed" URL must resolve; a broken one is fixed or removed the same day.

Every listing should match [AGENT_CARD.md](AGENT_CARD.md) where it shows our text. The read-only check every listing should carry:

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

| Index | URL | Status | Matches AGENT_CARD.md | Checked |
|---|---|---|---|---|
| Official MCP Registry | https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest | Listed (`io.github.MorrisMoe/soulintime` 0.1.1, active, remote https://soulintime.com/functions/mcp). Description (max 100 characters): "Sealed 019bd305… @ block 965906. Verify." Changing it needs a republish with a login, so unchanged | Yes, as far as it goes: Door hash, block 965906 and the MCP URL match; too short to hold the card | 2026-11-16 |
| mcpservers.org | https://mcpservers.org/servers/soulintime/soulintime-client | Listed; renders an earlier snapshot of this README | Partly: Door curl, block 965906 and MCP URL match; the card block (added 2026-11-16) is not in their snapshot yet. Nothing to change on our side | 2026-11-16 |
| Glama (connector) | https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime | Listed; Healthy (unclaimed listing; not claimed) | Yes for what it shows: Door hash and MCP URL | 2026-11-16 |
| mcp.so | https://mcp.so/servers/soulintime-client | Listed (picked up from GitHub; nothing submitted). Older repo description, "No standard config provided". Its submit form is a $39 paid listing behind a Sign In; not used | Partly: Door hash, block and MCP URL match; older text | 2026-11-16 |
| awesome-remote-mcp-servers | https://github.com/punkpeye/awesome-remote-mcp-servers/pull/4785 | Submitted; PR #4785 open, mergeable, labels endpoint-ok and has-connector, no review or comments | Yes: the PR entry points at https://soulintime.com/functions/mcp | 2026-11-16 |
| MCP.Directory | https://mcp.directory/submit | Pending: in their review queue ("already been submitted"); no listing page yet (404) | n/a until listed | 2026-11-16 |
| PulseMCP | https://www.pulsemcp.com/servers?q=soulintime | Not listed (0 results). Submissions and listing changes still paused ("while we rework how we ingest"); they ingest the Official MCP Registry. Nothing to submit | n/a | 2026-11-16 |
| awesome-mcp-servers | https://github.com/punkpeye/awesome-mcp-servers | Not submitted: its CI needs a Glama server page, which would need a Glama claim (not done) | n/a | 2026-11-16 |
| Smithery | https://smithery.ai | Not listed; publishing needs a Smithery account (not used) | n/a | 2026-11-16 |

Directories: 4 listed (Registry, mcpservers.org, Glama, mcp.so), 2 pending (PR #4785, MCP.Directory).

Agent test: [AGENT_TEST.md](AGENT_TEST.md). Framework hook: [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md). People: https://soulintime.com/check
