# Indexes

Where agents and tools can find SoulInTime. Checked weekly (Mondays). Every "listed" URL must resolve; a broken one is fixed or removed the same day.

Every listing should match [AGENT_CARD.md](AGENT_CARD.md) where it shows our text. The read-only check every listing should carry:

```sh
curl -s "https://soulintime.com/functions/v1Verify?hash=019bd3056ae35f6eee3f61fcabdaabcfe5f374c07168a7e4d6fa38a828cbac2f"
```

| Index | URL | Status | Matches AGENT_CARD.md | Checked |
|---|---|---|---|---|
| OpenTimestamps members list | https://opentimestamps.org/ | Listed: logo and name "SoulInTime" linking to https://soulintime.com (PR https://github.com/opentimestamps/opentimestamps.org/pull/89 merged 2026-11-17 10:29 IST by RCasatta) | n/a (logo and link only, no card text) | 2026-11-17 |
| Official MCP Registry | https://registry.modelcontextprotocol.io/v0.1/servers/io.github.MorrisMoe%2Fsoulintime/versions/latest | Listed (`io.github.MorrisMoe/soulintime` 0.1.1, active, remote https://soulintime.com/functions/mcp). Description (max 100 characters): "Sealed 019bd305… @ block 965906. Verify." Changing it needs a republish with a login, so unchanged | Yes, as far as it goes: Door hash, block 965906 and the MCP URL match; too short to hold the card | 2026-11-16 |
| mcpservers.org | https://mcpservers.org/servers/soulintime/soulintime-client | Listed; still renders an earlier snapshot of this README ("Last verified: 2026-11-12"). Their login-free "Request update" (refresh documentation) button was pressed once on 2026-11-16 | Partly: Door curl, block 965906 and MCP URL match; the card block is not in their snapshot yet. Recheck next Monday | 2026-11-16 |
| Glama (connector) | https://glama.ai/mcp/connectors/io.github.MorrisMoe/soulintime | Listed; Healthy (unclaimed listing; not claimed) | Partly: shows the 15-line card from before 2026-11-16 14:11 IST; the wait line added then is not in their copy yet (it reaches them through the MCP verify description on their next crawl) | 2026-11-16 |
| mcp.so | https://mcp.so/servers/soulintime-client | Listed (picked up from GitHub; nothing submitted). Older repo description, "No standard config provided"; not recrawled to the card. Editing or submitting needs a Sign In and its submit is a $39 paid listing; not used | Partly: Door hash, block and MCP URL match; older text | 2026-11-16 |
| awesome-remote-mcp-servers | https://github.com/punkpeye/awesome-remote-mcp-servers/pull/4785 | Submitted; PR #4785 open, mergeable, labels endpoint-ok and has-connector, no review or comments (last update 2026-11-15) | Yes: the PR entry points at https://soulintime.com/functions/mcp | 2026-11-16 |
| MCP.Directory | https://mcp.directory/submit | Pending: in their review queue ("already been submitted"); no listing page yet (404) | n/a until listed | 2026-11-16 |
| PulseMCP | https://www.pulsemcp.com/servers?q=soulintime | Not listed (0 results). Submissions and listing changes still paused ("while we rework how we ingest"); they ingest the Official MCP Registry. Nothing to submit | n/a | 2026-11-16 |
| awesome-mcp-servers | https://github.com/punkpeye/awesome-mcp-servers | Not submitted: its CI needs a Glama server page, which would need a Glama claim (not done) | n/a | 2026-11-16 |
| Smithery | https://smithery.ai | Not listed; publishing needs a Smithery account (not used) | n/a | 2026-11-16 |

Directories: 4 listed (Registry, mcpservers.org, Glama, mcp.so), 2 pending (PR #4785, MCP.Directory).

Agent test: [AGENT_TEST.md](AGENT_TEST.md). Framework hook: [FRAMEWORK_NOTE.md](FRAMEWORK_NOTE.md). People: https://soulintime.com/check
