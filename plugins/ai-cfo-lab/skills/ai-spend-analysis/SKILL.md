---
name: ai-spend-analysis
description: >
  Where a company's AI spend went and where it's heading. Anthropic and OpenAI seats,
  extra usage and API spend go to people and teams, with this month's pace, next month's
  forecast and spike alerts. Built on Ramp: API spend and the people list come through
  the Ramp connector, which holds the Admin keys. Fires on "run the AI spend analysis",
  "refresh the AI spend dashboard", "how much are we spending on AI / Claude / ChatGPT",
  "are we on pace this month", "set up AI spend tracking", or a scheduled daily refresh.
  Read-only; it drafts alerts and never sends them.
---

# ai-spend-analysis

This skill gathers the inputs and shows the answers. The math is done by the open-source
engine, [aicfo-spend-analysis](https://github.com/aircfo/aicfo-spend-analysis), which runs
without Claude. Its design is in that repo's `docs/design.md`; read it when a number needs
explaining.

Throughout: `$SKILL` is this skill's folder, and `$FOLDER` is the company's folder. That
folder holds the settings, the people file, every saved download (`raw/`) and every
output (`out/`). It must be outside any git repo.

**Run the engine only through the launcher.** It downloads the pinned engine release
into `$FOLDER/.engine/` once, checks its fingerprint, and runs it:

```
python3 "$SKILL/scripts/aicfo_spend.py" "$FOLDER" <command> [arguments]
```

It needs Python 3.10 or later. If `python3` is older (macOS's built-in one is 3.9), say so
and stop; don't install anything else. Commands: `init`, `settings`, `save`, `report`,
`pace`, `forecast`, `dashboard`; each has `--help`.

## Which path

- **There's no `aicfo-spend.json` in the folder:** run Setup.
- **Otherwise, a refresh was asked for or a scheduled task is running:** run the Daily refresh.
- **Otherwise, a question about the numbers:** answer it from the latest
  `out/<month>/dashboard.json` and `report` output, and refresh first if the latest
  download is more than a day old.

## Setup

Talk to the operator one step at a time; they mostly confirm.

1. **Folder.** Agree on a folder outside any git repo, such as `~/Desktop/AI-Spend`.
   Then run `init --company "<name>"`.
2. **Ramp.** Call `ramp_get_ai_token_spend_connections`. Each provider whose Admin key is
   plugged into Ramp is listed there. If Anthropic or OpenAI is missing, the **Ramp admin**
   adds the key in Ramp's AI spend settings. Offer a short message the operator can
   forward, and carry on.
3. **Seats.** For each vendor, ask for each seat type's monthly price and how many were
   bought. Examples: Claude Team standard and premium, or ChatGPT Business. Write them to
   `aicfo-spend.json` as `seats.<vendor>.<seat type> = {"price_usd": …, "bought": …}`, with
   vendors `anthropic` and `openai`. Check the file with `settings`.
4. **People file.** `people.csv` has one row per seat held: `email`, `vendor` and
   `seat_type`. Fill `name` and `team` only for someone Ramp doesn't know. Build it from the
   admin member lists the operator exports from claude.ai and ChatGPT. **Ask about anything
   unclear; never guess a seat type or a team.** A wrong guess files someone's spend under
   the wrong team.
5. **Who sees what.** `visibility` is `"team"` by default: shared outputs show teams, and
   teams under 3 people fold together. Set `"person"` only when the operator says the
   company has decided everyone with the link may see each person's spend. Never change
   it yourself.
6. **Extra usage.** On Claude Team, each person's extra usage comes only from the claude.ai
   spend export. There are two ways to get it:
   - **By hand:** claude.ai → Settings → Analytics → Export spend report.
   - **Daily on a Mac:** the fixed script `scripts/fetch_spend_export.py`. A claude.ai Owner
     signs it in once with `--login`.
   **The export only reaches back 90 days, so a month that isn't saved within 90 days is
   lost.** Save last month whole and this month so far (step 2 of the refresh).
7. **First refresh**, then **schedule it**. Run the Daily refresh. Its first run also saves
   last month whole: Ramp's per-key spend and vendor totals for last month's 1st to its last
   day, so the forecast and the change from last month have something to stand on. The
   first run also creates the page; tell the operator it's private until they share it.
   Then offer a Cowork scheduled task: daily, working in `$FOLDER`, with the instruction
   "Run the ai-spend-analysis daily refresh in this folder." Say plainly that it runs only
   while this computer is on. Show the task's settings and get a yes before creating it.

## Daily refresh

Every source is a day behind, so a refresh covers **through yesterday**. The month to refresh
is the one that contains yesterday, so the run on the 1st closes out the month just ended.
Below, `<first>` is that month's 1st, `<yesterday>` is yesterday and `<today>` is today, all as
`YYYY-MM-DD`.

1. **Save Ramp's numbers.** Follow every page and join the pages' lists into one. Copy
   values exactly as Ramp returned them: the engine checks the files, and Ramp's own totals
   check your copy.
   - **API spend by key:** call `ramp_api_key_spend` with `from_date` = `<first>` and
     `to_date` = `<today>`. Ramp's `to_date` is exclusive, so this reaches through
     yesterday. Use page size 100 and no status filter, because a locked key can still have
     spent this month. Write only the keys whose `estimated_cost.value` is above 0, and only
     the fields the engine reads: `name`, `provider`, `owner` (just its `email`), `tags`
     (just the `Department` one) and `estimated_cost`. Write it as `{"data": [ … ]}` to
     `$FOLDER/inbox/ramp-api-keys.json`, then run
     `save ramp-api-keys --start <first> --end <yesterday> --file "$FOLDER/inbox/ramp-api-keys.json"`.
   - **Ramp's total for each vendor:** call `ramp_get_ai_token_spend_aggregates` with
     `metric` = `cost`, `group_by` = `["provider"]`, `providers` = `["ANTHROPIC", "OPENAI"]`,
     `rollup` = `all`, `start_at` = `<first>` and `end_at` = `<today>`. Write each row's
     `provider` and `total_cost` as `{"cost": {"data": [ … ]}}` to
     `$FOLDER/inbox/ramp-provider-totals.json`, then run
     `save ramp-provider-totals --start <first> --end <yesterday> --file "$FOLDER/inbox/ramp-provider-totals.json"`.
     Spend this total has beyond the keys shows as Unassigned, "API spend not tied to a
     current key". The usual cause is a key deleted or rotated during the month.
   - **People:** only on the 1st, on Mondays, and at setup, because teams change slowly and
     the list is the longest answer. Call `ramp_list_users` (page size 100), write
     `{"users": [ … ]}` with each user's `email`, `first_name`, `last_name`,
     `department_name` and `is_inactive` to `$FOLDER/inbox/ramp-people.json`, then run
     `save ramp-people --start <today> --file "$FOLDER/inbox/ramp-people.json"`.
   - Delete each inbox file once its save succeeds.
2. **Save any new spend export.** If the Mac script ran, it has already saved its export.
   If the operator dropped an export in `$FOLDER/inbox/`, ask which days it covers. Then run
   `save claude-spend-export --start <its first day> --end <its last day> --file <it>`.
   It must start on a month's 1st and stay within one month.
3. **Run the numbers.** Run `report <month>`, `pace <month>` and `dashboard <month>`. On the
   1st to the 3rd, also run `report` for the month before, since it has just closed.
4. **Update the page.** Run `python3 "$SKILL/scripts/build_dashboard_page.py" "$FOLDER" <month>`.
   It writes `$FOLDER/out/<month>/dashboard.html`, a self-contained page holding the
   engine's numbers, so nothing is retyped. Publish that file with the Artifact tool:
   - **No `$FOLDER/dashboard-url.txt` yet:** publish it as a new page with the icon `chart`,
     and write the link the tool returns into `$FOLDER/dashboard-url.txt`.
   - **Otherwise:** read the page at that link first, then publish the file to that link
     (`url`), so the link stays the same every day.
   The page is private until the operator shares it from its Share menu. Never share it
   yourself. It shows exactly what the `visibility` setting allows.
5. **Show the results.** Give the page's link, then lead with the pace line, then the
   alerts, then the notes, and finish with the team table from `report`. Present the alerts
   as drafts: **never send anything**. If a scheduled task is running, write the same
   summary to `$FOLDER/out/<month>/summary.txt` and stop.

**When something fails, say so in the summary's first line.** That includes a Ramp call,
a save, or a missing export. Never fill a gap with a guess. A save that refuses a file says
why; fix the cause, don't edit files in `raw/`.

**If `report` says a vendor's keys add up to more than Ramp's total,** the per-key copy has a
mistake. Call `ramp_api_key_spend` again, write the file again, and save it again; the newer
save counts.

**If API spend reads near $0 while people use the API every day,** Ramp's connection may
point at a different Anthropic Console organization than the one in use. The Ramp admin
re-adds the right organization's Admin key in Ramp.

## Hard rules

- **Read-only** on every financial system. Never change seats, plans, billing, keys or settings.
- **The tool never handles a key.** Ramp holds the Admin keys. If a key is pasted in chat,
  don't use or store it. Tell the operator to revoke it, because it's now exposed, and that
  keys go into Ramp's AI spend settings instead.
- **Claude never drives claude.ai.** The spend export comes from the export button or the
  fixed script, which a claude.ai Owner signs in once. An unattended Claude session isn't
  allowed to export per-person data from an Owner's session.
- **Visibility is the operator's call**, as Setup step 5 says. Anyone who can open a shared
  output can download its rows.
- **Drafts only.** Alerts and summaries are written for a person to send.
- **Company data stays in `$FOLDER`.** Never copy it into a repo or anywhere else.
- **Run only the pinned engine**, through the launcher. Never edit files in `raw/` or `.engine/`.

## Files

| File | Purpose |
| --- | --- |
| `scripts/aicfo_spend.py` | The launcher: downloads the pinned engine once, checks its fingerprint, runs it |
| `scripts/fetch_spend_export.py` | The claude.ai spend export on a Mac, by a fixed script (`--login` once, then daily) |
| `scripts/build_dashboard_page.py` | Puts the engine's `dashboard.json` into `dashboard_page.html`, giving one self-contained page to publish |
| `scripts/dashboard_page.html` | The page: the month's verdict, where the money went, Unassigned and how to place it, the change from last month, and next month |
| `scripts/__tests__/` | Offline tests for the scripts: `python3 -m unittest discover -s scripts/__tests__` |
| `references/security-overview.md` | One page for an IT or security reviewer: what data goes where, and who can see it |
