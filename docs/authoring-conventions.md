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

**Never retroactively split or rename a published plugin.** Moving one breaks every install
that already points at it. The one exception so far: `ai-cfo-lab` and its only skill,
`ai-spend-analysis`, were withdrawn on 2026-10-28, when the skill moved into its engine's own
repo, [aircfo/aicfo-spend-analysis](https://github.com/aircfo/aicfo-spend-analysis), and few
if any outside installs used it. This repo has already migrated users once (the old `startup-finance`
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
  "name": "board-pack",
  "source": "./plugins/board-pack",
  "description": "…",
  "version": "0.1.0",
  "category": "finance",
  "keywords": ["finance", "newsletter"],
  "skills": ["./skills/board-pack"]
}
```

`skills` is an [official marketplace field](https://code.claude.com/docs/en/plugin-marketplaces#marketplace-schema).
Its declared paths **add to** the default scan of the plugin's `skills/` directory rather
than replacing it, so listing skills that already sit in the default location is redundant
for Claude Code itself — verified below that it does not double-register them. The reason to
declare it anyway is the [`skills` CLI](https://github.com/vercel-labs/skills): declared
paths put it into documented *Plugin Manifest Discovery* mode instead of its
recursive-search fallback, which is what gives readers on Claude Code (rather than Cowork) a
reliable `npx skills add … --skill <name>`.

> **A new skill must be added in two places: its plugin directory *and* the `skills` array
> in `marketplace.json`.** A skill missing from the array still loads in Cowork — the
> default scan finds it — but discovery by the `skills` CLI stops being deterministic. The
> pull-request template checks for this.

Two related fields, for reference: `strict` defaults to `true`, meaning each plugin's
`plugin.json` stays the authority for its components and the marketplace entry only
supplements it. Don't set `strict: false` here — it would make the marketplace entry the
entire definition and conflict with the `plugin.json` files these plugins ship.

Do not add `metadata.pluginRoot`. It's a real field (it prepends a base directory to
relative `source` paths), but setting it changes how every existing `source` is interpreted,
and the explicit `./plugins/<name>` paths already resolve correctly in both Cowork and the
CLI. No upside, real breakage risk.

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
so in the release title (`v1.2.0 — finance-contextos`).

## Before opening a pull request

Validate the manifests with Claude Code's own validator — it checks more than JSON syntax:

```bash
claude plugin validate .                     # the marketplace manifest
claude plugin validate plugins/<name>        # each plugin you touched
npx skills add . --list                      # every skill appears, including your new one
```

Then run a real end-to-end install. This used to be a manual Cowork step; it isn't — point
Claude Code at a throwaway config directory and it won't touch your own setup:

```bash
export CLAUDE_CONFIG_DIR=$(mktemp -d)        # isolates the test from your real config
claude plugin marketplace add ./             # note the trailing slash; "." is rejected
claude plugin install <plugin>@claude-startup-finance
claude plugin details <plugin>               # the check that matters — see below
unset CLAUDE_CONFIG_DIR
```

`claude plugin details` prints the component inventory that the plugin loader actually
resolved: the skill count and names, the MCP servers, and the projected token cost. Confirm
the skill count is **exactly** what you expect — this is what catches a skill that failed to
load, and it's how we confirmed that declaring `skills[]` doesn't double-register skills
already found by the default scan. Watch the always-on token cost too: every skill's
description loads into every session, so a bloated description is a real cost.

A pass in Cowork specifically is still worth a spot check before a release, since it's the
supported install path, but it's no longer the only way to catch a broken manifest.

Also confirm:

- No secrets, tokens, customer data, or real financial data in the diff. Fixtures stay
  synthetic.
- Anything touching a financial system is still **read-only**, and every touched README
  keeps its Unofficial / not-affiliated disclaimer.
