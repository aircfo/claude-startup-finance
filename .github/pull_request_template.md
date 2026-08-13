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

- [ ] `jq . .claude-plugin/marketplace.json` and every touched `plugin.json` parse cleanly.
- [ ] The marketplace loads in Claude Cowork and the affected plugin installs. *(Manual —
      not skippable.)*
- [ ] No published plugin or skill was renamed, moved, or split.
- [ ] New skills are registered in **both** their plugin directory **and** the `skills` array
      in `marketplace.json` — `npx skills add . --list` shows them by name.

**Housekeeping**

- [ ] `plugin.json` and the matching `marketplace.json` entry bumped **in lockstep** (or no
      version change needed because behavior didn't change).
- [ ] `CHANGELOG.md` entry added under `[Unreleased]`.
- [ ] Docs updated — root README table, plugin README, and the docs site where affected.
- [ ] Every touched README keeps its Unofficial / not-affiliated disclaimer and its read-only
      language.
- [ ] All new relative links resolve on GitHub **and** on the published Pages site.
- [ ] No internal or unreleased product names, client names, or airCFO-internal detail
      introduced anywhere public.

## Follow-ups

<!-- Anything deliberately left for a human: releases, images, repo settings, a manual check
     you couldn't run. -->
