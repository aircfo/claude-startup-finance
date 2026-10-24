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

**Who you'll need.** Setup touches three systems, and each has its own admin.
If that's not all you, line these people up first; Claude will tell you
exactly what to ask each of them, and you can keep going while you wait.

| Who | What they do | How long |
|---|---|---|
| A **claude.ai Owner** (Primary Owner or Owner) | Sign the daily export in once, in a window that opens on your computer; tell you the organization id | 2 minutes |
| Your **Console admin** (platform.claude.com) | Create an Admin API key and paste it into a file in your workspace | 3 minutes. Optional: only for API cost and the Claude Code report |
| Your **Ramp admin** | Connect Anthropic in Ramp's AI-spend settings, using a key from the *same* Console organization | 5 minutes. Optional: only if you use Ramp |
| **You** | Everything else | About 30 minutes, plus filling in departments |

**What to have ready:** your seat prices (claude.ai → Settings → Billing), and
an export of your company roster from HR or payroll (a spreadsheet with names
and departments; emails help).

**On your computer:** the skill installed (see the repository's README), Python
3.9 or newer, [uv](https://docs.astral.sh/uv/), and Google Chrome. The Excel
workbooks are optional; everything else works without them.

---

## Getting started

Ask, in plain English:

> "Set up AI spend tracking."  *(or run `/ai-spend-analysis`)*

Claude runs a **checkup** (the "doctor") that looks at everything setup needs
and tells you the one next thing to do, who can do it, and how. You do that
step, the checkup runs again, and so on until everything is green. You mostly
confirm; there are no forms.

**You can stop at any time.** Setup picks up where you left off: the checkup
works out where you are from your workspace, so nothing is lost if you close
the chat, wait on someone, or come back next week. Just ask again.

What the checkup will walk you through, in order:

1. A folder for your data, **outside any code repository** (it holds real
   per-person spend).
2. Your company name and seat prices.
3. The organization id and the export sign-in (a claude.ai Owner).
4. Optionally, the Admin key (Console admin) and Ramp (Ramp admin).
5. Your first spend export, and your roster from it.
6. The dashboard, and the daily refresh.

To run the checkup yourself at any point: ask Claude "check my AI spend
setup", or run `python3 <skill folder>/scripts/doctor.py <your workspace>`.

---

## Your spend export

With the daily refresh set up, this happens automatically every morning (a small
script fetches it with the sign-in your Owner did once). Without it, or as a
fallback, it's one manual step a month:

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

**Don't want to type?** Give Claude your HR or payroll export and tell it who
has premium seats. It matches each person's claude.ai email to your roster by
email or name, prefers current employees over old entries, and **asks you
about anyone it isn't sure of** (two people with the same first name, someone
not on the HR list) instead of guessing. A rough list pasted into the chat
works too.

The very first dashboard (before you fill the roster) shows everyone under
**"(unmapped)"** — that's expected. Fill the roster and re-run to get real
department and per-person breakdowns.

---

## Optional: tracking API / Console spend (Surface C)

If your organization uses the Anthropic **API or Developer Console** (separate from
Claude seats), you can fold that cash into the dashboard. It needs an **Admin API
key**.

1. At **platform.claude.com → Settings → Admin keys**, create a key (you must be
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

## Optional: a daily dashboard your team can open

Instead of a file you open once a month, you can keep a **Claude Dashboard**
current every morning and share its link with your team. Ask Claude to "set up
a daily AI spend dashboard for my team" and it walks you through it.

How it stays current:

- **A cloud job** refreshes your API (Console) cost from Ramp each morning. It
  holds no passwords or keys and touches no individual's data.
- **A job on your Mac** pulls the claude.ai spend export each morning with a
  small fixed script (no AI involved) that uses its own Chrome profile, which
  you sign into claude.ai once. It also picks up your Ramp card charges at
  Anthropic. It needs your Mac to be awake at some point in the morning; if it
  isn't, those sections show their age and catch up next time.

Before you share it, decide what your team should see. The default shows
departments only, with no names. You can choose per-person detail instead, but
anyone you share the link with can download every row, so make that a
deliberate decision.

Claude proposes both scheduled jobs and creates them only after you say yes.
The full runbook is in [`references/daily-refresh.md`](references/daily-refresh.md).

---

## Privacy & security

- **Admin-only.** The dashboard and workbooks name individuals and their spend.
  Decide who can see them before you share, and treat inputs and outputs as
  admin-only.
- **Your data stays yours.** Everything lives in your local workspace folder, which
  is gitignored. Nothing leaves it unless you set up the daily dashboard, and
  then only the datasets that your visibility setting allows (departments only,
  by default).
- **Keys are protected.** API keys live only in environment variables or the hidden
  `.secrets/` folder — never in config, workbooks, the dashboard, logs, or chat.
- **Nothing is auto-sent.** The Slack summary is a `.txt` draft. You send it.

---

## Removing it

Ask Claude to "remove the AI spend setup from this Mac", or run
`python3 <skill folder>/scripts/uninstall.py <your workspace>`. It lists what it
would remove and does nothing until you confirm. By default it removes only the
daily job; you choose separately whether to remove the saved claude.ai sign-in,
the Admin key (revoke it in platform.claude.com too), and the spend history.
The dashboard itself is deleted from its menu on claude.ai.

For your IT or security team, [`references/security-overview.md`](references/security-overview.md)
is a one-page summary of what this reads, stores and shares.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| Dashboard shows a **"Surface B missing"** banner | The export didn't land — re-export from claude.ai and drop it at `raw/<YYYY-MM>/overage_spend.csv`. |
| **No `.xlsx` workbooks** (but dashboard is fine) | Install openpyxl: `pip install openpyxl`, then refresh. |
| Everyone shows as **"(unmapped)"** | Fill in departments in `config/roster.xlsx` and re-run. |
| API spend all lands in an **"unassigned"** bucket | Map keys to owners in `config/api_key_map.csv`. |
| **Surface C says "not configured"** | Add an Admin key via `PASTE_ADMIN_KEY_HERE.txt` (optional). |
| Dashboard says **"claude.ai session signed out"** | The export script's login expired. Ask Claude to "sign the AI spend export back in to claude.ai" (it reopens the sign-in window); the next run recovers the whole month. |
| Dashboard sections say they're **stale** | The Mac job hasn't run (Mac off or asleep all morning). It catches up on the next run. |
| **Claude Code tab shows only API keys**, no people | Your Admin key belongs to a different organization than your claude.ai Team workspace. Per-person detail comes from the spend export instead. |
| Your key **wasn't picked up** | Make sure you pasted it into `PASTE_ADMIN_KEY_HERE.txt` and saved, then re-run. |

---

*Unofficial — not affiliated with or endorsed by Anthropic. Provided as-is. The
deeper "why" behind the design lives in [`references/dashboard-guide.md`](references/dashboard-guide.md); the operational runbook is [`SKILL.md`](SKILL.md).*
