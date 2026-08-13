---
title: Authoring Conventions
description: House rules for adding a skill, plugin, or connector to the airCFO Claude for Startup Finance repo — naming, required files, versioning, and the release process.
---

# Authoring conventions

House rules for anything published out of
[`aircfo/claude-startup-finance`](https://github.com/aircfo/claude-startup-finance). The
goal is that a reader arriving from an AI CFO issue can install exactly the thing that
issue was about, at a version that still matches what they read.

If you're contributing from outside airCFO, start with
[CONTRIBUTING.md](https://github.com/aircfo/claude-startup-finance/blob/main/CONTRIBUTING.md);
this page is the detail behind it.

## What lives in this repo, and what doesn't

| Product type | Home | Why |
| --- | --- | --- |
| Plugin (skills + bundled connectors) | `plugins/<name>/` in this repo | The Cowork marketplace installs from this repo's `.claude-plugin/marketplace.json`. |
| Standalone skill | A plugin directory in this repo (see below) | Skills need a plugin wrapper to appear in the marketplace; they also install directly via the `skills` CLI. |
| MCP server | **Its own repository** (e.g. [`aircfo/qbo-mcp`](https://github.com/aircfo/qbo-mcp)) | Servers deploy and version on their own cadence, and the marketplace pulls this whole repo on install — server code would bloat every user's install. |
| Micro webapp / demo | **Its own repository**, or the docs site if it's a static page | Same reason: build artifacts and deploy pipelines don't belong in an install payload. |

**Everything airCFO publishes for Claude gets a row in the root README's "What's in this
repo" table, including things hosted in another repository.** The table is the index; the
directory tree is only the part that ships inside a plugin install. Do not create empty
placeholder directories for product types that don't exist yet — an empty `apps/` reads as
vaporware. Add the directory in the same commit as the first real thing in it.

## When a skill gets its own plugin

Plugins — not skills — are the unit of listing, versioning, and installation in the Claude
plugin browser. That drives the split:

**Give the skill its own plugin when it's a headline deliverable.** Anything a newsletter
issue, essay, or demo is *about* should be independently browsable, independently
versioned, and linkable as "install this one thing." This is the default for a new
newsletter drop.

**Add it to an existing plugin when it's a supporting part of that plugin's job.** A skill
that only makes sense with a sibling skill's output, or a small utility inside an existing
workflow family, belongs in that plugin. `all-systems-go` is a deliberate bundle: its
workflows share connectors and all read the ContextOS first.

**The trade-off, stated plainly.** One plugin per skill means a reader who wants five drops
performs five installs, and the marketplace list grows with every issue. Bundling means new
skills never get their own listing and inherit an unrelated version number. We accept the
longer list, because a newsletter link should resolve to one installable thing. Revisit
this if the list gets long enough to be a browsing problem — grouping *retired* drops into
an archive plugin is the escape hatch, since renaming or moving a live plugin breaks
existing installs.

**Never retroactively split or rename a published plugin.** `ai-cfo-lab` keeps
`ai-spend-analysis` where it is, permanently. Moving it would break every install that
already points at it. This repo has already migrated users once (the old `startup-finance`
plugin split into `finance-contextos` + `all-systems-go`); a second forced migration would
spend trust we don't need to spend.

## Required files

A plugin directory:

```
plugins/<plugin-name>/
├── .claude-plugin/plugin.json    # required
├── .mcp.json                     # only if the plugin bundles connectors
├── skills/<skill-name>/SKILL.md  # required, one directory per skill
└── README.md                     # required
```

`templates/skill-plugin/` is a copy-ready scaffold of exactly this shape. Copy it, rename
the placeholders, and delete the parts you don't need.

**`plugin.json`** requires `name` (matching the directory), `description`, and `version`.
Include `displayName`, `author`, `homepage`, `repository`, `license`, and `keywords` to
match the existing plugins.

**`SKILL.md`** requires YAML frontmatter with `name` and `description`. The description is
the trigger surface — it is how the agent decides whether to run the skill, so write it as
*what it does plus the phrases a user would actually say*, in the style of the existing
skills. A vague description is the single most common reason a skill never fires.

## Naming

- Lowercase, hyphen-separated, no spaces or underscores: `revenue-reconciliation`.
- **The skill's directory name, its `name` in frontmatter, and its slash command are all
  the same string.** `skills/board-metrics/` is invoked as `/board-metrics`.
- Plugin directory name matches `name` in `plugin.json` and the marketplace entry.
- Prefer a verb-or-noun phrase describing the outcome (`runway-and-burn`), not a product
  name.

## Registering in the marketplace

A plugin does not appear in Cowork until it's listed in `.claude-plugin/marketplace.json`.
Add an entry with `name`, `source` (`./plugins/<name>`), `description`, `version`,
`category`, `keywords`, and a `skills` array listing each skill directory relative to the
plugin root:

```json
{
  "name": "ai-cfo-lab",
  "source": "./plugins/ai-cfo-lab",
  "description": "…",
  "version": "0.1.0",
  "category": "finance",
  "keywords": ["finance", "newsletter"],
  "skills": ["./skills/ai-spend-analysis"]
}
```

The `skills` array is what the [`skills` CLI](https://github.com/vercel-labs/skills) reads
for deterministic discovery (its *Plugin Manifest Discovery* mode), so readers who use
Claude Code rather than Cowork get a reliable `--skill <name>` install instead of relying
on the CLI's recursive-search fallback.

> **A new skill must be added in two places: its plugin directory *and* the `skills` array
> in `marketplace.json`.** A skill missing from the array still works in Cowork but becomes
> undiscoverable to the CLI. The pull-request template checks for this.

Do not add `metadata.pluginRoot`. Setting it changes how `source` paths are interpreted,
and the current explicit `./plugins/<name>` paths already work in both Cowork and the CLI.

## Release process

Versions are explicit — users click **Update** in Cowork to re-sync, so a version bump is
the signal that anything changed.

1. **Bump `plugin.json` and the matching `marketplace.json` entry in lockstep.** They must
   never disagree. Semver: patch for fixes and copy, minor for new capability or a new
   skill, major for a breaking change to a skill's inputs or output layout.
2. **Add a `CHANGELOG.md` entry** under a new version heading, in
   [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format.
3. **Tag the merge commit** `v<x.y.z>` and cut a GitHub Release with the changelog section
   as its body.
4. **Link the corresponding AI CFO issue** in the release notes when the drop accompanies
   published writing, so a reader can get the exact version the piece described.

Repo-wide tags cover the repo, not one plugin. When a release touches a single plugin, say
so in the release title (`v1.2.0 — ai-cfo-lab`).

## Before opening a pull request

- `jq . .claude-plugin/marketplace.json` and every `plugins/*/.claude-plugin/plugin.json`
  parse cleanly.
- `npx skills add . --list` from the repo root lists every skill, including any new one.
- The marketplace still loads in Cowork and the affected plugin installs. This one is
  manual and cannot be skipped — a malformed manifest breaks install for everyone.
- No secrets, tokens, customer data, or real financial data in the diff. Fixtures stay
  synthetic.
- Anything touching a financial system is still **read-only**, and every touched README
  keeps its Unofficial / not-affiliated disclaimer.
