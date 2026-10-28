<!--
Thanks for the pull request. Fill in what applies and delete what doesn't.
"N/A" is a fine answer on any checklist line — a silently unchecked box is not.
Contributor guide: CONTRIBUTING.md · House rules: docs/authoring-conventions.md
-->

## What changed

<!-- One or two sentences. What does this do, and why? -->

## How it was verified

<!--
These artifacts are prompt-shaped, so a real run is the test. Say what you actually ran and
what came back — "ran /runway-and-burn against a QuickBooks sandbox; burn matched the manual
figure" is worth more than a green checkmark.
-->

## Checklist

**Safety — the non-negotiables**

- [ ] **Read-only preserved.** Nothing added can write, send, transfer, or delete in an
      accounting, banking, payments, or spend system. Anything outward-facing is drafted for a
      human, never sent.
- [ ] **No secrets.** No API keys, OAuth tokens, client secrets, or account numbers in the
      diff — including fixtures, tests, and commit messages.
- [ ] **No real financial or customer data.** Fixtures and examples are synthetic, not
      anonymized production data.
- [ ] **Per-user auth.** Any new connector authenticates as the user via their own OAuth
      login, not a shared credential.

**Install path — breaking these breaks existing users**

- [ ] `claude plugin validate .` passes, and `claude plugin validate plugins/<name>` passes
      for every plugin touched.
- [ ] Installed end to end in a throwaway config (`CLAUDE_CONFIG_DIR=$(mktemp -d)`), and
      `claude plugin details <plugin>` shows the **expected skill count** and MCP servers —
      see CONTRIBUTING.md for the exact commands.
- [ ] No published plugin or skill was renamed, moved, or split.
- [ ] New skills are registered in **both** their plugin directory **and** the `skills` array
      in `marketplace.json` — `npx skills add . --list` shows them by name.

**Housekeeping**

- [ ] `plugin.json` and the matching `marketplace.json` entry bumped **in lockstep** (or no
      version change needed because behavior didn't change).
- [ ] `CHANGELOG.md` entry added under `[Unreleased]`.
- [ ] Docs updated — root README table, plugin README, and the docs site where affected.
- [ ] A new reader-facing tool has its library page in `docs/_tools/` (theme, `reads`,
      summary), and the site builds locally.
- [ ] No connector bundled that another plugin already provides — see `docs/_data/connectors.yml`.
- [ ] Every touched README keeps its Unofficial / not-affiliated disclaimer and its read-only
      language.
- [ ] All new relative links resolve on GitHub **and** on the published Pages site.
- [ ] No internal or unreleased product names, client names, or airCFO-internal detail
      introduced anywhere public.

## Follow-ups

<!-- Anything deliberately left for a human: releases, images, repo settings, a manual check
     you couldn't run. -->
