---
title: All Systems Go
theme: connected-stack
order: 1
summary: Connects Stripe, Ramp, and Mercury to Claude — read-only, with your own logins — and adds the cross-system workflows that need them. Named for airCFO's All Systems Go series on the startup back-office stack.
plugin: all-systems-go
plugin_home: true
reads: [Stripe, Ramp, Mercury]
needs_finance_brain: true
time: A few minutes to authorize each system you use
---

## One place for your connectors

Every tool in this library that reads Stripe, Ramp, or Mercury uses the connectors in this
plugin. You authorize each system once, and each tool page tells you exactly which plugins
it needs. QuickBooks is the one exception: connect it in Claude's connector settings with
your own login (for example, Intuit's QuickBooks connector).

| System | What tools read from it |
| --- | --- |
| Mercury | Bank balances and every cash movement, which is the complete record of burn |
| Ramp | Card and bill spend by vendor and category, which explains *what's inside* the burn |
| Stripe | Subscriptions, payments, fees, and refunds, the source for MRR and revenue tie-outs |

Authorize the systems you use and decline the rest. Declining never blocks anything.

## What it adds

<div class="card-grid" markdown="0">
{%- for theme in site.data.themes %}
  {%- assign bundled_tools = site.tools | where: "plugin", "all-systems-go" | where: "theme", theme.key | sort: "order" %}
  {%- for tool in bundled_tools %}
    {%- unless tool.plugin_home %}{% include tool-card.html tool=tool %}{% endunless %}
  {%- endfor %}
{%- endfor %}
</div>

## Fill in your Finance Brain

Working from a [Finance Brain]({{ '/finance-brain.html' | relative_url }})? After you
authorize, use the kit's `setup-finance-brain` skill again. The refresh reads your bank, card,
and billing accounts and fills in the cash, systems, and metrics pages your books alone
can't.
