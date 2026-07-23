# AI Spend Analysis — User Guide

Turn your organization's Anthropic / Claude spend into a clear **person →
department → product → model** dashboard, refreshed monthly. This guide is for the
person running it — no coding required. You talk to Claude in plain English; it
does the work.

> **What it will and won't do.** It's **read-only** on your seats, billing, and org
> settings — it never changes them. It **never sends anything** — every output is a
> file you review, including the Slack summary (which is a *draft* you send
> yourself). It covers Anthropic/Claude spend only (other vendors are on the
> roadmap).

---

## The big idea: three separate pools of money

Most "what are we spending on AI?" confusion comes from mashing three different
things into one number. This tool keeps them distinct everywhere:

| Surface | What it is | Where it comes from |
|---|---|---|
| **A — Committed seats** | The fixed monthly cost of your seats, whether or not they're used | Your roster × seat prices |
| **B — Seat overage** | Usage *beyond* what a seat's allotment covers | Your monthly claude.ai spend export |
| **C — API / Console** | Developer-platform usage, billed as cash, unrelated to seats | The Anthropic Admin API (needs a key) |

A heavy user who stays inside their seat allotment shows **$0 overage but lots of
tokens** — that's correct, not a gap.

---

## Before you start

- **A Claude for Work org** (Team or Enterprise) and **admin/owner access** — the
  spend data is admin-only.
- **The skill installed** in your Claude workspace (see the repository's README for
  install steps).
- **Excel files are optional.** You always get the interactive dashboard and the
  Slack draft. To also get the two `.xlsx` workbooks, the Python library `openpyxl`
  must be available (`pip install openpyxl`). On the web/Cowork this is usually
  already there; on a local machine you may need to install it once.

---

## Getting started (first run)

Just ask, in plain English:

> "Set up AI spend tracking."  *(or run `/ai-spend-analysis`)*

Claude walks you through a short, friendly setup — you mostly **confirm**, you
don't fill out forms:

1. **Where to keep your data.** Claude proposes a folder (e.g.
   `~/Desktop/AI-Spend-Analytics`). Pick somewhere easy to find and **outside any
   code repository** — it will hold real per-person spend. Claude locks it down so
   the data can't be committed to version control.
2. **A few basics.** Your company name (for the dashboard title), your plan
   (**Team** or **Enterprise**), and your seat prices (e.g. standard $30, premium
   $150). The Organization ID is **optional** — you can skip it.
3. **Your roster comes later, automatically** — see below. No need to prepare one.

---

## The one manual step: your monthly spend export

This is the only thing Claude can't fetch for you on the Team plan (it lives behind
a button in your account):

1. Go to **claude.ai → Settings → Analytics**.
2. Find **"How much is Claude costing?"** → **Export spend report** → **Last
   Month**.
3. Save the downloaded CSV into your workspace at
   `raw/<YYYY-MM>/overage_spend.csv` (Claude tells you the exact path). In Cowork,
   you can attach the file to the chat instead.

> **⏳ Don't skip a month.** claude.ai only exports the most recent ~90 days. If you
> miss a month, that data is gone for good — so run this monthly.

**Enterprise plan:** there's no button step — Claude pulls this automatically via
the Analytics API.

---

## Your roster (who's who)

You don't build a roster by hand. On your first run, Claude reads the list of people
straight out of your spend export and creates a **fill-in spreadsheet** at
`config/roster.xlsx`. Open it and:

- type each person's **department**, and
- set **seat_type** using the dropdown (`standard` / `premium`).

That's it — the **dollar amounts fill themselves** from the seat prices you gave
during setup, so there's no money column to touch.

**Don't want to type?** Paste your roster into the chat — even a rough one
("Engineering: ada, alan; Finance: grace; these three are premium") — and Claude
will fill the spreadsheet for you.

The very first dashboard (before you fill the roster) shows everyone under
**"(unmapped)"** — that's expected. Fill the roster and re-run to get real
department and per-person breakdowns.

---

## Optional: tracking API / Console spend (Surface C)

If your organization uses the Anthropic **API or Developer Console** (separate from
Claude seats), you can fold that cash into the dashboard. It needs an **Admin API
key**.

1. At **console.anthropic.com → Settings → Admin keys**, create a key (you must be
   an Organization Owner/Admin). An Admin key is different from a regular API key.
2. In your workspace you'll find a file named **`PASTE_ADMIN_KEY_HERE.txt`**. Open
   it, paste the whole key (it starts with `sk-ant-…`) on the line at the bottom,
   and save.
3. Next run, Claude moves the key into a locked-down, hidden `.secrets/` folder and
   **deletes the paste file**. Your key is never written to chat, logs, the
   workbook, or the dashboard.

> **🔒 Never paste your key directly into the chat.** Use the file. If a key ever
> ends up in a conversation, treat it as compromised and rotate it at
> console.anthropic.com.

No key? No problem — the dashboard simply shows **"Surface C not configured."**

> **Cowork note:** Claude on the web doesn't have a secure secrets store yet, and
> file uploads may be retained. For now, the cleanest way to include Surface C is to
> run it from a local session; on the web, it's fine to leave Surface C off.
> Surfaces A and B need no key and work everywhere.

---

## Monthly refresh

Each month, drop in the new export and say:

> "Refresh the AI spend dashboard."

Claude pulls everything, rebuilds the workbooks and dashboard, and writes a fresh
Slack draft. New hires or seat changes? Just update your roster spreadsheet — the
rest regenerates automatically.

---

## Reading your dashboard

Open `artifacts/<YYYY-MM>_ai_spend.html` in any browser (it's a single self-contained
file — no internet needed).

- **Trend chart** keeps the three surfaces color-coded and separate.
- **Partial month** (you exported before the month ended) is marked, with a dashed
  run-rate forecast that disappears once the full month lands.
- **Quick-win flags** highlight things worth a look:
  - *reclaim candidate* — a barely-used seat you could drop
  - *premium underutilized* — a premium seat that could go standard
  - *consistent overage* — someone consistently over their allotment (check for
    runaway automation)
  - *product spike* — a product's spend jumped month-over-month
  - *unowned API key* — API spend from a key with no owner (fill
    `config/api_key_map.csv` to attribute it)
- **Routing what-if** estimates savings from shifting frontier-model traffic to a
  cheaper model. It's a *model, not advice* — it doesn't judge quality.

---

## Privacy & security

- **Admin-only.** The dashboard and workbooks name individuals and their spend.
  Decide who can see them before you share, and treat inputs and outputs as
  admin-only.
- **Your data stays yours.** Everything lives in your local workspace folder, which
  is gitignored. Nothing is uploaded or sent anywhere by the skill.
- **Keys are protected.** API keys live only in environment variables or the hidden
  `.secrets/` folder — never in config, workbooks, the dashboard, logs, or chat.
- **Nothing is auto-sent.** The Slack summary is a `.txt` draft. You send it.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Dashboard shows a **"Surface B missing"** banner | The export didn't land — re-export from claude.ai and drop it at `raw/<YYYY-MM>/overage_spend.csv`. |
| **No `.xlsx` workbooks** (but dashboard is fine) | Install openpyxl: `pip install openpyxl`, then refresh. |
| Everyone shows as **"(unmapped)"** | Fill in departments in `config/roster.xlsx` and re-run. |
| API spend all lands in an **"unassigned"** bucket | Map keys to owners in `config/api_key_map.csv`. |
| **Surface C says "not configured"** | Add an Admin key via `PASTE_ADMIN_KEY_HERE.txt` (optional). |
| Your key **wasn't picked up** | Make sure you pasted it into `PASTE_ADMIN_KEY_HERE.txt` and saved, then re-run. |

---

*Unofficial — not affiliated with or endorsed by Anthropic. Provided as-is. The
deeper "why" behind the design lives in [`references/dashboard-guide.md`](references/dashboard-guide.md); the operational runbook is [`SKILL.md`](SKILL.md).*
