---
title: Data Handling And Security
---

# Data Handling And Security

Finance tools require trust. This page explains what the Finance Brain Starter Kit and the
tools in this library access, what they write, and what to avoid storing.

This is a plain-English guide. It is not legal advice. Confirm your company's internal data
policies before connecting production systems.

## Where Your Data Lives

**The Finance Brain is a folder on your machine.** It's plain markdown (plus the workpapers you
save there). airCFO never sees it: nothing in the kit sends it anywhere. You decide where it
lives and who it's shared with, for example a private Git repository or a shared drive with
your team's normal permissions.

**Connectors are the vendors' own.** Stripe, Ramp, and Mercury connect through each vendor's own
remote connector, bundled in the `all-systems-go` plugin. QuickBooks connects through a
QuickBooks connector you add in Claude's connector settings, such as Intuit's. You authorize
each one with your own login, directly with that vendor. airCFO runs no server in between and
never holds your tokens or your data.

**Claude sees what it reads.** When a skill or tool reads a connected system, that data goes
into your own Claude conversation to produce the answer. How Anthropic handles it is governed
by the terms of your Claude account and workspace settings.

## Read-Only Product Intent

Everything here is designed for read-only finance work. The kit's skills and the tools read your systems
and prepare workpapers, analysis, and import files. They never post journal entries, pay,
transfer, or edit records. A person reviews and posts.

Some connectors offer write access. The kit's rules and every tool's instructions tell Claude
not to use it. If Claude ever proposes a write action, stop and review before proceeding.

## What Gets Written

- **The kit** writes only inside its own folder: handbook pages, workpapers in `testing/` or
  your close folder, and the changelog in `CLAUDE.md`. It never deletes or moves files you put
  there.
- **The tools** write nothing by default. Their outputs appear in your conversation unless you
  ask Claude to save them.

These files can hold sensitive business context: account names, vendor names, reporting
definitions, and judgment calls. Store them according to your company's data policies.

## What Not To Store

Do not put any of these in your Finance Brain or in documents you share with Claude:

- API keys, OAuth tokens, or passwords;
- full bank or card numbers (last four digits only);
- sensitive personal employee data;
- customer personal data the work doesn't need.

## What If A Connector Is Missing?

Nothing breaks. The kit marks the gap as a placeholder and asks for the specific export it
needs. Tools skip what they can't read and list it as an open question:

```text
[PLACEHOLDER: Ramp is not connected, so card spend by vendor still needs an export.]
```

That's preferable to Claude guessing.

## Human Review Required

Review outputs before they're used in board materials, investor updates, audit support, lender
reporting, or operational decisions. The kit builds this in: the person who runs a skill
never approves its output.

**Security or privacy questions:** email **alex@aircfo.com** with "Security" in the subject
line.
