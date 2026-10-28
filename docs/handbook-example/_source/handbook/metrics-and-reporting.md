# Metrics and reporting

**What this page is for:** the numbers the company runs on, defined exactly, plus who reads
them and when.

**Last reviewed:** 2026-10-15, by Head of Finance

> Which accounts feed each metric lives in `handbook/chart-of-accounts.md` (Reporting
> rollups), and which accounts count as cash lives in `handbook/cash.md`.

## The numbers we run on

| Metric | Exact definition | Source | Target or benchmark |
| --- | --- | --- | --- |
| MRR | Subscription revenue recognized in the month (4000). Excludes onboarding fees (4100). ARR is MRR times 12. | QuickBooks P&L, closed months only | 2026 Operating Plan v3 |
| Gross margin | Revenue less cost of revenue (5000-5999), as a % of revenue | QuickBooks P&L | 75% or better |
| Net burn | See Burn and runway below | Mercury, checked against QuickBooks | Plan v3 |
| Runway | See Burn and runway below | Mercury | 24 months or more |
| Net revenue retention | MRR this month from customers who existed 12 months ago, divided by their MRR then | Stripe | 110% or better |

**Boundary cases:** Annual prepays count toward MRR as they're recognized, not when billed. Free
trials are not revenue. Onboarding fees are services revenue, never MRR.

## Burn and runway

- **Gross burn:** All cash out of Mercury operating checking, excluding transfers to treasury.
- **Net burn:** Gross burn less cash collected from customers (Stripe payouts and wires).
- **Financing inflows:** The Series A and any future equity or debt proceeds are excluded from net burn.
- **One-time items:** Left out of run-rate burn when the Head of Finance says so, and listed in the monthly package. Current list: the November 2026 offsite.
- **Lookback window:** Trailing three full closed months.
- **Runway:** Runway cash (operating plus treasury, per `handbook/cash.md`) divided by average monthly net burn over the lookback window.

## Customers and revenue

- **Customer list of record:** Stripe.
- **Collections versus revenue:** About 35% of ARR is billed annually in advance, so cash collected runs ahead of revenue in renewal months. Deferred revenue (2400) is the bridge.
- **Customer concentration:** Flag any customer over 10% of ARR. Today none is.

## People and payroll

- **Headcount of record:** Gusto. Contractors are listed separately.
- **Loaded cost:** Salary plus 22% for payroll taxes and benefits.
- **Contractors:** Engaged through Ramp bills, coded to 6150 Contractors by team, and not counted in headcount.
- **Bonuses and commissions:** Quarterly bonuses accrued monthly at target and paid the month after quarter end. Sales commissions paid monthly on collected cash.

## Plan and forecast

- **Budget or forecast of record:** Google Sheets, "2026 Operating Plan v3", board-approved March 2026. Variance is measured against it.
- **Hiring plan:** Four roles in Q4 2026 (two engineers, one AE, one support lead), tracked in the plan's Headcount tab.
- **Known changes coming:** The November 2026 offsite (about $60,000, one-time). A per-seat price increase for new customers in January 2027.
- **Seasonality:** Annual renewals cluster in December and January, so collections spike then while MRR doesn't.

## Who reads the numbers

| Audience | What they get | Cadence | What they always ask |
| --- | --- | --- | --- |
| CEO | Reporting package (Google Slides) | Monthly, by BD8 | Runway, and burn against plan |
| Board | Board pack: the reporting package plus a KPI page | Quarterly | Net revenue retention, gross margin trend |
| Investors | Update email | Monthly, by BD10 | MRR growth and runway |

- **Preferred format:** Lead with MRR, net burn, and runway, then one paragraph of commentary per material variance. The September 2026 package is the model; it's saved in `handbook/sources/`.
- **Reporting only on closed months:** numbers for a month that isn't closed (per
  `handbook/close-process.md`) are labeled preliminary.
