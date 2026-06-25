---
title: Data Handling And Security
---

# Data Handling And Security

Finance tools require trust. This page explains what the beta plugin accesses, what it writes to your workspace, and what to avoid sharing — with full detail on the airCFO-operated QuickBooks connector.

This is a plain-English beta guide. It is not legal advice and not a substitute for a published privacy policy or terms of service — both are required before any public, non-gated launch. Confirm your company's internal data policies before connecting production systems.

## What The Plugin Connects To

The plugin can connect Claude to:

- QuickBooks
- Stripe
- Ramp
- Mercury

Authentication is handled through per-user OAuth in your browser as workflows invoke each connector.

## Read-Only Product Intent

The plugin is designed for read-only finance analysis.

Workflow skills should not write to QuickBooks, Stripe, Ramp, or Mercury. They are intended to read data, summarize it, map it into your finance profile, and produce analysis for human review.

If Claude ever proposes a writeback action, stop and review before proceeding.

## What Gets Written To Your Workspace

The plugin creates an airCFO Finance Context folder in a location you approve, usually:

```text
~/Desktop/airCFO Finance Context/
```

That folder may include:

- `finance-profile.md`
- `account-map.csv`
- `context/`
- `CHANGELOG.md`

The builder also saves a small **pointer** so future workflows can find this folder without loading your whole profile every session, and — only with your OK — may add a short note to your workspace configuration. It never writes the full profile into your configuration.

These files may contain sensitive business context: account names, vendor names, reporting definitions, and financial judgment calls. Store the folder according to your company's data policies.

## What Not To Store

Do not place the following in `finance-profile.md`, `account-map.csv`, or shared context docs:

- API keys;
- OAuth tokens;
- passwords;
- full bank account numbers;
- full card numbers;
- sensitive personal employee data;
- customer PII that is not needed for the workflow.

Use names, last-four identifiers, and internal IDs only where needed.

## Connector Note For Beta

Stripe, Ramp, and Mercury use their own configured remote MCP endpoints — you authorize each directly with that vendor.

QuickBooks uses an **airCFO-operated** MCP server during beta. Because that server is run by airCFO (not Intuit), the section below documents exactly what it does and does not do with your data.

If you are not ready to authorize production finance data, use a sandbox or test company file while evaluating the plugin.

## The QuickBooks Connector (Beta): Security And Privacy

The QuickBooks connector is a multi-user, remote MCP server, currently in gated beta. You connect your own QuickBooks Online company through Intuit's OAuth, which gives Claude read-only access to that company's accounting data (P&L, balance sheet, cash flow, general ledger, AR/AP aging, vendor spend, and individual transactions).

*Verified against the connector's source code and deployment on 2026-06-25.*

### The core guarantees

- **Read-only.** No write tools exist. Claude cannot create, edit, delete, or send anything in QuickBooks.
- **Your financial data is not stored.** Your books are fetched live from QuickBooks for each question, returned to Claude to produce the answer, and not persisted in the connector's database. Only your connection tokens and minimal metadata are kept.
- **Per-user isolation.** Each connection can reach only the one company tied to that login — there is no path, accidental or intentional, to another user's data.
- **Self-service disconnect.** You can disconnect anytime; the connector deletes the stored connection and attempts to revoke the Intuit token. You can also revoke the app directly inside your Intuit account.

### Hosting and who touches your data

- **Host:** Railway, US East (Virginia) — a single instance with one persistent, encrypted volume.
- **The only third parties that touch your data:**
  - **Railway** — hosting and compute, plus the encrypted volume that stores connection tokens.
  - **Intuit / QuickBooks Online** — the data source you authorize directly.
  - **Anthropic (Claude)** — receives the QuickBooks data needed to answer your question, inside your own Claude conversation.
- **AI training:** Your data is never used to train any AI model — not by us. It's sent to Claude (Anthropic) only to answer your question; how Anthropic handles it is governed by the terms of your own Claude account and workspace settings.

### Encryption

- **In transit:** TLS/HTTPS on every hop — Claude ↔ connector and connector ↔ QuickBooks. No user data crosses an unencrypted connection.
- **At rest:** Your Intuit access and refresh tokens are encrypted with AES-256-GCM, with the key held in the environment, separate from the database volume. The Claude-to-connector credentials are stored only as SHA-256 hashes.

### Logging

- **What's logged:** one short structured line per request, plus connect/disconnect events — a timestamp, an internal connection ID, the tool name, the response status, latency, and (on connect/disconnect) the email you self-report.
- **What's never logged:** your financial data and your tokens.
- **Retention:** up to 30 days, then rotated out.
- **Access:** limited to airCFO engineering staff with access to the hosting environment.

### Good to know

- The email you enter when connecting is self-reported and unverified — a soft accountability signal, not identity.
- This beta documentation is not legal advice; a published privacy policy and terms of service are still required before any public launch.

**Security or privacy questions:** email **alex@aircfo.com** with "Security" in the subject line.

## What If A Connector Is Missing?

The plugin can continue with partial setup. Missing systems should become placeholders and open questions in the finance profile.

Example:

```text
[PLACEHOLDER: Ramp is not connected, so recurring vendor rules still need to be mapped.]
```

That is preferable to Claude guessing.

## Human Review Required

Outputs should be reviewed before they are used in:

- board materials;
- investor updates;
- audit support;
- lender reporting;
- operational decisions.

The plugin helps gather and interpret context. It does not replace finance judgment.
