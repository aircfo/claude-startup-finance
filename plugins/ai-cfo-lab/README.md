# ai-cfo-lab (plugin)

The home for skills shipped with the **AI CFO newsletter**. Each one is a
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
  with synthetic fixtures only. Run it by asking "run the AI spend analysis" or
  invoking `/ai-spend-analysis`.

## How to use

Ask in plain English ("how much are we spending on Claude?") and the right skill
runs automatically, or invoke a skill by name (e.g. `/ai-spend-analysis`). The
first run of `ai-spend-analysis` walks you through setup; after that, monthly
runs are a single step.
