# Security overview

One page for whoever approves this tool. It covers what data the tool reads, where that data goes, who can see it, and what holds credentials.

## Data flow

```
 Ramp ──────────────────(the operator's Ramp connector)───────┐
 claude.ai spend export ─(Claude in Chrome, the button, or the script)─┼──► The company's folder ──► summaries and a team dashboard
 Seat holders ──────────(admin member lists, by hand)─────────┘    (local files)            (drafts; shared only by a person)
```

## What is read

| Source | What it contains | How it's reached |
|---|---|---|
| Ramp: API key spend | Each API key's name, owner, department tag and estimated cost, for Anthropic and OpenAI | Ramp's connector, under the operator's own Ramp login. Ramp holds the Admin keys. |
| Ramp: vendor totals | Ramp's total API cost for Anthropic and OpenAI, including spend no current key carries | The same connector |
| Ramp: people list | Each person's name, email, department and active status | The same connector |
| claude.ai spend export | Each person's email, product, model and extra-usage dollars | Claude in Chrome clicking the export button in the Owner's own signed-in Chrome, the button by hand, or one GET request by a fixed script through a browser profile a claude.ai Owner signed in |
| Admin member lists | Who holds which seat type, from claude.ai and ChatGPT | Files the operator exports and provides |

Nothing is written to any of these systems. The tool never changes seats, billing, settings, keys or cards, and it never sends a message.

## What is stored, and where

Everything lands in **one folder on the operator's computer**, outside any git repository.

- **`raw/`** holds every download, saved once and read-only.
- **`out/`** holds the spend table, the forecast plan, the alert drafts and the dashboard data.
- **`aicfo-spend.json` and `people.csv`** hold seat prices and who holds a seat.
- **`.engine/`** holds the pinned release of the open-source engine, checked against its fingerprint before it's run.
- **`.browser-profile/`** is created only if the Mac script is used. It holds a **claude.ai Owner session**, so treat it like a password. Anyone who can read this computer account's files can act as that Owner on claude.ai until the session expires or is signed out. Keep FileVault on, don't share the account, and delete the folder when the tool is retired or the operator changes.

## What leaves the folder

- **Shared outputs.** The dashboard data shows teams by default. Teams under 3 people fold together, and no name, email or API key name is included. A person opts into the person view, which shows each person's spend. **Anyone a shared output reaches can read every number in it**, so sharing is the access control.
- **What Claude reads.** During a refresh, Claude reads Ramp's answers and the tool's summaries, under the operator's Claude plan terms. Ramp's answers include people's names. The spend export is saved by code; Claude doesn't need to read it.

## Credentials

| Credential | Power | Held by | Limit it by |
|---|---|---|---|
| Anthropic and OpenAI Admin keys | More than reading usage | **Ramp**, never this tool | Ramp's AI spend settings; revoke them at the vendor when retiring |
| Ramp connector | Whatever the operator's Ramp role allows; the tool uses read tools only | claude.ai (OAuth) | The operator's Ramp permissions |
| claude.ai Owner session (Mac script only) | Full Owner access to claude.ai | `.browser-profile/` in the folder | FileVault; delete it on retirement; signing out of claude.ai everywhere ends it |

## Known risks

- **The export endpoint is undocumented.** The Mac script uses the request behind claude.ai's Export button. Anthropic doesn't document that request and can change it. A change shows as a failed export, and the button is the fallback.
- **An Owner session is automated.** Claude in Chrome acts inside the Owner's signed-in Chrome. The skill limits it to reading member lists and exporting the spend report, never changing anything, and Chrome asks before a download. The Mac script makes only the export's one request; review `scripts/fetch_spend_export.py` before approving, as it is short on purpose.
- **The engine is downloaded code.** The launcher runs only the release whose fingerprint is pinned in `scripts/aicfo_spend.py`. Changing the version means changing the fingerprint in a reviewed pull request.
