---
title: First-Session Guide
---

# First-Session Guide

This guide walks you from install to first useful output.

The goal of your first session is to create a usable `finance-profile.md`, review the initial account map, and run at least one finance workflow that uses your company's context.

## Before You Start

You will need:

- access to **Claude Cowork**;
- access to the finance systems you want to connect;
- permission to authenticate those systems;
- one finance artifact or business description, if available.

For a cautious beta test, use sandbox or test-company data first — see [Data Handling and Security](data-handling-security.md).

## Install The Plugin

The plugin installs from inside **Claude Cowork** — there is no command line. You add the airCFO marketplace once, then install the plugin from it.

1. Open Claude Cowork (in the Claude desktop app, select the **Cowork** tab from the mode selector at the top).
2. Click **Customize** in the left sidebar, then **Browse plugins**.
3. Select **Personal**, click the **+** button, and choose **Add marketplace from GitHub**.
4. Enter the repository URL: `https://github.com/aircfo/claude-startup-finance`
5. The **startup-finance** plugin appears in the marketplace — click **Install**. It activates automatically.

Then begin setup:

```text
/finance-context-builder
```

You can also just ask — "set up the finance plugin." Type **/** or click **+** in Cowork anytime to see every skill the plugin adds.

> **First, open a working folder in Cowork.** Before you run the skill, use the *"Work in a folder"* control in your Cowork session and pick (or create) a folder Claude can read and write. That folder is where your Finance Context gets saved. If you skip this, Claude may finish the setup but be unable to save the output.

## Step 1: Confirm The Finance Context Folder

Claude will propose a folder, usually:

```text
~/Desktop/airCFO Finance Context/
```

This folder is where the plugin stores your finance context files.

Expected files:

- `finance-profile.md`
- `account-map.csv`
- `context/`
- `CHANGELOG.md`

Use a location that is easy for your team to find and safe for your company's data policies.

After you confirm the location, the builder saves a small **pointer** so future finance workflows can find this folder without loading your whole profile into every session. It may also ask permission to add a short note to your workspace configuration — say yes or no; either way the pointer keeps things working, and the full profile is never loaded into every session.

## Step 2: Connect Systems

The plugin works best with:

- QuickBooks for accounting and chart of accounts;
- Stripe for customers, subscriptions, and payment activity;
- Ramp for card spend and vendor activity;
- Mercury for cash balances and bank accounts.

On the first run, `/finance-context-builder` checks all four connectors up front, so you may see several browser sign-in prompts in a row. Authorize the systems you use and decline the rest — declining is expected and never blocks setup.

You do not need all four. The minimum useful setup is **QuickBooks plus at least one of Stripe, Ramp, or Mercury**. Missing systems become placeholders and open questions rather than guesses.

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

Claude will draft `account-map.csv` from QuickBooks.

You will review:

- P&L reporting groupings;
- OpEx department classifications;
- COGS vs. operating expense calls;
- cash-flow mapping for balance-sheet accounts;
- account descriptions Claude wrote where QuickBooks did not have one.

Do not worry about making it perfect on the first pass. The goal is to confirm obvious mappings and flag anything uncertain.

## Step 5: Finalize The Finance Profile

Claude will draft `finance-profile.md` from:

- your shared context;
- connected systems;
- the account map;
- discovered money-flow mappings.

Some sections may contain placeholders. That is expected.

Placeholders are a product feature: they show where Claude does not know enough yet. Leave them in place rather than accepting a guess.

## Step 6: Run Your First Workflow

Try one:

```text
What is our runway?
```

Then try:

```text
Give me board metrics for last month.
```

Claude should use the finance profile before pulling numbers.

## What Good Looks Like

After a successful first session, you should have:

- a Finance Context folder in the location you approved;
- a first version of `finance-profile.md`;
- a first version of `account-map.csv`;
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

If auth otherwise fails:

- confirm the connector account is accessible in your browser;
- retry the workflow that invoked the connector;
- use sandbox data if production auth is blocked.

If the profile cannot be found:

- point Claude to the Finance Context folder;
- rerun `/finance-context-builder` to refresh the pointer;
- confirm the file exists at `~/Desktop/airCFO Finance Context/finance-profile.md` or your chosen folder.

If an output feels wrong:

- ask Claude to show the source of each number;
- check the account map;
- email the issue to alex@aircfo.com.

## Next Step

Try the prompts in [Use Cases](use-cases.md).
