---
title: Tool Library
---

<div class="hero" markdown="0">
  <p class="eyebrow">From The AI CFO newsletter · by airCFO</p>
  <h1>Build an AI-powered finance function.</h1>
  <p class="lede">Free, read-only Claude tools for startup finance and accounting, organized by the job they do. Every one starts from your <strong>ContextOS</strong> — your definitions, mapped once and proven against your live books — so Claude uses your numbers the way your team means them.</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="{{ '/tools/contextos/' | relative_url }}">Start with your ContextOS</a>
    <a class="btn btn-secondary" href="#tools">Browse the tools</a>
  </div>
</div>

<p class="credibility" markdown="0">Built by <a href="https://aircfo.com">airCFO</a>, the AI-enabled back-office growth partner for startups — on the same context model our team runs on our own books.</p>

## How it fits together

<div class="card-grid card-grid-steps" markdown="0">
  <a class="card tool-card" href="#foundation">
    <span class="step-no">1</span>
    <h3>Teach Claude your numbers</h3>
    <p>Build your ContextOS from QuickBooks: your definitions, your account map, and a tie-out that proves it against your live books.</p>
  </a>
  <a class="card tool-card" href="#connected-stack">
    <span class="step-no">2</span>
    <h3>Connect your stack</h3>
    <p>Add Stripe, Ramp, and Mercury once, read-only, with your own logins. Every tool that needs them shares them.</p>
  </a>
  <a class="card tool-card" href="#cash-and-runway">
    <span class="step-no">3</span>
    <h3>Run the workflows</h3>
    <p>Runway, revenue tie-outs, board metrics, and more as they ship. Each reads your ContextOS before it touches a number.</p>
  </a>
  <a class="card tool-card" href="#build-your-own">
    <span class="step-no">4</span>
    <h3>Build your own</h3>
    <p>Turn the workflows your team already runs into skills of your own, built to the same standards.</p>
  </a>
</div>

<div id="tools" class="library" markdown="0">
{%- for theme in site.data.themes %}
  {%- assign theme_tools = site.tools | where: "theme", theme.key | sort: "order" %}
  {%- if theme_tools.size > 0 %}
  <section class="theme-section" id="{{ theme.key }}">
    <h2>{{ theme.name }}</h2>
    <p class="theme-summary">{{ theme.summary }}</p>
    <div class="card-grid">
      {%- for tool in theme_tools %}{% include tool-card.html tool=tool %}{% endfor %}
    </div>
  </section>
  {%- endif %}
{%- endfor %}
</div>

## Read-only by design

Every tool reads your systems with your own login and never writes to them. No journal
entries, no payments, no subscription changes. Outputs are analysis for a human to review,
and anything a tool couldn't verify shows up as an open question instead of a confident guess.

The QuickBooks connector is operated by airCFO, open source (MIT), and documented in full:
what it stores, where it runs, and who can touch your data.
[Data handling and security]({{ '/data-handling-security.html' | relative_url }}) ·
[Self-host it instead]({{ '/self-hosting.html' | relative_url }})

## Install once, add tools anytime

Everything installs inside [Claude Cowork](https://claude.com/product/cowork), the Cowork tab
in the Claude desktop app, on Pro, Max, Team, and Enterprise plans. Add the airCFO
marketplace once, and every tool after that is a one-click install. Each tool's page lists
exactly which plugins it needs, in order.

## Documentation

- [First-session guide]({{ '/first-session-guide.html' | relative_url }}): install to first useful output.
- [What is a ContextOS?]({{ '/finance-profile-explainer.html' | relative_url }}): how the context model works.
- [Prompts to try]({{ '/use-cases.html' | relative_url }}): including ad-hoc analyses with no dedicated tool yet.
- [Data handling and security]({{ '/data-handling-security.html' | relative_url }}): read before you connect anything.
- [Self-hosting the QuickBooks connector]({{ '/self-hosting.html' | relative_url }}): run it on your own infrastructure.
- [Known limitations]({{ '/known-limitations.html' | relative_url }}): the honest list.

<div class="section-note newsletter-note" markdown="0">
  <p><strong>New tools ship with The AI CFO.</strong> Practical, tested playbooks for startup finance in the age of AI, every two weeks. Each tool here is versioned, so what you read still matches what you install.</p>
  <a class="btn btn-secondary" href="{{ site.newsletter_url }}">Subscribe to The AI CFO</a>
</div>
