---
name: runway-and-burn
description: Calculate a startup's net monthly burn and cash runway by combining bank balances from Mercury with card and bill spend from Ramp, offset by revenue. Use when someone asks "what's our runway," "how many months of cash do we have," "what's our burn rate," "how long until we run out of money," or wants a burn/runway update for fundraising or board prep.
---

# Runway & Burn

Calculate net monthly burn and months of cash runway across the startup's bank and spend accounts.

## When to use this
Trigger when the user asks about runway, burn rate, months of cash, cash-out date, or needs a burn update for a board meeting or fundraise.

## Data to gather
1. **Current cash** — from **Mercury**: sum the available balance across all operating and treasury accounts. This is the numerator for runway.
2. **Cash outflows (spend)** — from **Ramp**: card transactions and paid bills over the trailing window (default: the last 3 full calendar months).
3. **Cash inflows (revenue)** — from **Stripe** (collected payments) and/or **Mercury** deposits over the same window. Use this to compute *net* burn.
   - If the company is pre-revenue, inflows are ~0 and net burn ≈ gross spend.

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
3. One sentence on the trend (burn rising or falling) and the single biggest spend driver if it's obvious from Ramp.
4. Caveats (one-time items, accounts excluded, cash vs. accrual).
