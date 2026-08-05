---
name: runway-and-burn
description: Calculate a startup's net monthly burn and cash runway from Mercury bank flows, offset by revenue, with Ramp explaining the spend drivers. Use when someone asks "what's our runway," "how many months of cash do we have," "what's our burn rate," "how long until we run out of money," or wants a burn/runway update for fundraising or board prep.
---

# Runway & Burn

Calculate net monthly burn and months of cash runway across the startup's bank and spend accounts.

## When to use this
Trigger when the user asks about runway, burn rate, months of cash, cash-out date, or needs a burn update for a board meeting or fundraise.

## Step 0 — Load the finance profile
Read `finance-profile.md` first (the company's semantic map). It tells you which Mercury accounts are operating vs. treasury, which count as cash for runway, what the company treats as an internal transfer (excluded from burn), and the pinned burn definition — so you don't re-derive the topology or guess.

Find the profile in this order:
1. If this session's instructions (e.g. a workspace `CLAUDE.md`) include a **ContextOS** pointer (the bounded block is labeled `airCFO Finance Context` in older installs), use the profile path it names.
2. Else if `.aircfo-finance-context.json` exists in the current workspace, read `financeProfile` from it.
3. Else check the default location: `~/Desktop/ContextOS/finance-profile.md` — then the legacy default `~/Desktop/airCFO Finance Context/finance-profile.md`.
4. Else check the current workspace for `finance-profile.md`.
5. If you still can't find it, run `finance-context-builder` first (or tell the user to). **Do not guess** the operating-vs-treasury split or the internal-transfer exclusions — without the profile they're guesswork.

## Data to gather
1. **Current cash** — from **Mercury**: sum the available balance across the accounts the profile counts as runway cash. This is the numerator for runway.
2. **Cash outflows** — from **Mercury**: every debit out of the operating accounts over the trailing window (default: the last 3 full calendar months), excluding the internal transfers the profile defines. The bank sees *all* cash out — payroll, taxes, card settlements, wires — so this is the only complete measure of gross burn. **Never use Ramp as the outflow total:** payroll and other non-card spend never touch Ramp, so a card-only number understates burn, often badly.
3. **Cash inflows (revenue)** — from **Stripe** (collected payments) and/or **Mercury** deposits over the same window, again excluding internal transfers. Use this to compute *net* burn.
   - If the company is pre-revenue, inflows are ~0 and net burn ≈ gross spend.
4. **Spend drivers** — from **Ramp**: top vendors and categories over the window. This is what Ramp is authoritative for — explaining *what's inside* the burn (the biggest drivers, what changed) — not totaling it.

## Calculation
- Use a trailing window of **3 full calendar months** unless the user asks for a different window.
- **Gross monthly burn** = total outflows over the window ÷ number of months.
- **Net monthly burn** = (total outflows − total inflows) over the window ÷ number of months.
- **Runway (months)** = current cash ÷ net monthly burn.
  - If net burn ≤ 0 (cash-flow positive), say the company is not burning and runway is effectively unlimited at the current trend.
- **Estimated cash-out date** = today + runway months.

## Always
- Use a computation step for the arithmetic — never eyeball aggregates across many transactions.
- Show your work: list the months used, the outflow and inflow totals per month, and the averages, before giving the headline number.
- State the as-of date and exactly which accounts and window are included.

## Output format
1. **Headline**: "≈ X months of runway (net burn ≈ $Y/mo, cash ≈ $Z as of <date>)."
2. A short table: month | outflows | inflows | net burn.
3. One sentence on the trend (burn rising or falling) and the biggest spend drivers from Ramp — name the vendors or categories moving the number.
4. Caveats (one-time items, accounts excluded, cash vs. accrual).

## Never
- Read-only — never write to Mercury, Ramp, Stripe, or QuickBooks.
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
