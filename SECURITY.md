# Security policy

This project connects Claude to real accounting, banking, payments, and spend systems. We
take reports seriously and would rather hear about a problem early and informally than not
at all.

## Reporting a vulnerability

**Email [alex@aircfo.com](mailto:alex@aircfo.com) with the subject line
`SECURITY: claude-startup-finance`. Please do not open a public issue** for anything that
could expose someone's financial data or credentials.

Useful to include, as much as you have:

- What you found and the impact you think it has.
- The steps to reproduce it, and which plugin, skill, or connector is involved.
- Whether it affects the airCFO-hosted QuickBooks MCP server, a self-hosted deployment, or
  only the skills in this repository.

What to expect: an acknowledgment within three business days, and a fix or a plan with
timing once we've reproduced it. We'll credit you in the release notes if you'd like, or keep
you anonymous if you'd prefer. There is no bug-bounty program — this is a small team
shipping in public.

## Never paste secrets or real financial data

**Do not put API keys, OAuth tokens, client secrets, access tokens, account numbers, or real
financial or customer data into a GitHub issue, discussion, pull request, or commit** — in
this repository or any other. Issues and pull requests are public and permanently indexed,
and commit history survives a later deletion.

If you need to show a number or a payload to explain a bug, redact it or replace it with a
synthetic equivalent. Fixtures committed here are synthetic and must stay that way.

**If you believe you've already committed or posted a credential:** treat it as compromised.
Revoke and rotate it at the source (QuickBooks, Stripe, Ramp, Mercury, or Anthropic) first,
then email us — rotating comes before cleaning up the history.

## How this project is designed to limit risk

- **Read-only wherever it touches money.** The connectors ship without write tools, so the
  skills here can read your books and change nothing.
- **Per-user OAuth.** You authenticate into your own accounts in your own browser. This
  repository contains no keys or tokens, and airCFO never holds a shared credential to your
  systems.
- **No server-side storage of financial data.** The airCFO-operated QuickBooks MCP server
  fetches your data live per question and does not retain it. It keeps only encrypted
  connection tokens (AES-256-GCM), your company name, and your sign-up email. Say
  "disconnect QuickBooks" to revoke and erase.
- **Self-hosting is supported.** If you'd rather your books never touch airCFO
  infrastructure, run the same MIT-licensed server yourself:
  [`aircfo/qbo-mcp`](https://github.com/aircfo/qbo-mcp) ·
  [deploy guide](https://aircfo.github.io/claude-startup-finance/self-hosting.html).
- **Local files stay where you approve them.** Skills write to the ContextOS folder you
  choose, plus a small pointer file with your consent.
- **Evaluate with a sandbox.** Not ready to authorize production data? Point the QuickBooks
  connector at a sandbox company first.

Full detail, including exactly what each connector can read:
[docs/data-handling-security.md](docs/data-handling-security.md).

## Scope

This policy covers the plugins, skills, and manifests in this repository, and the
airCFO-operated QuickBooks MCP server they connect to (source:
[`aircfo/qbo-mcp`](https://github.com/aircfo/qbo-mcp)).

Vulnerabilities in QuickBooks, Stripe, Ramp, Mercury, Claude, or Claude Cowork themselves
belong to those vendors — this project is unofficial and not affiliated with any of them.
Please report those through the vendor's own security channel. If you're unsure which side a
problem sits on, email us and we'll help route it.
