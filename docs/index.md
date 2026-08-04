---
title: Give Claude Your Finance Context Once
---

<div class="hero" markdown="0">
  <p class="eyebrow">A Claude Cowork plugin by airCFO</p>
  <h1>Give Claude your finance context. Once.</h1>
  <p class="lede">Claude can already read your finance systems. This plugin teaches it what your numbers <em>mean</em> — your definitions of burn, runway, and MRR; how your accounts map into reporting; the judgment calls your team carries in its head. Built once, reused by every finance workflow after.</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="first-session-guide.html">Get started</a>
    <a class="btn btn-secondary" href="https://github.com/aircfo/claude-startup-finance">View on GitHub</a>
  </div>
</div>

<p class="credibility" markdown="0">Built by <a href="https://aircfo.com">airCFO</a>, the AI-enabled back-office growth partner for startups — the same context model our team uses on real books.</p>

## The problem

Finance analysis breaks when the model doesn't know your company's definitions:

- Which Mercury accounts count as cash for runway?
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
    <h3>Connect your stack</h3>
    <p>One install wires up Stripe, Ramp, Mercury, and QuickBooks — each authorized with your own login, read-only. Use the ones you have; missing systems become open questions, never guesses.</p>
  </div>
  <div class="card">
    <span class="step-no">2</span>
    <h3>Build the context</h3>
    <p>A guided ~20-minute setup drafts your account map from QuickBooks, reads whatever you share about the business, and writes a durable <code>finance-profile.md</code>. You review only the judgment calls.</p>
  </div>
  <div class="card">
    <span class="step-no">3</span>
    <h3>Verify, then work</h3>
    <p>Setup ends by proving the model ties to your live systems — cash to the bank, revenue to the books. Then every workflow reads the profile first: runway, board metrics, revenue reconciliation, and skills you build yourself.</p>
  </div>
</div>

## What you get

**Four connectors**, authorized per-user with OAuth: QuickBooks, Stripe, Ramp, and Mercury.

**A finance context that persists.** The setup produces a folder you own and can open anytime:

- `finance-profile.md` — Claude's operating manual for your finance function: KPI definitions, cash and burn rules, source-of-truth mappings, known exceptions. [How it works →](finance-profile-explainer.md)
- `account-map.csv` — every QuickBooks account, classified for management reporting and cash-flow mapping, editable in any spreadsheet.

**Workflows that use it:**

- **Runway & burn** — complete bank flows from Mercury, spend drivers explained by Ramp.
- **Board metrics** — ARR/MRR, cash, burn, runway, and AR/AP aging in one paste-ready summary.
- **Revenue reconciliation** — an explicit bridge from Stripe gross to QuickBooks recognized revenue.
- **Build your own** — meta-skills that turn a workflow you just ran into a reusable skill of your own.

See [Use Cases](use-cases.md) for prompts to try.

## Read-only by design

The plugin reads your systems; it never writes to them. No journal entries, no subscription changes, no writeback of any kind. Outputs are analysis for human review — placeholders and open questions mark what the model doesn't know, instead of fake certainty.

The QuickBooks connector is operated by airCFO and documented in full — what it stores, where it runs, and who can touch your data: [Data Handling and Security](data-handling-security.md).

## Install

You'll need **Claude Cowork** (the Cowork tab in the Claude desktop app, on Pro, Max, Team, or Enterprise plans). The plugin installs from inside Cowork — no command line.

1. Open Claude Cowork, click **Customize** in the left sidebar, then **Browse plugins**.
2. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
3. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
4. Click **Install** on the **startup-finance** plugin. It activates automatically.

Then, in a Cowork session, start setup:

```text
/finance-context-builder
```

You can also just ask in plain English — "set up the finance plugin." The [First-Session Guide](first-session-guide.md) walks through the whole thing.

## Early access

<p class="section-note" markdown="0">The plugin is in early access. It's best for teams on QuickBooks plus at least one of Stripe, Ramp, or Mercury — and for finance leaders comfortable reviewing AI-drafted mappings before relying on them. Read the <a href="beta-tester-brief.html">Early Access Brief</a> and <a href="known-limitations.html">Known Limitations</a>, and send feedback to <a href="mailto:alex@aircfo.com">alex@aircfo.com</a>.</p>

## Documentation

1. [Early Access Brief](beta-tester-brief.md) — what you're testing and what good feedback looks like.
2. [Data Handling and Security](data-handling-security.md) — read before you connect anything.
3. [First-Session Guide](first-session-guide.md) — install to first useful output.
4. [The Finance Profile](finance-profile-explainer.md) — how the context model works.
5. [Use Cases](use-cases.md) — prompts to try.
6. [Known Limitations](known-limitations.md) — the honest list.
