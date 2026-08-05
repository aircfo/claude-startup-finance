---
title: Build Your ContextOS
---

<div class="hero" markdown="0">
  <p class="eyebrow">Claude Cowork plugins by airCFO</p>
  <h1>Build your ContextOS.</h1>
  <p class="lede">Claude can already read your finance systems. A <strong>ContextOS</strong> teaches it what your numbers <em>mean</em> — your definitions of burn, runway, and MRR; how your accounts map into reporting; the judgment calls your team carries in its head. Built once from QuickBooks in a guided session, proven against your live books, reused by every finance conversation after.</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="first-session-guide.html">Get started</a>
    <a class="btn btn-secondary" href="https://github.com/aircfo/claude-startup-finance">View on GitHub</a>
  </div>
</div>

<p class="credibility" markdown="0">Built by <a href="https://aircfo.com">airCFO</a>, the AI-enabled back-office growth partner for startups — the same context model our team runs on our own books.</p>

## The problem

Finance analysis breaks when the model doesn't know your company's definitions:

- Which bank accounts count as cash for runway?
- Does treasury count as available runway cash?
- Is Stripe MRR the same definition you use in the board deck?
- Which vendors are COGS instead of G&A?
- Which QuickBooks accounts roll into each management reporting line?
- Which one-time costs should be excluded from run-rate burn?

Those answers rarely live cleanly in one system. They live in board decks, close checklists, reporting packages, spreadsheets, and CFO judgment. Without them, every AI answer is a generic answer.

## How it works

<div class="card-grid" markdown="0">
  <div class="card">
    <span class="step-no">1</span>
    <h3>Connect QuickBooks</h3>
    <p>Install the <code>finance-contextos</code> plugin — one connector, authorized with your own QuickBooks login, read-only. That's the whole first-run surface: one sign-in pop-up.</p>
  </div>
  <div class="card">
    <span class="step-no">2</span>
    <h3>Build the ContextOS</h3>
    <p>A guided ~20-minute session drafts your account map from QuickBooks, reads whatever you share about the business, and writes a durable <code>finance-profile.md</code>. You review only the judgment calls.</p>
  </div>
  <div class="card">
    <span class="step-no">3</span>
    <h3>Prove it ties</h3>
    <p>A ContextOS isn't done until it ties — cash to the bank, revenue to the books, to the penny. Differences become open questions, never silent assumptions. Then every finance conversation starts from your definitions.</p>
  </div>
</div>

## What you get

**A ContextOS that persists.** The build produces a folder you own and can open anytime:

- `finance-profile.md` — Claude's operating manual for your finance function: KPI definitions, cash and burn rules, source-of-truth mappings, known exceptions. [How it works →](finance-profile-explainer.md)
- `account-map.csv` — every QuickBooks account, classified for management reporting and cash-flow mapping, editable in any spreadsheet. Rows you confirm are never overwritten by a refresh.

**Then grow it.** A second plugin, **`all-systems-go`** — named for airCFO's *All Systems Go* series on the startup back-office stack — adds Stripe, Ramp, and Mercury connectors plus workflows that read your ContextOS first:

- **Runway & burn** — complete bank flows from Mercury, spend drivers explained by Ramp.
- **Board metrics** — ARR/MRR, cash, burn, runway, and AR/AP aging in one paste-ready summary.
- **Revenue reconciliation** — an explicit bridge from Stripe gross to QuickBooks recognized revenue.
- **Build your own** — meta-skills that turn a workflow you just ran into a reusable skill of your own.

See [Use Cases](use-cases.md) for prompts to try.

## Read-only by design

The plugins read your systems; they never write to them. No journal entries, no subscription changes, no writeback of any kind. Outputs are analysis for human review — placeholders and open questions mark what the model doesn't know, instead of fake certainty.

The QuickBooks connector is operated by airCFO, open source (MIT), and documented in full — what it stores, where it runs, and who can touch your data: [Data Handling and Security](data-handling-security.md). Prefer not to route through our server? [Self-host it](self-hosting.md).

## Install

You'll need **Claude Cowork** (the Cowork tab in the Claude desktop app, on Pro, Max, Team, or Enterprise plans). The plugins install from inside Cowork — no command line.

1. Open Claude Cowork, click **Customize** in the left sidebar, then **Browse plugins**.
2. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
3. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
4. Click **Install** on the **finance-contextos** plugin. (Add **all-systems-go** now or later.)

Then, in a Cowork session:

```text
build my ContextOS
```

The [First-Session Guide](first-session-guide.md) walks through the whole thing.

> **Upgrading from the old `startup-finance` plugin?** It split into `finance-contextos` (QuickBooks + the context builder) and `all-systems-go` (everything else). Uninstall the old plugin, update the marketplace, install the new ones — your existing context folder keeps working unchanged.

## Early access

<p class="section-note" markdown="0">The plugins are in early access. They're best for teams on QuickBooks Online — and for finance leaders comfortable reviewing AI-drafted mappings before relying on them. Read the <a href="beta-tester-brief.html">Early Access Brief</a> and <a href="known-limitations.html">Known Limitations</a>, and send feedback to <a href="mailto:alex@aircfo.com">alex@aircfo.com</a>.</p>

## Documentation

1. [Early Access Brief](beta-tester-brief.md) — what you're testing and what good feedback looks like.
2. [Data Handling and Security](data-handling-security.md) — read before you connect anything.
3. [First-Session Guide](first-session-guide.md) — install to first useful output.
4. [What is a ContextOS?](finance-profile-explainer.md) — how the context model works.
5. [Self-Hosting the QuickBooks Connector](self-hosting.md) — run it on your own infrastructure.
6. [Use Cases](use-cases.md) — prompts to try.
7. [Known Limitations](known-limitations.md) — the honest list.
