---
title: Runway & burn
theme: cash-and-runway
order: 1
summary: Net monthly burn, months of runway, and an estimated cash-out date, from your bank's complete cash flows, with Ramp explaining what's driving the number.
plugin: all-systems-go
skill: runway-and-burn
ask: What's our runway?
reads: [Mercury, Ramp, Stripe]
needs_finance_brain: true
time: A minute or two per run
---

## What you get

1. **A headline:** "≈ X months of runway (net burn ≈ $Y/mo, cash ≈ $Z as of <date>)."
2. **A monthly table** of outflows, inflows, and net burn, so you can check the math.
3. **The trend and its drivers:** is burn rising or falling, and which vendors or categories
   are moving it.
4. **Caveats:** one-time items, excluded accounts, cash vs. accrual.

## How it calculates

- **The bank is the source of truth for burn.** Mercury sees every dollar out: payroll,
  taxes, card settlements, wires. Card spend alone understates burn, often badly, so Ramp is
  used to *explain* the burn, never to total it.
- **Your definitions come from your Finance Brain:** which accounts count as runway cash, which
  transfers are internal, how you define burn.
- **Trailing three full months** by default. Net burn is outflows minus inflows, and runway
  is current cash divided by net burn.
- The arithmetic runs in a computation step, never by eye, and every number shows its work.

## Try asking

```text
Use the trailing three full months and show the monthly burn table.
```

```text
Why did burn change this month?
```
