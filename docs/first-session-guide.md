---
title: First-Session Guide
---

# First-Session Guide

This guide walks you from install to first useful output.

The goal of your first session is to build your **ContextOS** — a usable `finance-profile.md` and a reviewed account map — and see it verified against your live books.

## Before You Start

You will need:

- access to **Claude Cowork**;
- access to your QuickBooks Online account (and permission to authenticate it);
- one finance artifact or business description, if available.

For a cautious first test, use sandbox or test-company data — see [Data Handling and Security](data-handling-security.md).

## Install The Plugin

The plugin installs from inside **Claude Cowork** — there is no command line. You add the airCFO marketplace once, then install the plugin from it.

1. Open Claude Cowork (in the Claude desktop app, select the **Cowork** tab from the mode selector at the top).
2. Click **Customize** in the left sidebar, then **Browse plugins**.
3. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
4. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
5. Click **Install** on **finance-contextos**. It activates automatically.
   (Optionally also install **all-systems-go** — it adds Stripe/Ramp/Mercury connectors and
   the runway, board-metrics, and reconciliation workflows. You can add it after the build too.)

Then begin:

```text
build my ContextOS
```

You can also run `/finance-context-builder` directly. Type **/** or click **+** in Cowork anytime to see every skill the plugins add.

> **First, open a working folder in Cowork.** Before you run the skill, use the *"Work in a folder"* control in your Cowork session and pick (or create) a folder Claude can read and write. That folder is where your ContextOS gets saved. If you skip this, Claude may finish the setup but be unable to save the output.

## Step 1: Confirm The ContextOS Folder

Claude will propose a folder, usually:

```text
~/Desktop/ContextOS/
```

This folder is where the plugin stores your ContextOS files. (Built one under the older default, `~/Desktop/airCFO Finance Context/`? It keeps working — refreshes find and reuse it.)

Expected files:

- `finance-profile.md`
- `account-map.csv`
- `context/`
- `CHANGELOG.md`

Use a location that is easy for your team to find and safe for your company's data policies.

After you confirm the location, the builder saves a small **pointer** so future finance workflows can find this folder without loading your whole profile into every session. It may also ask permission to add a short note to your workspace configuration — say yes or no; either way the pointer keeps things working, and the full profile is never loaded into every session.

## Step 2: Connect QuickBooks

QuickBooks is the backbone — it's where the account map and most of the profile come from, and it's the only connector `finance-contextos` ships. Expect **one** browser sign-in pop-up: your own QuickBooks login, read-only. Claude confirms the company name it connected to, so a wrong company is caught immediately.

If you've also installed **all-systems-go**, Claude checks its connectors too (Stripe for subscriptions, Ramp for card spend, Mercury for bank balances) — authorize the ones you use and decline the rest; declining is expected and never blocks setup. Missing systems become placeholders and open questions rather than guesses.

> **QuickBooks — connect the airCFO connector, not Intuit's.** This plugin ships its own QuickBooks connector. Claude or Cowork may also offer Intuit's official QuickBooks connector — that is a *different* one and produces weaker results here. Make sure the QuickBooks connection used during setup is the airCFO one that came with the plugin. If a first run gave odd QuickBooks numbers, this is the most likely cause — check the connector and re-run.

> **Some connectors grant only partial access.** Depending on the scope you approve, or your role in that system, a connector may connect but block certain data — for example, Ramp may allow card and vendor data but refuse treasury/checking accounts. That is fine: the skill uses what it can read and marks the rest as open questions.

## Step 3: Share Business Context

Claude will ask what would help it understand your business.

Good inputs include:

- board deck;
- monthly reporting package;
- KPI dashboard;
- month-end close checklist;
- revenue recognition policy;
- a short written explanation of the business model.

You do not need to prepare something formal. A few paragraphs are useful.

Example:

```text
We are a B2B SaaS company. We report ARR, MRR, gross margin, net burn, and runway to the board. We include trialing subscriptions in internal MRR but not in board ARR. We treat customer hosting costs as COGS and exclude one-time legal fees from run-rate burn.
```

## Step 4: Review The Account Map

Claude will draft `account-map.csv` from QuickBooks. Most rows map by rule; you review only the ones Claude marks `needs-review` — typically:

- expense-category calls (what kind of money an account is);
- department calls (which team owns the spend);
- COGS vs. operating expense calls;
- the proposed `mrr` tag set — this defines your P&L-based MRR, so confirm it deliberately;
- cash-flow mapping questions (e.g. a treasury account you may want treated as Investing).

Rows you sign off on are marked `confirmed`, and later refreshes never overwrite them. Do not worry about making it perfect on the first pass. The goal is to confirm obvious mappings and flag anything uncertain.

## Step 5: Finalize The Finance Profile

Claude will draft `finance-profile.md` from:

- your shared context;
- connected systems;
- the account map;
- discovered money-flow mappings.

Some sections may contain placeholders. That is expected.

Placeholders are a product feature: they show where Claude does not know enough yet. Leave them in place rather than accepting a guess.

## Step 6: Watch It Verify (Prove It Ties)

Setup does not end on "here are your files." Claude closes by checking the freshly built context against your live systems — for example:

- Mercury balances tied to the mapped QuickBooks bank accounts;
- last month's revenue re-totaled through the account map, matching the QuickBooks P&L to the penny;
- your runway-cash definition played back as a number you can sanity-check.

You get a short tie-out table. An unexplained difference becomes an open question — finding one is the feature working, not the setup failing.

## Step 7: Run Your First Workflow

The cross-system workflows ship in the **all-systems-go** plugin — install it from the same marketplace if you haven't. Then try one:

```text
What is our runway?
```

Then try:

```text
Give me board metrics for last month.
```

Claude should read your ContextOS before pulling numbers.

## What Good Looks Like

After a successful first session, you should have:

- a ContextOS folder in the location you approved;
- a first version of `finance-profile.md`;
- a first version of `account-map.csv`;
- a tie-out showing the model matches your live systems;
- a list of open questions;
- at least one useful finance workflow output.

## If Something Goes Wrong

If a connector sign-in fails (the connect page will not load, shows "can't connect to the server" or a `localhost` address, or reports an "unavailable scope"):

- make sure you are in the **Claude desktop app with Cowork open** — a browser-only flow cannot always complete the sign-in handshake;
- close the failed sign-in tab and retry the connection once or twice;
- an **"unavailable scope" or permission error** means your account or role cannot grant that data (for example Ramp treasury) — that is not a blocker; the skill continues with what it can read;
- if a connector keeps failing, decline it and connect it later — setup never blocks on one connector.

If QuickBooks output looks wrong:

- confirm the **airCFO** QuickBooks connector was used, not Intuit's built-in one (see Step 2), then re-run;
- if the chart of accounts is large and a pull errors out, ask Claude to "pull the account list in smaller pages."

If a connector that worked before asks you to sign in again:

- connector sessions expire after a few idle days — a re-sign-in prompt on a later run is **normal, not a bug**; authorize and continue.

If auth otherwise fails:

- confirm the connector account is accessible in your browser;
- retry the workflow that invoked the connector;
- use sandbox data if production auth is blocked.

If the profile cannot be found:

- point Claude to the ContextOS folder;
- rerun `/finance-context-builder` to refresh the pointer;
- confirm the file exists at `~/Desktop/ContextOS/finance-profile.md` (or `~/Desktop/airCFO Finance Context/finance-profile.md` for older builds), or your chosen folder.

If an output feels wrong:

- ask Claude to show the source of each number;
- check the account map;
- email the issue to alex@aircfo.com.

## Next Step

Try the prompts in [Prompts to try](use-cases.md), or browse the [tool library](index.md#tools).
