# ai-cfo-lab (plugin)

The home for skills shipped with
**[The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo)**. Each one is a
self-contained workflow you can install and run against your own systems — no
airCFO data, no shared secrets, read-only wherever it touches money.

> **Unofficial.** Not affiliated with, endorsed by, or sponsored by Anthropic or
> any other vendor named in these skills. Provided as-is under the MIT license.

## Skills

- **ai-spend-analysis**: where your company's AI spend went and where it's heading.
  Every dollar of Anthropic and OpenAI seats, extra usage and API spend goes to a person
  and a team, or shows as Unassigned with the reason. It projects this month and next and
  drafts two alerts: a team's day spiking, and the month running well over plan.
  - **Built on Ramp.** API spend and the people list come through the Ramp connector, and
    Ramp holds the Admin keys, so the skill never touches one.
  - **Open-source math.** The numbers come from
    [aicfo-spend-analysis](https://github.com/aircfo/aicfo-spend-analysis), which runs
    without Claude. The skill downloads the pinned release once, checks its fingerprint,
    and runs it on files in your company's folder.
  - **Daily.** A Cowork scheduled task refreshes the numbers each day. Shared outputs show
    teams by default.
  - **Read-only.** It never changes seats, billing or settings, and it never sends anything.
  - **Get started:** ask "set up AI spend tracking", or invoke `/ai-spend-analysis`.

## How to use

Ask in plain English ("how much are we spending on Claude?") and the right skill
runs automatically, or invoke a skill by name (e.g. `/ai-spend-analysis`). The
first run of `ai-spend-analysis` walks you through setup; after that, a daily
scheduled task keeps the numbers current.

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
