# ai-cfo-lab (plugin)

The home for skills shipped with
**[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo)**. Each one is a
self-contained workflow you can install and run against your own systems — no
airCFO data, no shared secrets, read-only wherever it touches money.

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Anthropic or
> any other vendor named in these skills. Provided as-is under the MIT license.

## Skills

- **ai-spend-analysis** — turn your organization's Anthropic/Claude spend into a
  person / department / product / model dashboard across three cost surfaces
  (committed seats, variable seat-overage, and API-platform cash). A
  conversational first run sets up a local workspace; monthly runs rebuild two
  Excel workbooks + a self-contained interactive HTML dashboard and draft (never
  send) a summary. It never modifies seats, billing, or org settings, and ships
  with synthetic fixtures only. It can also keep a shared Claude Dashboard
  current every day (department-level by default), with the scheduled jobs
  proposed for your approval. Setup is guided by a checkup that names each
  next step and who can do it, so an Ops lead can run it without help. Run it
  by asking "set up AI spend tracking" or invoking `/ai-spend-analysis`.

## How to use

Ask in plain English ("how much are we spending on Claude?") and the right skill
runs automatically, or invoke a skill by name (e.g. `/ai-spend-analysis`). The
first run of `ai-spend-analysis` walks you through setup; after that, monthly
runs are a single step.

## Where new newsletter skills land

This plugin is the **index of AI CFO newsletter skills** — the place to look first
for anything shipped with an issue. It is not necessarily the place every skill
lives: going forward, a skill that is the headline of its own issue typically
ships as **its own plugin**, so it gets its own marketplace listing, its own
version, and an install link that resolves to exactly one thing. Smaller
supporting utilities join this plugin instead.

Either way, every published skill is listed in the root
[README's "What's in this repo" table](https://github.com/aircfo/claude-startup-finance#whats-in-this-repo).
The rule for choosing between the two is in
[docs/authoring-conventions.md](https://aircfo.github.io/claude-startup-finance/authoring-conventions.html).

`ai-spend-analysis` stays here permanently — moving a published skill would break
existing installs.

---

Part of [(Un)official Claude for Startup Finance](https://github.com/aircfo/claude-startup-finance)
by [airCFO](https://aircfo.com) · [Docs](https://aircfo.github.io/claude-startup-finance/) ·
[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo)
