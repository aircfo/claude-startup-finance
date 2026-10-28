# Chart of accounts

**What this page is for:** how the chart of accounts is organized, so Claude codes things the
way the team would and never invents an account.

**Last reviewed:** 2026-10-15, by Head of Finance

## Source of truth

The full account list lives in QuickBooks Online. Claude reads it from there. This page
explains the structure and the judgment calls.

**Rule:** Claude only uses accounts that exist in QuickBooks. If a task seems to need an account
that doesn't exist, stop and ask. Never create or rename accounts.

## Numbering

| Range | Type | Notes |
| --- | --- | --- |
| 1000-1999 | Assets | Cash 1010-1030, prepaids 1300, fixed assets 1500s, clearing 1950s |
| 2000-2999 | Liabilities | Ramp card 2010, accrued expenses 2101, deferred revenue 2400 |
| 3000-3999 | Equity | |
| 4000-4999 | Revenue | 4000 subscription, 4100 services |
| 5000-5999 | Cost of revenue | Hosting, AI inference, support, payment processing |
| 6000-7999 | Operating expenses | By department class: R&D, S&M, G&A |
| 8000-9999 | Other income and expense | Interest income, FX |

## Departments, classes, and other dimensions

Every expense line on a JE needs a **Class**: R&D, S&M, G&A, or COGS. No locations or projects.

## The judgment calls

| Spend or activity | Account | Why |
| --- | --- | --- |
| Stratus Cloud, production | 5100 Hosting (COGS) | Serves customers |
| Stratus Cloud, dev and staging | 6420 Software & Tools, class R&D | Internal use |
| Lattice Inference API | 5110 AI Inference (COGS) | Powers product features customers use |
| Contractors | 6150 Contractors, class by team | Not payroll; 1099s at year end |
| Stripe fees | 5300 Payment Processing (COGS) | Grossed up from net payouts |
| Laptops under $2,500 | 6410 Computer Equipment (expensed) | Under the capitalization threshold |

## Reporting rollups

The definitions behind these live in `handbook/metrics-and-reporting.md`.

| Rollup | What it's for | Accounts |
| --- | --- | --- |
| Recurring revenue (MRR) | The accounts that add up to recurring revenue | 4000 Subscription Revenue |
| Contra-revenue | Discounts, credits, and refunds netted against revenue | None separate. Booked directly against 4000. |
| Excluded from burn | One-time or non-operating activity left out of run-rate burn | 8000s (interest income, FX). One-time items named in `handbook/metrics-and-reporting.md`. |
| Sales and marketing spend (for CAC) | What counts as acquisition cost | Every 6000-7999 line with class S&M |
| Clearing | Accounts money passes through, which should net to zero (also listed below) | 1950 Ramp Clearing, 1960 Stripe Clearing, 2150 Payroll Clearing |

## Accounts that should always be zero

- 1950 Ramp Clearing
- 1960 Stripe Clearing
- 2150 Payroll Clearing

## Accounts to leave alone

- 6990 Ask My Accountant (legacy, from the pre-Series A bookkeeper). Must stay at zero.
