# Stage 1: Interview (build the handbook)

**Purpose:** fill in `CLAUDE.md` and every page in `handbook/` so Claude knows how this company
does its accounting. Systems and documents fill the "what." The person running this fills the
"why": definitions, policies, intent, and judgment calls.

Run it once to set up, and again any time to refresh. If the user names one page, work on
that page only.

## Principles

- **Systems first, people for the why.** Read the documents and connected systems before asking
  anything. Every question you ask should come from a real gap you found, never from a generic
  list, and never ask for a number that's already in the books.
- **Placeholder, never guess.** Fill what you can support. Mark everything else
  `[PLACEHOLDER: what's needed and why it matters]`. A half-filled page is a normal first run.
- **Cite your source.** After anything you fill in, note where it came from in parentheses, for
  example "(account list, read 2026-10-27)" or "(close-checklist.xlsx)".
- **"I don't know" is a fine answer.** Record who does know as an open question with an owner,
  and move on. Never loop on a question.
- **Read-only.** Read connected systems. Never write to them.
- **The folder belongs to the user.** Don't delete or move their files.

## Steps

### 0. Orient the user

Before doing anything, send one short message with the plan, so the wait and any sign-in
prompts make sense:

> "I'll build your finance handbook. It takes 30 to 60 minutes and you can stop and resume any
> time. The path: (1) confirm I can save to this folder, (2) check which finance systems I can
> read, (3) you share any docs you have handy (optional), (4) I read your books and draft every
> page, (5) I show you what I could fill on my own, (6) I ask you only the questions I couldn't
> answer, (7) I run a few checks to make sure the handbook matches your books. After that
> there's a short follow-up with whoever owns the numbers, and an optional internal website.
> Ready?"

Give a one-line status update at each step.

### 1. Confirm you can write here

Add a line to the Changelog in `CLAUDE.md`: "YYYY-MM-DD: handbook setup started." If the write
fails, stop and ask the user to give this session access to the folder. Don't continue until a
write has worked.

### 2. Check which systems you can read

Look at which finance tools are available in this session (accounting, bank, spend platform,
billing, payroll, shared drive). For each, do one small read to confirm it works and that it's
the right company: for the accounting system, read the company name and show it to the user.

Show a short table: system, status (connected, partial, not connected), and what that means for
the handbook. A missing system is never a blocker. Its sections stay as placeholders, or you
work from exports instead.

**No accounting system connected?** Ask for these exports, each with its date range, and save
them in `handbook/sources/`: the account list (chart of accounts), a trial balance and balance
sheet at the last month end, and a monthly P&L for the last three closed months. Use them in
step 4 and step 7 wherever these steps say "the books" or "the account list."

### 3. Invite documents (lightly)

> "If you have anything handy, drop it here now: a close checklist, policy docs, last month's
> reporting package, the prepaid or fixed asset schedule, a few finished workpapers. They teach
> me your conventions before I draft. If not, no problem: I'll read your books and ask only what
> they can't tell me."

Save what they share into `handbook/sources/` (create it if needed) and cite it when you use it.
Don't run an interview here. The real questions come in step 6, once you know what's missing.

### 4. Read the books and draft every page

Pull what the connected systems can tell you. Always pass an explicit start and end date on
dated reports, and page through large lists.

| Page | What to pull |
| --- | --- |
| `company-overview.md` | Company name, entities, fiscal year, accounting basis, currency from the accounting system. Which systems are in use, inferred from connected tools and from vendor spend (payroll provider, billing tool, spend platform). |
| `chart-of-accounts.md` | The full account list: numbering ranges, account types, departments or classes in use, inactive accounts that still have balances, accounts that look like clearing or holding accounts. A first draft of the Reporting rollups (revenue accounts, contra-revenue, interest and other non-operating accounts), marked for the user to confirm. |
| `accounting-policies.md` | Accounts that show recurring patterns: prepaid and accrued accounts with monthly activity, deferred revenue, fixed assets and depreciation. Note the patterns; the policies themselves come from the user. |
| `close-process.md` | When manual journal entries usually post relative to month end (a hint at the close calendar). The last closed period, if the system shows one. |
| `cash.md` | Every bank, card, and treasury account on the balance sheet, with the last four digits if they appear in the name. Statement timing for cards if it's visible. |
| `systems-and-data.md` | The connector status table from step 2. Data issues you noticed while reading (duplicates, clearing accounts that don't clear, uncategorized balances). Vendors or customers that appear under different names in different systems. |
| `workpaper-standard.md` | Nothing to pull: the standard ships ready to use. If the user shared finished workpapers in step 3, note where their conventions differ (tab names, file naming) and ask which to keep. The aging threshold for reconciling items stays a placeholder for step 6. |
| `metrics-and-reporting.md` | Only what the books show: revenue mix, gross margin, and average monthly cash out over the last three closed months, each computed in a calculation step. Definitions and targets stay placeholders; the user or the follow-up (stage 2, `follow-up-questions.md`) fills them. |

Write a first draft of each page and the "Company at a glance" section of `CLAUDE.md`. Fill
what you can support, cite it, and placeholder the rest.

### 5. Show the report card

One row per page: what was filled from systems, what was filled from documents, and what needs
the user. Frame it as progress: "Your systems filled most of this. Here's the short list only you
can answer."

### 6. Ask only what's left

Generate the questions from the placeholders and judgment calls you actually found. Group them,
ask the most valuable first, and keep each one answerable in under a minute. Typical shapes:

- **The ruling:** "Does [your treasury account] count as runway cash, or is it a reserve you
  don't touch?"
- **The odd account:** "Walk me through [the account whose activity is visible but whose
  purpose isn't]."
- **The catch-all:** "A lot of spend posts to [a parent or catch-all account]. Deliberate, or
  should it be split?"
- **The policy threshold:** "What's the dollar threshold for capitalizing an asset? For booking a
  prepaid? For an accrual?"
- **The close:** "Who does the close, what's the target day, and what does 'done' mean?"
- **The approvals:** "Who approves manual journal entries, and is there a dollar limit?"
- **Materiality:** "What size of month-over-month change deserves a sentence of explanation?"
- **Burn:** "What do you leave out when you talk about burn: transfers, fundraising, one-time
  costs?"
- **Rec aging:** "How old can a reconciling item get before it's flagged?" Answer goes in
  `workpaper-standard.md`.
- **The last question, always:** "What do you know about this business that the books would never
  tell me?" Answers go in "Things the books won't tell you" in `company-overview.md`.

Write each answer into the right page immediately. Offer to stop after the first 15 minutes and
keep the rest as open questions with owners. Questions about metric definitions, the plan, and
reporting can wait for the follow-up (stage 2), which is built for whoever owns the numbers.

### 7. Check the handbook against the books

Run a few checks and show them as a table (check, handbook says, books say, result). Use a
calculation step for any arithmetic; never eyeball it.

- Every bank and card account in `cash.md` exists in the account list, and every bank or card
  account in the account list appears in `cash.md`.
- Every account named anywhere in the handbook exists in the account list.
- Every account listed under "should always be zero" actually was zero at the last month end.
  (Report it; don't fix it.)
- Count of placeholders remaining, by page.

If you had neither a connected system nor exports, say which checks were skipped and why.

Anything that doesn't match becomes an open question in `CLAUDE.md`. A mismatch you find here is
the handbook doing its job, so say so.

### 8. Finish

- Update the "Last reviewed" line on every page you touched.
- Update `CLAUDE.md`: the at-a-glance section, open questions, and a Changelog line saying what
  was built and what's still open.
- During first setup, add "Setup stage 1 (interview) done. Next: follow-up." to the Changelog
  and offer the next stage as `SKILL.md` describes.

## Refreshing later

Run this again any time. A refresh skips the orientation message (step 0), logs "handbook
refresh started" instead of "setup started" in step 1, reruns steps 2, 4, 5, and 7, and in step 6
asks only questions that are new since the last run. Never overwrite something the user wrote or
confirmed without asking. If the user says "add this to the handbook," save the document in
`handbook/sources/`, fold what it says into the right pages, log it in the Changelog, and stop
there. A refresh doesn't lead into the other stages.

## Never

- Never write to a connected system.
- Never store full bank or card numbers, passwords, or tokens. Last four digits only.
- Never fill a policy with a "typical" value. Policies come from the user.
- Never delete or move files the user put in this folder.
