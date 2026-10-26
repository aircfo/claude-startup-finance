# Security overview

One page for whoever approves this tool: what data it reads, where that data
goes, who can see it, and what holds credentials. Everything below is the
daily-dashboard setup; the monthly workflow is the same minus the dashboard
and the scheduled jobs.

## Data flow

```
 claude.ai spend export ──(fixed script, Owner's saved login)──┐
 Anthropic Admin API ─────(Admin key, read endpoints only)────┼──► Workspace on one Mac ──(filtered datasets)──► Claude Dashboard
 Ramp ────────────────────(the operator's Ramp connector)─────┘     (local files)                                 (claude.ai, private
                                                                                                                  until shared)
 Optional cloud routine: Ramp ──► org-wide API cost only ──────────────────────────────────────────────────────► same dashboard
```

## What is read

| Source | What it contains | How it's reached |
|---|---|---|
| claude.ai spend export | Per person: email, product, model, requests, tokens, overage dollars | One GET request through a dedicated browser profile signed in by a claude.ai Owner |
| Anthropic Admin API | Console API usage and cost; Claude Code usage per person or API key | An Admin API key stored on the Mac |
| Ramp | Anthropic card charges (cardholder name, amount, date); API cost per model | The operator's own claude.ai Ramp connector (OAuth); Claude saves the answers |
| HR / payroll export (once, at setup) | Names, departments, active status | A file the operator provides |

Nothing is written to any of these systems. The tool never changes seats,
billing, settings, cards or transactions, and never sends a message.

## What is stored, and where

Everything lands in **one workspace folder on the operator's Mac**, outside any
git repository, with a `.gitignore` covering every sensitive path:

- `raw/`, `workbooks/`, `artifacts/`, `dashboard/` — per-person spend history,
  kept until `uninstall.py --purge-data`.
- `config/` — the roster (names, emails, departments, seat types).
- `.secrets/anthropic_admin_key` — the Admin key, file mode 600.
- `.browser-profile/` — the **claude.ai Owner session** the export uses. Treat
  it like a password: anyone who can read this macOS user's files can act as
  that Owner on claude.ai until the session expires or is signed out. Keep
  FileVault on, don't share the macOS account, and remove it with
  `uninstall.py --remove-login` when the tool is retired or the operator
  changes.
- `logs/` — job output and setup check statuses; no keys, and no spend in the
  setup log.

## What leaves the Mac

- **To the Claude Dashboard** (hosted on claude.ai under the operator's
  account): the datasets `manifest.json` lists. With `dashboard_visibility:
  "department"` (the default) no name or email is uploaded — people are summed
  into departments first. With `"person"`, per-person rows are uploaded.
  **Anyone the dashboard is shared with can download every row** from its
  Sources panel, so sharing is the access control. The dashboard is private
  until its owner shares it. Each refresh replaces the previous upload and
  deletes it.
- **To Claude** (the model), during the scheduled run: Ramp's answers (card
  charges with cardholder names) and the pipeline's summaries, under the
  operator's Claude plan terms. The spend export itself is fetched and saved by
  code, not read by the model.

## Credentials

| Credential | Power | Held | Limit it by |
|---|---|---|---|
| Anthropic Admin API key | Admin keys can do more than read; the scripts call only read endpoints | `.secrets/` on the Mac | A dedicated key for this tool; revoke it in platform.claude.com when retiring |
| claude.ai Owner session | Full Owner access to claude.ai | `.browser-profile/` on the Mac | Dedicated profile, FileVault, `--remove-login` on retirement; signing out of claude.ai everywhere ends it |
| Ramp connector | What the operator's Ramp role allows (the tool uses read tools only) | claude.ai (OAuth) | The operator's Ramp permissions |

No credential is stored in the cloud. The optional cloud routine uses only the
Ramp connector, under the operator's claude.ai account.

## Known risks

- **Undocumented endpoint.** The Team-plan export uses the request behind the
  claude.ai Export button, which Anthropic doesn't document and can change. A
  change shows on the dashboard as a failed export; the manual export is the
  fallback.
- **Automation of an Owner session.** Claude Code's safety checks refuse to let
  an unattended Claude session do this, so the export is a fixed script that
  can make only that one request. Review `scripts/fetch_surface_b_browser.py`
  before approving; it is short on purpose.
- **Per-person visibility.** Choosing `"person"` makes individual spend visible
  to everyone the dashboard is shared with.
