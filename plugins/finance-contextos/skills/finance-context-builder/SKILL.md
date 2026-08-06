---
name: finance-context-builder
description: Build the company's ContextOS — a folder (default on the Desktop) holding a finance-profile.md semantic map and an account map drafted from the QuickBooks Account List, verified against the live books before handoff. QuickBooks is the backbone; Stripe, Ramp, and Mercury enrich the context when connected. It builds from the systems first (after a light invite to share any docs on hand), drafts the account map for review, then asks the finance pro only the targeted questions their connectors can't answer. Use on first-time setup or to refresh, or when someone says "build my ContextOS," "set up the finance plugin," "build my finance context," "build my finance profile," "map my accounts across systems," "add this to my ContextOS," or when another finance workflow can't find finance-profile.md.
---

# Finance Context Builder — build the company's ContextOS

Produce the **ContextOS**: a folder the finance pro can open anytime (default `~/Desktop/ContextOS/`) holding `finance-profile.md` (the semantic map), `account-map.csv` (how every account classifies), the source docs they've shared, and a changelog. Every other finance workflow reads the profile first, so Claude reasons about the company's finances with one shared model — grounded in how *this* company actually reports. **A ContextOS isn't done until it ties** — the build ends by verifying the model against the live books (step 12), never on "here are your files."

## What this produces
An **ContextOS folder** (default `~/Desktop/ContextOS/`; confirm the location with the user on the first run):

```
~/Desktop/ContextOS/
├── finance-profile.md     # the semantic map (narrative + summary) — the main read
├── account-map.csv        # every GL account × its classification — the editable source of truth
├── context/               # source docs the pro shares (written here after they're ingested)
└── CHANGELOG.md           # dated log of what changed each run
```

Each finance workflow reads this profile at its own Step 0 — so it loads when finance work actually runs, not globally on every session. The profile follows the **14-section template** (schema below; a fill-in skeleton ships in `templates/finance-profile-template.md`) and is populated from three input layers:
- **Business context (from the pro)** — what's true and unique about this company, captured from whatever docs and notes they share.
- **Reporting framework** — the account map (below).
- **Money-flow graph (discovered)** — how each Mercury account, Ramp clearing account, and Stripe payout/revenue stream maps onto a QuickBooks GL account.

`account-map.csv` is the canonical, spreadsheet-editable classification; `finance-profile.md` is the human-readable layer that **references** it — never duplicate the full per-account table in the profile.

## Principles
- **Systems first; humans for the "why."** Connectors alone fill most of a ContextOS — the structure, the amounts, the vendors, the rails. What they can't fill is definitions, policies, and intent. So build from the systems first, then ask the human *targeted* questions generated from the build's actual gaps — never open-ended questions up front, and never a question the books can answer.
- **Draft, then confirm.** Build a *first draft* of the account map from the QuickBooks Account List, then have the human review it — never finalize a mapping without confirmation.
- **Fill or placeholder — never guess.** Draft the profile from what you actually know (the context docs + the system analysis); mark every gap with an explicit `[PLACEHOLDER: …]` and surface it for the human — never invent a value to fill a section.
- **QuickBooks is the source of truth for the account list and the amounts.** The map decides how those accounts classify and roll up.
- **Read-only** against every connector.
- **Degrade gracefully on partial access.** A connector that's connected but blocks some endpoints (a permission/scope error) — or returns more data than fits in one read — is *partial*, not failed: read what you can, page large pulls, and mark the rest as an explicit placeholder. Never hard-fail the whole run on one bad endpoint.
- **Expect connections to expire.** Connector sessions lapse after a few idle days — on a refresh run, a connector that worked last time may ask the user to sign in again. That's normal, not a bug: say so ("your QuickBooks session expired — you'll see a quick re-sign-in"), let them re-auth, and continue. Never treat a re-auth prompt as a failed connector.
- **Always pass explicit date ranges.** On any dated report pull (balance sheet, P&L, trial balance), pass *both* a start date and an end date — some connectors silently ignore a lone end date and return the wrong period. If a number looks implausible, re-pull with the full explicit range before trusting it.
- **The folder is the finance pro's.** Keep it human-readable and easy to open; never move or delete files in `context/` without asking.

## Build sequence

### 0 · Orient the user first (before doing anything)
This is a guided, **~15–20 minute** setup with two quick review points. Open with a one-message roadmap so the pop-ups and the wait don't feel random, then begin:

> "I'll build your ContextOS — about 15–20 minutes. The path: ① pick a folder to save everything → ② connect QuickBooks (one sign-in pop-up; if you have other finance connectors installed I'll check those too) → ③ share any docs you have handy (optional) → ④ I read your books and draft your account map; you rule on just the judgment calls and we lock it → ⑤ I draft your finance profile and show you what your systems filled on their own → ⑥ a few targeted questions only you can answer → ⑦ I verify the model ties to your live books. You can stop and resume anytime. Ready?"

Then keep the user oriented as you go — a one-line "here's where we are / here's what's next" at each stage beats long silent stretches, especially while pulling a large chart of accounts or drafting the map.

### 1 · Locate or create the ContextOS folder
On the first run, propose `~/Desktop/ContextOS/` and confirm it (let the user pick another spot); create it with the structure above. On later runs, use the existing folder — including folders created by earlier versions under the old default name `~/Desktop/airCFO Finance Context/` (check the pointer file first, then both default paths). An old-named folder is fully valid; never rename or move it without asking.

**In Claude Cowork, you can only write to a folder the user has granted the session access to — confirm this *first*, before investing the next 15 minutes.** Create the folder and immediately write a small file to it (the `LOCATION.md` below doubles as the write-test). If that write fails with a permission error, stop right here and ask the user to grant a folder via Cowork's *"Work in a folder"* control, then retry — do not move on to connectors or the account map until a write has actually succeeded. Never run all the way to the end only to silently fail to save the output.

**Then persist a lightweight pointer**, so future workflows can find the profile without loading it into every session. Write the machine-readable pointer to the current workspace (if writable), and offer to add a short note to the workspace `CLAUDE.md`:

- **`.aircfo-finance-context.json`** in the current workspace:

  ```json
  {
    "contextFolder": "/absolute/path/to/ContextOS",
    "financeProfile": "/absolute/path/to/ContextOS/finance-profile.md",
    "accountMap": "/absolute/path/to/ContextOS/account-map.csv",
    "lastUpdated": "YYYY-MM-DD"
  }
  ```

- **`CLAUDE.md` pointer — only with the user's OK.** Adding to `CLAUDE.md` changes their workspace instructions, so ask in plain English first:

  > "I can add a tiny pointer to this workspace's CLAUDE.md so future finance workflows know where your finance profile lives. I will not import the profile itself, so it will not load into every session."

  If they agree, add (or update) a bounded block so re-runs replace it instead of duplicating:

  ```md
  <!-- airCFO Finance Context:start -->
  ContextOS folder: /absolute/path/to/ContextOS
  Finance profile: /absolute/path/to/ContextOS/finance-profile.md
  <!-- airCFO Finance Context:end -->

  (Keep the `airCFO Finance Context` marker comments exactly as-is — they're the bounded-block
  identifier existing installs already carry, so re-runs keep replacing instead of duplicating.)
  ```

  If they decline, skip the `CLAUDE.md` write — the JSON pointer and the default folder still let workflows find the profile.

- **Never add an `@import` of the full profile** to `CLAUDE.md`. That would load the entire profile into every session — exactly what the pointer avoids.

Also drop a human-readable `LOCATION.md` inside the ContextOS folder noting its own path — a convenience for the user. Don't rely on it for discovery: workflows find the folder via the pointer or the default path, not this file.

### 2 · Connector preflight — see which systems are live
**QuickBooks is the build; everything else is enrichment.** This plugin ships only the QuickBooks connector. Stripe, Ramp, and Mercury tools are present only if the **all-systems-go** plugin (or another connector) is also installed — detect which connectors exist from the available tools, and only mention the ones that do. **Don't ask the user to list their systems.**

**Tell the user what's coming before you trigger anything:** "I'll connect QuickBooks now — you'll get one sign-in pop-up. Sign in with your own QuickBooks login; access is read-only." (If other finance connectors are installed, add: "I'll also check [Stripe/Ramp/Mercury] — authorize the ones you use and just close/decline the rest.")

Then check each present connector by running **one lightweight read** (read-only). **Do QuickBooks first** — it's the backbone, so confirm it before anything else: read company info and show the user the company name you got back ("Connected to QuickBooks: *Acme, Inc.*") so a wrong connector or wrong company is caught immediately. Then, if installed: Stripe (account/balance), Ramp (current user), Mercury (accounts).

If a connector isn't authorized, its read surfaces the provider's browser sign-in. If a sign-in **fails to complete** (window won't load, "can't connect to the server," or the user closes it), don't wait on it — mark the connector **Not connected**, note it, and move on; the user can reconnect and re-run later. **Never block setup on a missing or failed connector.**

**Use the QuickBooks connector bundled with this plugin — the airCFO-operated server.** If the environment also exposes a separate Intuit/QuickBooks connector, the account list and the amounts must come from the airCFO connector, not the other one; if you can't tell which one answered, confirm the company name with the user before drafting anything.

A connector can also be **connected but partial** — it answers some reads and returns a permission/scope error on others (e.g. Ramp returning *"You do not have permission to view checking accounts"*). Mark it **Connected (partial)**, use what you can read, and record the blocked parts as explicit placeholders and open questions.

Show a short status table and the impact of anything missing:

| Connector | Status | Impact |
| --- | --- | --- |
| QuickBooks | Connected | I can draft the account map and reporting framework. |
| Stripe | Connected | I can map subscription/customer revenue rules. |
| Ramp | Not connected | Vendor/spend rules will stay placeholder. |
| Mercury | Connected | I can map cash accounts and runway cash. |

Then continue with the connected systems. Missing systems become explicit placeholders and open questions, not guesses. **QuickBooks is the backbone** — it owns the account list everything else maps onto — so if QuickBooks isn't connected, say so plainly and focus on what the other systems can still provide.

### 3 · Invite docs — lightly (the conversation comes later)
**Systems fill the "what"; humans fill the "why" — and the "why" questions can't even be written until the books have been read.** So don't interview the pro up front. Offer one quick chance to share *artifacts* — a reporting package teaches you their department names and conventions before you draft the map — and move on:

> "One optional thing before I read your books: if you have anything handy — your monthly reporting package, board deck, a close checklist, a policy doc — drop it here now. It teaches me your department names and conventions before I draft your account map. If not, no problem: I'll read your books first and later ask you only the questions they can't answer."

Read whatever they share, then **persist it**: save the source material (and a short distilled summary) into the `context/` subfolder, and fold the salient points into the relevant profile sections as you draft, citing the saved file. `context/` is a *record of what's been ingested* — the pro never has to manage it. If they volunteer business context in conversation, take it — but don't prompt for it here; the real conversation is the targeted intake in step 10, generated from the build's actual gaps. If they share nothing, proceed immediately.

### 4 · Pull the QuickBooks Account List
Get company info (legal name, fiscal year, accounting basis, reporting currency) and run the **Account List** report / chart of accounts. For every account, capture: the QuickBooks internal **Id** (the map's primary key — it survives renames and renumbers), number, name, **Type**, **Detail Type**, **Active** flag, the account **description** (if any), the **parent account** (`ParentRef` and the parent's name — needed for department inference), and balance. This is what the draft is built from.

**Large charts of accounts need paging.** A real startup chart can run to several hundred accounts, and pulling them all in one call can exceed the connector's output-size limit and error out (a ~250-account chart can return well over 100K characters). Pull the list in pages — step through with the query's `startposition` / `maxresults` (around 100 accounts at a time) and assemble the rows as you go. If a page still errors on size, halve the page size and retry. Don't abandon the chart of accounts because the first full pull was too big.

### 5 · Draft the account map
Write one row per GL account to `account-map.csv` in the ContextOS folder. The full schema and vocabularies live in **`templates/account-map-spec.md`** — read it before drafting. Columns: `gl_account_id, account_number, account_name, account_type, detail_type, parent_account, active, expense_category, department, cf_section, cf_line, tags, mapping_status, review_note, confirmed_by, confirmed_date`.

**The mental model (from the spec): the map is a cube, not a tree.** Each account carries independent axes — Class (derived from `account_type`), `expense_category` (what kind of money), `department` (whose money), `cf_section`/`cf_line` (how its change moves cash), and `tags` (cross-cutting analysis groups). Deliverables pivot these axes into whatever hierarchy they need; the map never hard-codes an outline.

**Ledger facts — straight from QuickBooks, no judgment:** `gl_account_id` (the internal Id — the primary key), `account_number`, `account_name`, `account_type`, `detail_type`, `parent_account`, `active` — all verbatim. These columns are script-territory: refreshes overwrite them; humans never edit them.

**`expense_category` — every account gets one**, from the spec's fixed vocabulary (Subscription revenue, Hosting & infrastructure, Payroll & benefits, Software & tools, Deferred revenue, …). Seed it by rule and record how confident the rule was:
1. **`detail_type` lookup** — many detail types map cleanly (Payroll-type → `Payroll & benefits`, Advertising/Promotional → `Marketing & advertising`, Prepaid → `Prepaid expenses`). High confidence → `mapping_status: auto`.
2. **Account-name keywords** — hosting/AWS/GCP → `Hosting & infrastructure`; legal/audit → `Professional services`; recruiter/ATS → `Recruiting`; etc. Reasonable confidence → `auto`.
3. **Can't tell** — assign the closest category, set `mapping_status: needs-review`, and say why in `review_note`. Never leave the category blank and never force a confident-looking guess.

**`department` — value kind follows the account's Class** (see the spec): revenue accounts → product / revenue stream (often blank for single-product companies); COGS → cost-of-revenue function (Infrastructure / Support / Services); Expense → an OpEx department; Bank accounts → `Operating cash` or `Treasury`. For OpEx, classify to the team that owns the spend, working down this list and stopping at the first that fits (lean on the pro's context docs — their reporting package usually names the canonical departments):
  1. **In the account name** — a department after a dash or an embedded keyword ("Salaries & Wages — Engineering" → `Engineering`).
  2. **Parent account** — a sub-account inherits its parent (header) account's department when the parent reads like one (children of a "Marketing" parent → `Marketing`).
  3. **Judgment from what the account is for** — advertising, paid media, events, agencies, content, brand, demand gen → **Marketing**; commissions, CRM, sales tooling → **Sales**; cloud/engineering tooling in OpEx, R&D → **Engineering**; support/success tooling → **Customer Success**; rent, insurance, legal, audit, bank fees, company-wide software → **G&A**.

  **G&A is a legitimate home** for genuinely general-and-administrative accounts. Set `needs-review` (with the reasoning in `review_note`) rather than guessing when an account is irregular — and don't use G&A as a catch-all. Other Income / Other Expense and non-cash balance-sheet accounts take no department.

**`cf_section` + `cf_line` — balance-sheet accounts only**, from the spec's line list. Mostly deterministic from account type (AR → Operating / Change in accounts receivable; Fixed Asset → Investing / Purchases of fixed assets; Credit Card → Operating / Change in credit cards; deferred revenue → Operating / Change in deferred revenue; SAFEs & notes → Financing / Equity issuance). Cash accounts and retained earnings stay blank — they're the statement's subject and the net-income roll, not lines. The judgment call to surface: a **treasury / investment** account QuickBooks lists as a current asset that belongs under **Investing** — flag it `needs-review`.

**`tags` — from the spec's registry only** (`mrr`, `cac`, `contra-revenue`, `pass-through`, `clearing`, `non-operating`). The two that need care on a first draft: tag `mrr` on recurring-revenue accounts *only after* confirming with the pro what they count as recurring (this defines their P&L-based MRR/ARR); tag `clearing` on anything that should net to zero (payroll holding, processor clearing, unapplied-cash system accounts) — the anomaly-sweep workflows key off it.

**`mapping_status` is the honesty column:** rule-drafted rows are `auto`, judgment calls are `needs-review` (with `review_note` saying why), and nothing is `confirmed` until the human signs off in step 6. Downstream workflows disclose any non-confirmed rows they relied on — so the statuses are load-bearing, not decoration.

### 6 · Review the draft with the human, then lock the map (the gate)
**Don't make the user read all N rows** — a real chart has hundreds of accounts; only the `needs-review` queue needs their eyes. Say so up front ("Most of your ~250 accounts mapped by rule — I only need you on the few I had to judge"), then present the map by `mapping_status`:
- **`auto`** (rule-mapped: verbatim ledger facts, clean `detail_type` → category seeds, deterministic `cf_section` / `cf_line` defaults) — summarize as a count ("228 accounts mapped directly"), don't enumerate.
- **`needs-review`** — present **compactly** (grouped, ideally a short table showing each row's `review_note`): the `expense_category` and `department` judgment calls (how each was derived — name, parent, or judgment), any `cf_section` call (e.g. treasury/investment under Investing), the proposed `mrr` tag set (this defines their MRR — make them say yes), and anything whose name fights its type.

On sign-off, mark the reviewed rows `confirmed` with `confirmed_by` / `confirmed_date`, and clear their `review_note`. The pro can also confirm the `auto` rows wholesale ("the rest look fine") — record that the same way. Don't finalize until the human has ruled on the judgment calls; their corrections go back into `account-map.csv` — the full map stays in the folder for spreadsheet editing anytime.

**End the gate on a lock milestone, and say it:** "Your account map is locked — all N accounts confirmed." The lock is what makes the map the live extraction layer every downstream deliverable trusts. Residual *books* questions surfaced during review (an odd reserve, legacy accounts worth deactivating, a reclass candidate) go to profile §13 Open Questions — they're bookkeeping follow-ups, not mapping blockers; never hold the lock hostage to them. If the pro genuinely can't rule on a row yet, it stays `needs-review` and the map locks around it — downstream workflows already disclose reliance on non-confirmed rows.

### 7 · Map the other systems onto the GL (money-flow graph)
For each connected system, bind its money containers to GL accounts (match on names, last-4, amounts; confirm anything low-confidence):
- **Mercury** — accounts (operating vs treasury, name, last-4, balance) → the QBO bank GL account each represents; mark which count as cash for runway.
- **Ramp** — the funding/clearing account → its QBO liability/clearing account; how spend categories roll up to expense accounts; the top recurring vendors. If Ramp blocks the business/treasury/checking-account reads with a permission error (a scope the user didn't grant), map what you *can* see — card spend and vendors — and leave the funding/treasury mapping as a placeholder and open question.
- **Stripe** — the payout destination → which Mercury account → which GL account; how gross revenue, processing fees, and refunds book; the recognition method and treatment of annual prepays, coupons, and trials.

### 8 · Pin the mechanical conventions
Pin what the systems (and any step-3 docs) can actually state: fiscal year, accounting basis (cash/accrual), reporting currency, and the internal-transfer topology observed in the books (transfers between own accounts — excluded from burn). The *human-held* conventions — the materiality threshold, the MRR and revenue-recognition definitions, the close cadence, the treasury-vs-operating cash policy — are intake questions (step 10), not things to capture here: don't guess them, and don't run a mini-questionnaire now. If a context doc already answered one, record it with the doc cited and skip the question later.

### 9 · Draft the profile from the template (fill what you know, placeholder the rest)
Start from the **finance-profile template** (`templates/finance-profile-template.md`; the 14 sections are detailed under the schema below) and write a *first draft* of `finance-profile.md`. Fill every section you can from two sources: the **context docs** the pro shared (step 3) and the **system analysis** (steps 4–8 — the account map, the money-flow graph, and the pinned conventions).

Wherever you don't yet know something, **don't guess and don't silently drop the line** — leave an explicit placeholder so the gap is visible:

> `[PLACEHOLDER: <what's needed, and why it matters>]`

A section may come out fully filled, partly filled, or all placeholder — that's expected on a first run; the profile fills in over time.

### 10 · Report card, then targeted intake (the gate before finalizing)
Two moves: show what the systems filled on their own, then ask only what they can't answer.

**First, the connector report card** — a compact in-session readout (not a file), one row per profile section: *filled from your systems · filled from your docs · needs you*. Frame it as the win it is: "Your connectors filled most of this on their own — here's the short list only you can answer." This readout is what makes the intake feel targeted instead of like a questionnaire; every remaining gap on it is visibly something no connector could know.

**Then run the rulings block in the session (~7 minutes).** Generate it from *this company's* build residue — the `needs-review` rows that survived the map lock plus the §13 open questions — following the Block 1 shapes in `templates/intake-questions.md` (the identity check, the cash-perimeter ruling, the odd-account walkthrough, the unlabeled bucket, the unexplained number, the invisible rail). Each is a 30-second answer that unblocks automated reporting; without it, every future report has to hedge. Fold each ruling into the profile and map immediately, and never ask for a number that's already in the books.

**"I don't know" is a valid answer.** When the pro doesn't know offhand ("my controller books those"), record *who does* and move on — the item becomes an open question with an owner, and downstream deliverables hedge that section rather than block on it. Never loop on an unanswerable question.

**Offer the rest of the intake (Blocks 2–5) as the take-away.** KPI definitions, plan and forecast, cadence and materiality, tacit knowledge — the full timeboxed ~30-minute set in `templates/intake-questions.md`, where every answer lands in a specific profile section. They can keep going now if they have the time, or take it to whoever owns the numbers and bring back answers ("add this to my ContextOS"). Drop any question the build or their docs already answered — never re-ask.

Anything still unfilled after this is mirrored into **Open Questions** (§13) with a suggested next step, so the uncertainty stays visible. Placeholders stay in the file — nothing gets silently assumed.

### 11 · Finalize & write the ContextOS
- Write `finance-profile.md` and `account-map.csv` into the folder; make sure the docs the pro shared are saved in `context/`. Remaining placeholders stay in the file and are listed in Open Questions.
- Confirm the pointer is current: update `.aircfo-finance-context.json` (`lastUpdated`) and the `CLAUDE.md` block if one was added.
- Append a dated entry to `CHANGELOG.md` describing what changed and what's still open.
- Record provenance (§14): as-of date, connectors read, docs ingested, and which sections remain placeholder.

### 12 · Prove it ties (ground-truth check), then hand off
**A ContextOS isn't done until it ties.** Don't end on "here are your files" — end on **evidence the model is right**. Run a quick tie-out of the freshly built context against the live systems, picking the 2–3 checks the connected systems support:

- **Cash tie (Mercury ↔ QuickBooks):** for each Mercury account bound in the money-flow graph, compare the live Mercury balance to the mapped QuickBooks bank-account balance as of the last close date. An exact tie is the headline; a difference should be explainable (uncleared items, timing since close) or it becomes an open question.
- **Revenue coverage (account map ↔ QuickBooks):** pull last full month's P&L from QuickBooks and re-total revenue by summing every account the map classes as Income (`account_type: Income`, any `expense_category`). The two must match to the penny — this proves the map covers every income account, not most of them. If any revenue accounts carry the `mrr` tag, also play back the tag-based MRR total as a sanity check on the tag set.
- **Runway-cash sanity (profile ↔ human):** total the accounts the profile counts as runway cash and play it back: "By your profile's definition, runway cash is ≈ $X across these N accounts — does that match your mental model?"

Present the results as a compact tie-out table — *check · source A · source B · difference · verdict* — using a computation step for the arithmetic, never eyeballed. Grade every check with the three-word vocabulary: **tie** (exact), **explained variance** (a difference whose cause you state unprompted — uncleared items, timing since close), or **wrong**. A confidently-presented wrong number is the failure mode that matters most — if one appears, say so plainly and fix the mapping before handing off; never reframe a wrong as an explained variance after the fact. Every unexplained difference goes into Open Questions (§13) with a suggested next step; never soften or hide a miss. A found discrepancy is the feature working, not the setup failing — say so.

Then **hand off.** Close by confirming they're set up and verified: "Your ContextOS is built and it ties to your live books." If the All Systems Go plugin's workflows are installed, suggest one next ("try *'what's our runway?'* or *'give me board metrics for last month'* — they'll use this profile"); otherwise mention that installing **all-systems-go** from the same marketplace adds those workflows plus Stripe/Ramp/Mercury enrichment. If sections are still placeholder, add one line that those fill in as they share more.

## Updating & adding context over time
This skill is **build-or-refresh** — run it again anytime to refresh:
- **New context anytime** — the pro shares more in the session (or says *"add this to my ContextOS"*); ingest it, persist it to `context/`, fold it into the relevant profile sections (**replacing any matching placeholders**), and note it in the changelog.
- **Refresh the map** — re-pull the Account List and diff against `account-map.csv` **on `gl_account_id`** (renames and renumbers update in place instead of looking like new accounts): overwrite the ledger-fact columns; draft genuinely new accounts as `auto`/`needs-review`; mark disappeared accounts inactive (never delete); **never overwrite a `confirmed` row's mappings** — flag a conflict for the human instead.
- **Always** append a dated `CHANGELOG.md` entry describing what changed, and update the profile's as-of date and the pointer's `lastUpdated`.

## The account map (schema)
`account-map.csv` lives in the ContextOS folder root (default `~/Desktop/ContextOS/account-map.csv`), one row per GL account, keyed on **`gl_account_id`** (QuickBooks' internal account Id). The full contract — column rules, the Expense Category / department vocabularies, the tag registry, the cash-flow line list, and the refresh workflow — is **`templates/account-map-spec.md`**; a blank-header template CSV ships alongside it.

`gl_account_id, account_number, account_name, account_type, detail_type, parent_account, active, expense_category, department, cf_section, cf_line, tags, mapping_status, review_note, confirmed_by, confirmed_date`

Three column groups:
- **Ledger facts** (`gl_account_id` → `active`) — verbatim from QuickBooks; refreshes overwrite them; humans never edit them. Class (Revenue / COGS / OpEx / below-the-line / balance sheet) is derived from `account_type`, never stored.
- **Reporting mappings** — `expense_category` (what kind of money, from the spec's fixed vocabulary), `department` (whose money; value kind follows Class), `cf_section` + `cf_line` (balance-sheet accounts only), `tags` (registry-controlled cross-cutting groups: `mrr`, `cac`, `contra-revenue`, `pass-through`, `clearing`, `non-operating`).
- **Governance** — `mapping_status` (`auto` / `needs-review` / `confirmed`), `review_note`, `confirmed_by`, `confirmed_date`. Confirmed rows survive refreshes untouched; workflows disclose reliance on non-confirmed rows.

## `finance-profile.md` schema
`finance-profile.md` is a **semantic control file, not a data dump** — it holds definitions, mappings, conventions, and judgment calls so every workflow reasons with the same financial brain. It *references* `account-map.csv` (never duplicates it). A fill-in skeleton ships in `templates/finance-profile-template.md`; draft from it, filling what you know and placeholdering the rest (steps 9–11). The 14 sections:

1. **Company Snapshot** — legal name, fiscal year, accounting basis (cash/accrual), reporting currency, current stage, primary business model, as-of date, connected systems read.
2. **Business Model** — plain-English how the company makes money (subscription / services / usage / marketplace / hardware / transaction fees / hybrid) and the main operating drivers (customers, units, headcount, usage, gross margin, sales cycle, seasonality).
3. **KPI Definitions** — the company's canonical definition for every metric it lives by ("when we say X, here's exactly how we calculate it"): e.g. revenue, bookings, billings, gross / contribution margin, gross / net burn, runway, CAC, LTV, active customers, retention, utilization, pipeline, ARR / MRR — whichever apply.
4. **Source-of-Truth Map** — which system owns which number (e.g. cash → Mercury, recognized revenue → QBO, subscription detail → Stripe, card/vendor spend → Ramp, payroll/headcount → payroll system or user-provided roster, forecast → planning tool), and which sources are authoritative vs. directional.
5. **Chart of Accounts / Reporting Framework** — points to `account-map.csv` (no full table): P&L categories, departments / cost centers, balance-sheet groups, cash-flow classifications, accounts needing review, and accounts intentionally excluded from certain metrics.
6. **Cash, Burn, and Runway Rules** — which bank accounts count as cash; whether treasury/investment counts as runway cash; gross-burn and net-burn definitions; internal-transfer exclusions; treatment of financing inflows; default lookback window; trailing-average vs. current run-rate.
7. **Revenue and Collections Rules** — how revenue is recognized; how collections differ from revenue; refund / credit treatment; deferred revenue; non-core revenue; AR / collections conventions; customer aliases across systems.
8. **Spend, AP, and Vendor Rules** — vendor aliases across Ramp / QBO; recurring-vendor list; one-time vs. recurring; card vs. bills vs. payroll; capitalization rules (if any); excluded / non-operating spend.
9. **People and Payroll Model** — headcount source of truth; departments; loaded-payroll assumptions; contractor treatment; commissions / bonuses; hiring-plan source.
10. **Planning and Forecast Assumptions** — current budget / forecast source; approved hiring plan; revenue-forecast logic; major planned investments; fundraising assumptions; board-approved plan vs. latest estimate.
11. **Reporting Cadence and Materiality** — monthly close cadence; board / investor cadence; materiality threshold; variance-explanation threshold; preferred output style.
12. **Known Exceptions and Judgment Calls** — the "don't rediscover this every time" list (e.g. "this savings account counts as runway cash"; "this vendor maps to COGS, not G&A"; "Stripe dashboard MRR ≠ board MRR because of trials/prepaids"; "this legal bill is one-time, exclude from run-rate burn").
13. **Open Questions** — anything unresolved, each with a suggested next step (this is where unfilled placeholders land, so uncertainty stays visible).
14. **Provenance and Changelog** — last updated, systems read, docs ingested, what changed, what still needs confirmation.

## Never
- Never store secrets, tokens, or full account numbers — names, last-4, and internal IDs only.
- Never write to a connected system.
- Never add an `@import` of the full profile to `CLAUDE.md` (or write the `CLAUDE.md` pointer without the user's OK).
- Never finalize the account map or overwrite human-confirmed rows without confirmation.
- Never move or delete files the pro placed in `context/` without asking.
