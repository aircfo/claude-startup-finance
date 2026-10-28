---
title: Tool Library
---

<div class="hero" markdown="0">
  <p class="eyebrow">From The AI CFO newsletter · by airCFO</p>
  <h1>Build an AI-powered finance function.</h1>
  <p class="lede">Free, read-only Claude tools for startup finance and accounting, organized by the job they do. Start with the <strong>Finance Brain Starter Kit</strong>: a folder that gives Claude your handbook, your recurring skills, and a review step, so it works the way your team does.</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="{{ '/finance-brain.html' | relative_url }}">Get the starter kit</a>
    <a class="btn btn-secondary" href="#tools">Browse the tools</a>
  </div>
</div>

<p class="credibility" markdown="0">Built by <a href="https://aircfo.com">airCFO</a>, the AI-enabled back-office growth partner for startups — on the same context model our team runs on our own books.</p>

## How it fits together

<div class="card-grid card-grid-steps" markdown="0">
  <a class="card tool-card" href="{{ '/finance-brain.html' | relative_url }}">
    <span class="step-no">1</span>
    <h3>Build your Finance Brain</h3>
    <p>Download the free starter kit. Claude drafts your handbook from your docs and books, then asks you only what they can't answer.</p>
  </a>
  <a class="card tool-card" href="#connected-stack">
    <span class="step-no">2</span>
    <h3>Connect your stack</h3>
    <p>Add Stripe, Ramp, and Mercury once, read-only, with your own logins. Every tool that needs them shares them.</p>
  </a>
  <a class="card tool-card" href="#cash-and-runway">
    <span class="step-no">3</span>
    <h3>Run the workflows</h3>
    <p>Runway, revenue tie-outs, board metrics, and more as they ship. Each reads your Finance Brain before it touches a number.</p>
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

Every connector is the vendor's own, authorized with your own login. airCFO runs no server
in between, and your Finance Brain is a folder on your machine.
[Data handling and security]({{ '/data-handling-security.html' | relative_url }})

## Install once, add tools anytime

Everything runs in [Claude Cowork](https://claude.com/product/cowork), the Cowork tab in the
Claude desktop app, on Pro, Max, Team, and Enterprise plans. The starter kit is a download:
nothing to install. For the tools, add the airCFO marketplace once, and every tool after that
is a one-click install. Each tool's page lists exactly which plugins it needs, in order.

## Documentation

- [Finance Brain Starter Kit]({{ '/finance-brain.html' | relative_url }}): download it and get set up in Cowork.
- [Example handbook]({{ '/handbook-example/' | relative_url }}): the kit filled in for a fictional Series A company.
- [Prompts to try]({{ '/use-cases.html' | relative_url }}): including ad-hoc analyses with no dedicated tool yet.
- [Data handling and security]({{ '/data-handling-security.html' | relative_url }}): read before you connect anything.
- [Known limitations]({{ '/known-limitations.html' | relative_url }}): the honest list.

<div class="section-note newsletter-note" markdown="0">
  <p><strong>New tools ship with The AI CFO.</strong> Practical, tested playbooks for startup finance in the age of AI, every two weeks. Each tool here is versioned, so what you read still matches what you install.</p>
  <a class="btn btn-secondary" href="{{ site.newsletter_url }}">Subscribe to The AI CFO</a>
</div>
