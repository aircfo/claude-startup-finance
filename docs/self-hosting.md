---
title: Self-Hosting the QuickBooks Connector
---

# Self-hosting the QuickBooks connector

By default, the `finance-contextos` plugin routes QuickBooks reads through an
airCFO-operated MCP server. If you'd rather your books never touch our
infrastructure, run the same server yourself — it's the identical codebase,
[open source under MIT](https://github.com/aircfo/qbo-mcp), and the plugin works
the same way against your deployment. Same tools, same read-only design, your
infrastructure.

## What you're deploying

[`aircfo/qbo-mcp`](https://github.com/aircfo/qbo-mcp) — a multi-user, remote MCP
server for QuickBooks Online. 41 read-only tools (reports, ledger, search); Intuit
tokens encrypted at rest (AES-256-GCM); your financial data is fetched live per
question and never stored server-side. Read its
[SECURITY.md](https://github.com/aircfo/qbo-mcp/blob/main/SECURITY.md) for the full
posture.

## What you'll need

1. **An Intuit developer app** ([developer.intuit.com](https://developer.intuit.com)) —
   free. You'll create an app, note its Client ID/Secret, and register your server's
   OAuth redirect URI. Production keys require Intuit's self-attested security
   questionnaire (no pen-test or SOC 2 — attestation of secure token storage and
   handling, which this codebase is built to satisfy).
2. **Somewhere to run one container.** The repo ships a Dockerfile and a
   step-by-step [Railway deploy guide](https://github.com/aircfo/qbo-mcp/blob/main/DEPLOY.md)
   (a small instance with a persistent volume is all it takes). Any host that runs
   a Docker container with a persistent disk works.
3. **Ten minutes.** Deploy, set ~7 environment variables, generate a domain.

## Pointing the plugin at your server

The plugin's connector URL lives in one file. Fork (or clone) the
[marketplace repo](https://github.com/aircfo/claude-startup-finance) and edit
`plugins/finance-contextos/.mcp.json`, replacing the `url` with your deployment:

```json
{
  "mcpServers": {
    "aircfo-quickbooks": {
      "type": "http",
      "url": "https://YOUR-DEPLOYMENT.example.com/mcp"
    }
  }
}
```

Then add **your fork** as the marketplace in Cowork (Customize → Browse plugins →
**+** → Add marketplace from GitHub) and install `finance-contextos` from it.
Everything else — the skill, the templates, the build flow — is unchanged.

## Tradeoffs, honestly

- **You own the Intuit relationship**: your own API quota (generous for a single
  company), your own security attestation, your own uptime.
- **You maintain it**: pulling upstream updates to the server and the plugin is on
  you. The server is deliberately small (one process, one SQLite file) to keep
  that cheap.
- **Keep `TOKEN_ENCRYPTION_KEY` stable and the volume backed up** — rotating the
  key or losing the disk means everyone reconnects QuickBooks (annoying, not
  dangerous: no financial data is stored).

Questions: [alex@aircfo.com](mailto:alex@aircfo.com) (subject "Self-hosting").
