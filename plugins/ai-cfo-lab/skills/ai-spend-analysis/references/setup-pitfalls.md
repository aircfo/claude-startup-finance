# Setup pitfalls

Every way setup went wrong during the first real install (one Team-plan org,
October 2026), what it looked like, why it happened, and what now catches it.
`doctor.py` encodes these as checks; the check id is in the last column. Add a
row whenever a new install hits something new, and give it a check.

| # | What the operator saw | Root cause | Caught by |
|---|---|---|---|
| 1 | API cost near $0 although the team uses the API daily. No error anywhere. | Ramp's AI-spend connection held an Admin key for a *different* Console organization than the one carrying the traffic. Ramp validated the key and reported success. | `admin_key_org` prints the key's org; Claude compares it with Ramp's connection (SKILL.md → Doctor) |
| 2 | The Claude Code tab listed API keys but no people. | The Admin key belongs to the Console (developer-platform) org; the claude.ai Team workspace is a separate org, which no Console key can see. | `claude_code_visibility` |
| 3 | The unattended export was refused, twice, even in `dontAsk` mode with four allowed tools. | Claude Code's safety checks don't let an unattended Claude session export per-person data from an Owner's claude.ai session. | Design: the export is the fixed script `fetch_surface_b_browser.py`; `export_login` checks it can sign in |
| 4 | "Input must be provided…" from a scheduled run. | `--allowedTools` takes a list, so a space-separated list swallowed the prompt that followed it. | `install_mac_job.py` writes the command; nobody types it |
| 5 | The test suite failed with no test output. | Node 26 no longer accepts a bare directory for `node --test`. | Documented command `node --test scripts/__tests__/*.test.js`; CI runs it |
| 6 | New settings (`dashboard_visibility`, sources) silently absent. | The workspace was scaffolded before those settings existed; scaffolding never overwrites config. | `config_complete` (+ `doctor.py --fix-config`) |
| 7 | Seats showed made-up people at template prices. | `config.example` seeds a sample roster of `@example.com` people; it stayed after the real org was configured. | `roster_real` |
| 8 | Seat cost was off by 33–50%. | Template seat prices ($30 / $150) were never replaced with the org's ($20 / $100). | `seat_prices_confirmed` |
| 9 | Everyone was "standard". | The bootstrapped roster leaves seat type blank, which means standard. | `roster_complete` (warns at zero premium seats) |
| 10 | "Where do I drop the key?" | The drop file's path wasn't in front of the operator when they needed it. | `admin_key` prints the exact path |
| 11 | The company roster had names but no emails; first names repeated; old inactive rows duplicated active people; contractors were listed as "Robin (Fractional PM)". | Rosters from HR tools rarely key on the claude.ai login email. | `match_roster.py` (matches, prefers active, reports every ambiguity instead of guessing) |
| 12 | Two departments that look like one ("People Operations" / "COGS - People Operations"). | Inconsistent labels in the source roster. | `roster_departments` (flags one-person departments) |
| 13 | Copying Ramp's answers to disk could silently drop a page or mistype a figure. | Ramp is reached through a connector, so a model writes its answers to file. | Integrity checks in `ingest_ramp.py` (count / per-model total) |
| 14 | A month could stay half-captured if the Mac was off on the 1st. | The export only covers the month containing yesterday. | Catch-up in `fetch_surface_b_browser.py`; `data_fresh` |

## Roles setup touches

Setup crosses three systems, each with its own admin. An operator who isn't
all three needs a hand-off; `doctor.py` groups its findings by who can fix them.

| Role | Needed for | Typical holder |
|---|---|---|
| **claude.ai Owner or Primary Owner** | Signing the export script in once (`--login`), finding the org id | Founder / CEO |
| **Console (platform.claude.com) admin** | Creating the Admin API key | Whoever opened the API account |
| **Ramp admin** | Connecting Anthropic in Ramp's AI-spend settings with the right Console org's key | Finance / Ops |
| **Operator** (anyone with the workspace) | Everything else: scaffold, roster, dashboard, scheduling | Ops |
