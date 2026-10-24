# Changelog

All notable changes to this repository are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

**How versions work here.** Plugins are versioned individually —
`.claude-plugin/marketplace.json` is the source of truth, and each plugin's `plugin.json`
must match it. Headings below name the version and the plugin it applies to. Through v0.9.0
the two flagship plugins shared a version line (they were one plugin until the v0.9.0
split); `ai-cfo-lab` versions independently.

Entries dated before this file existed were reconstructed from git history, so they
summarize each release rather than listing every commit. Dates are commit dates. The
repository had no git tags or GitHub Releases before this file — see
[docs/authoring-conventions.md](docs/authoring-conventions.md) for the release process going
forward.

## [Unreleased]

### Added

- Root README reworked into a hub: badge row, a one-line hook with three "what you get"
  lines, a table of contents, and a **What's in this repo** table covering every published
  product type — including artifacts hosted in their own repositories, such as the
  `qbo-mcp` connector server.
- Instructions for installing individual skills without Claude Cowork, via the
  [`skills` CLI](https://github.com/vercel-labs/skills), with an explicit note that skills
  installed that way do not include the plugins' bundled connectors.
- `docs/authoring-conventions.md` — when a skill gets its own plugin versus joining an
  existing one, required files, naming rules, marketplace registration, and the release
  process.
- `templates/skill-plugin/` — a copy-ready scaffold for shipping a new skill as its own
  plugin. Verified that it is not picked up by skill discovery.
- `CHANGELOG.md` (this file), `SECURITY.md`, `CONTRIBUTING.md`, GitHub issue templates for
  bug reports and skill requests, and a pull-request checklist covering read-only
  preservation, secrets, disclaimers, and manifest validity.
- `skills` arrays on every plugin entry in `marketplace.json`, so the `skills` CLI resolves
  each skill through documented Plugin Manifest Discovery rather than its recursive-search
  fallback. Verified against Claude Code's own loader that this does not double-register
  skills already found by the default `skills/` scan.
- `assets/social-preview.png` — the GitHub social preview card (the thumbnail on every share),
  built from the docs site's brand tokens, with its HTML source and re-render instructions
  committed alongside it.
- Links to [The AI CFO Newsletter](https://www.aircfo.com/the-ai-cfo) from the README badge
  row and follow-along section, every plugin README footer, and the issue-template contact
  links.

### Changed

- `plugins/ai-cfo-lab/README.md` now presents the plugin as the index of AI CFO newsletter
  skills, and records that future headline skills may ship as their own plugins while
  `ai-spend-analysis` stays where it is permanently.

### Notes

- **No plugin version bumps in this release.** No skill behavior changed — the diff is
  repository documentation plus additive manifest metadata. Plugin versions stay at
  `finance-contextos` 0.9.0, `all-systems-go` 0.9.0, `ai-cfo-lab` 0.1.0 so installed users
  aren't prompted to update for a docs-only change.
- `metadata.pluginRoot` was deliberately **not** added: it changes how `source` paths are
  interpreted, and the existing explicit `./plugins/<name>` paths already resolve correctly
  in both Cowork and the `skills` CLI.

## [0.9.0] — 2026-08-06 — `finance-contextos` + `all-systems-go`

### Changed

- **Split the marketplace into two plugins.** The former single `startup-finance` plugin
  became `finance-contextos` (QuickBooks only — build your ContextOS) and `all-systems-go`
  (Stripe, Ramp, Mercury, and the cross-system workflows). Existing context folders keep
  working; users migrate by uninstalling the old plugin and installing the new ones.
- Rewrote the documentation site around the ContextOS concept and the two-plugin split,
  including navigation labels, meta descriptions, and the self-hosting link.
- Aligned `finance-context-builder`'s build sequence with the client-zero methodology proven
  on airCFO's own books.

## [0.8.0] — 2026-08-04 — `finance-context-builder`

### Added

- **Account map v2, the cube schema.** Every account classifies on independent axes
  (expense category, department, cash-flow line, tags) instead of a single bucket, with
  row-level governance — `auto`, `needs-review`, `confirmed` — so a refresh never overwrites
  a human's confirmed judgment.

## [0.7.0] — 2026-08-04 — `finance-context-builder`

### Added

- **Prove-it-ties validation.** The build now ends by verifying the model against the live
  books rather than on "here are your files"; unexplained differences become open questions.
- Connector resilience: partial access (a blocked endpoint or an oversized read) degrades to
  an explicit placeholder instead of failing the whole run.
- An airCFO-branded documentation site (GitHub Pages).

### Fixed

- `runway-and-burn` computes burn from Mercury bank flows rather than Ramp card spend, which
  had understated true net burn.

## [0.6.0] — 2026-06-26

### Added

- Finance-profile persistence and a connector preflight check ahead of long builds.
- Source-verified data-handling and security copy, replacing placeholder text.

### Fixed

- Hardened `finance-context-builder` setup from beta-tester feedback, including a smoother
  first-run flow and a distinctly named QuickBooks connector.

## [0.5.0] — 2026-06-23

### Added

- The 14-section finance profile and the draft-with-placeholders flow: the build drafts from
  what it actually knows and marks every gap explicitly rather than guessing.
- `finance-skill-builder` dry-runs a skill's logic and hands the result off in chat.

## [0.4.0] — 2026-06-22

### Added

- Meta-skills (`finance-skill-builder`, `finance-skill-tuner`) and airCFO branding.
- Account-map consolidation.

### Changed

- Renamed the onboarding skill to `finance-context-builder`.
- Removed the `/finance` command in favor of a pure skills-only plugin.

## [0.1.0] – [0.3.0] — 2026-06-17 → 2026-06-22

### Added

- Initial marketplace scaffold, the finance onboarding skill, and the semantic-layer profile
  that became the ContextOS.

### Fixed

- Corrected the Ramp MCP server URL to its canonical endpoint.

---

## `ai-cfo-lab`

### [0.2.0] — Unreleased

#### Added

- `ai-spend-analysis` can keep a shared **Claude Dashboard** current every day: a cloud
  routine refreshes API cost from Ramp (no keys, no per-person data), and a job on the
  operator's Mac pulls the claude.ai spend export with a fixed script (no AI in the loop) through
  a dedicated, signed-in browser profile. Runbook in
  the skill's `references/daily-refresh.md`.
- Optional Ramp sources: API cost from Ramp's AI-spend connection, and Anthropic charges
  on company cards (shown beside the totals, not added to them).
- Claude Code usage per person or API key from the Admin API's Claude Code usage report.
- A `dashboard_visibility` setting, defaulting to department level: names and emails are
  filtered out before anything is uploaded.

#### Changed

- Reversed two roadmap items previously marked "not planned" (Ramp ingestion and
  scheduled jobs); the reasoning is in the skill's design-decisions notes.

#### Fixed

- The API cost pull no longer drops the last second of each month.

### [0.1.0] — 2026-07-23

#### Added

- New `ai-cfo-lab` plugin as the home for AI CFO newsletter skills, registered in the
  marketplace.
- `ai-spend-analysis` — an org-wide Anthropic/Claude spend dashboard across committed seats,
  variable seat-overage, and API-platform cash, broken out by person, department, product,
  and model. Rebuilds two Excel workbooks plus a self-contained interactive HTML dashboard
  and drafts (never sends) a summary. Ships with synthetic fixtures only and never modifies
  seats, billing, or org settings.
- Roster bootstrap and a secure key drop-file for first-run setup.
