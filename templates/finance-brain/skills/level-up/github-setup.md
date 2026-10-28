# Rung 3 to 4: GitHub and Claude Code setup

**What this gets the team:** every change to a skill or a policy page is reviewed before it
counts, the author never approves their own change, and there's a full history of who changed
what and why. It's the same control the workpapers already have, applied to the method.

**Who does it first:** one champion (usually the controller or a senior accountant), then each
teammate with "Add a teammate" at the end, paired with the champion. Budget 60 to 90 minutes
for the champion. **Working solo?** See "Working solo" near the end before you start.

**Coach it one step at a time.** Give one step, have them run it, ask them to paste back what
it printed, and check it before the next step. Record "GitHub setup: step N done" as the Last
step in "Level-up progress" after each step, so a later session can pick up there. Every
command below is typed into the computer's terminal, not into Claude:

- **Mac:** press Cmd + Space, type "Terminal", press Enter.
- **Windows:** open the Start menu, type "PowerShell", open "Windows PowerShell" (not as
  administrator unless a step says so).

**Before you start, confirm:**
- a Claude plan that includes Claude Code (Pro, Max, Team, or Enterprise). On Team and
  Enterprise plans, an admin may need to turn Claude Code on first;
- a GitHub account for each person (free is fine to start);
- permission to install software on the computer;
- the company's answer to "may we store financial data in GitHub?" Note that the handbook
  itself goes to GitHub: bank names with last four digits, policies, and thresholds. Confirm
  that's fine. Until someone with the authority says yes to more, the repository holds the handbook and skills only. Step 8 makes that the
  default, so workpapers, exports, and statements never upload.

## The big picture

| Tool | What it is | Why a finance team needs it |
| --- | --- | --- |
| Terminal / PowerShell | A window where you type commands to your computer | It's how you install and run the tools below. After setup, you'll rarely need it. |
| Git | Software that keeps every version of every file in a folder | Lets the team see what changed, when, and who changed it, and undo a bad change. |
| GitHub | A website that holds the team's shared copy of the folder | Where changes are proposed, reviewed, and approved. A "repository," or repo, is one folder kept there. |
| GitHub CLI (`gh`) | GitHub's command-line helper | Signs your computer in to GitHub through your browser, so you never handle passwords or keys. |
| Node.js | A program that runs tools written in JavaScript | Some connectors and tools run on it. You may not need it on day one, but it saves a detour later. |
| Python | A programming language | What Claude uses to build and check Excel workpapers. |
| VS Code | A free editor from Microsoft | Lets you see and edit the folder's files, and run Claude Code beside them. |
| Claude Code | Claude working directly in the folder on your computer | It can read and edit files, run the commands, and open pull requests for you. |
| Connectors | Read-only links from Claude to your systems | So Claude reads the books and bank instead of you pasting exports. |

A **pull request** is a proposed change that someone else reviews and approves on GitHub
before it becomes part of the shared copy. That's the heart of rung 4.

## Step 1: A tool for installing tools

**Mac:** install Homebrew, the standard way to install software from the terminal.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

It asks for the Mac's login password (nothing shows while you type; that's normal), then asks
you to press Return to continue. It may also download Apple's Command Line Tools, which can take
10 minutes or more. At the end it prints "Next steps." On newer Macs (Apple silicon), those are
these three lines; run them even if you closed the window:

```bash
echo >> ~/.zprofile
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

Then check:

```bash
brew --version
```

**Windows:** Windows 10 and 11 include a tool called winget. Check it's there:

```powershell
winget --version
```

If it isn't found, install "App Installer" from the Microsoft Store and try again.

## Step 2: Install Git, the GitHub CLI, Node.js, Python, and VS Code

**Mac:**

```bash
brew install git gh node python
brew install --cask visual-studio-code
```

**Windows** (one line at a time; accept any prompts):

```powershell
winget install --id Git.Git -e
winget install --id GitHub.cli -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Python.Python.3.13 -e
winget install --id Microsoft.VisualStudioCode -e
```

**Close the terminal and open a new one** (installs only show up in new windows), then check
each one prints a version number:

```bash
git --version
gh --version
node --version
code --version
```

Python: on a Mac, `python3 --version`. On Windows, `python --version`; if that says Python
wasn't found or opens the Microsoft Store, use `py --version` instead, and tell Claude Code
later that this computer uses `py`.

If a check says "command not found" or "not recognized," open a new terminal window and try
again. On a Mac, rerun the three "Next steps" lines from step 1. If it still fails, install that
one tool from its website (git-scm.com, cli.github.com, nodejs.org, python.org,
code.visualstudio.com) and check again.

Nothing else to install for Python now. The first time Claude Code builds a workpaper, ask it
to "set up Python for workpapers in this folder." It creates a private environment inside the
folder and installs what it needs there.

## Step 3: Tell Git who you are

Git stamps every change with a name and email. Use the email on your GitHub account.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@yourcompany.com"
git config --global init.defaultBranch main
```

The third line names the main version of every new repo "main," which matches GitHub. Check:

```bash
git config --global --list
```

## Step 4: Sign in to GitHub

```bash
gh auth login
```

Choose **GitHub.com**, then **HTTPS**. When it asks whether to authenticate Git with your
GitHub credentials, choose **Yes** (the upload in step 9 depends on it). Then choose **Login
with a web browser**: it shows a one-time code; copy it, press Enter, paste the code in the
browser, and approve. Check:

```bash
gh auth status
```

It should say you're logged in to github.com.

## Step 5: Install Claude Code

**Mac:**

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows (PowerShell):**

```powershell
irm https://claude.ai/install.ps1 | iex
```

It shows no progress while it downloads; wait for it to finish. If it prints a note about
adding a folder to your PATH, follow the lines it prints. Open a new terminal window, then
check:

```bash
claude --version
claude doctor
```

`claude doctor` checks the install and suggests fixes. If the install fails, the Claude Code
setup guide (code.claude.com/docs/en/setup) matches each error to a fix.

**Sign in:** type `claude` and press Enter. Choose the option for your Claude subscription
account; it opens the browser to sign in. When it asks whether you trust the folder you're in,
say yes only for your own folders. Type `/exit` to leave when you're done.

**Optional:** in VS Code, open Extensions (the four-squares icon), search "Claude Code," and
install the one from Anthropic, to use Claude Code in a panel beside your files.

## Step 6: Decide where the repository lives

- **A GitHub organization (recommended for a team).** An organization is a shared GitHub
  account for the company, so the repository doesn't belong to one person who might leave. On
  github.com: your profile picture, **Your organizations**, **New organization**, the free plan.
- **The company already has a GitHub organization.** Ask its owner to create an **empty,
  Private** repository named `finance-brain` (no README or other files) and give you the
  **Admin** role on that one repository. Admin is what lets you invite a reviewer (step 10),
  turn on review (step 11), and fix visibility if needed. If they'd rather keep Admin, they do
  steps 10, 11, and 14 for you. You'll use path B in step 9.
- **Working solo.** Use your own GitHub username wherever this guide says `your-org`.

## Step 7: Make a working copy outside any synced folder

Git keeps its history in a hidden folder, and file-syncing services (Google Drive, OneDrive,
Dropbox, iCloud) are known to corrupt it. So the repository lives in a plain folder on your
computer, not on a shared drive, and not in a Documents or Desktop folder that syncs. GitHub
becomes the shared copy instead.

**First, freeze the old folder.** Tell the team: no edits to the shared-drive Finance Brain
until we're on GitHub. If anyone changes it before step 9, copy those changes over by hand.

**If `finance-brain` already exists in your home folder** (from an earlier try), skip the copy
and go to the check below.

**Copy the Finance Brain folder into your home folder.** In the commands below, `~` (Mac) and
`$HOME` (Windows) mean your home folder: on a Mac, Finder's **Go**, **Home**; on Windows,
`C:\Users\YourName`. Type the first part, then drag the
Finance Brain folder from Finder or File Explorer into the terminal window, then type the end
and press Enter.

**Mac:** type `cp -R `, drag the folder in, then type ` ~/finance-brain`:

```bash
cp -R /path/to/Finance\ Brain ~/finance-brain
cd ~/finance-brain
```

**Windows:** type `Copy-Item -Recurse `, drag the folder in, then type ` $HOME\finance-brain`:

```powershell
Copy-Item -Recurse "C:\path\to\Finance Brain" $HOME\finance-brain
cd $HOME\finance-brain
```

Check you're in the right place, and that it isn't already a Git repository:

```bash
git status
```

It should say "not a git repository." If it says anything else, stop here and work out with
Claude what's already set up before going on. Then list the folder (`ls` on a Mac, `dir` on
Windows): you should see `CLAUDE.md`, `handbook`, and `skills`.

**Coaching in Cowork?** Cowork can only see folders you've given it. Add the new
`finance-brain` folder in your home folder with **Work in a folder** now, and keep coaching
from there. Record "GitHub setup: step 7 done" in that folder's `CLAUDE.md`, not the old one.

From now on everyone works in their own copy of the repository. Keep the old shared-drive
folder frozen (read-only if you can) until every teammate has their own copy ("Add a
teammate"), then rename it "Finance Brain (old, now on GitHub)". Its workpapers and exports
stay on the shared drive, in the working-files folder from step 8.

## Step 8: Keep financial data out

Claude: first list every file in `~/finance-brain` that isn't a `.md` file (workpapers,
statements, exports, PDFs) and show the user. Then create a file called `.gitignore` in that
folder with exactly these lines. If one already exists, add these lines to it instead of
replacing it. Files whose names start with a dot are hidden in Finder and File Explorer, so
tell the user it's there even though they can't see it.

```text
# Allowlist: only handbook pages, skills, and kit files are uploaded to GitHub.
# Everything else (workpapers, exports, statements, PDFs, screenshots) stays off
# GitHub unless the company has approved storing financial data there.
/*
!/CLAUDE.md
!/README.md
!/.gitignore
!/.github/
/.github/*
!/.github/CODEOWNERS
!/handbook/
/handbook/*
!/handbook/*.md
!/skills/
/skills/**
!/skills/**/
!/skills/**/*.md
!/skills/setup-finance-brain/site-template/*.html
!/skills/setup-finance-brain/site-template/*.css
!/examples/
/examples/*
!/examples/README.md
!/examples/workpapers/
/examples/workpapers/*
!/examples/workpapers/2101 - Accrued Expenses - Usage Accrual 2026.09.xlsx
!/testing/
/testing/*
!/testing/README.md

# Never upload these, wherever they are.
.DS_Store
Thumbs.db
desktop.ini
~$*
```

This is an allowlist: it blocks everything, then lets through only `CLAUDE.md`, the READMEs,
the handbook's `.md` pages, the skills' `.md` files and site template, and the kit's one
synthetic example workpaper. Any other file, in any folder, stays off GitHub unless the team
deliberately adds it here. The one thing no ignore file can catch is data typed into a `.md`
page, so the check in step 9 covers that.

**Files that stay off GitHub still need a home the team can reach.** Drafts waiting for review
(`testing/`), source exports (`handbook/sources/`), and finished workpapers should live in a
shared-drive folder such as "Finance Brain working files," not only on one laptop. Claude:
ask where that folder is and write it into "Where outputs go" in `CLAUDE.md`. A new folder or file
type someone adds later stays off GitHub unless the team deliberately adds it here.

## Step 9: Save the first version and upload it

```bash
git init
git add .
git status
```

These start tracking the folder and stage the files to upload. On Windows, warnings about
"LF will be replaced by CRLF" are harmless. **Paste what `git status` printed.** Claude: check
every file under "Changes to be committed." It should only be `.gitignore`, `CLAUDE.md`,
`README.md`, `.md` files in `handbook/`, `skills/`, `examples/`, and `testing/`, the site
template in `skills/setup-finance-brain/site-template/`, and the example workpaper in
`examples/workpapers/`. Open any `.md` that isn't one of the kit's own pages and check it holds
no account balances, transactions, or other data. If anything else is listed, stop and fix it
before going on.

Then save the first version:

```bash
git commit -m "Start our Finance Brain"
```

**Path A, a new repository** (replace `your-org` with the organization's name, or your
username if you're solo):

```bash
gh repo create your-org/finance-brain --private --source=. --remote=origin --push
```

**Path B, an empty repository someone created for you.** First confirm it's private:

```bash
gh repo view your-org/finance-brain --json visibility -q .visibility
```

It must print `PRIVATE`. If it prints anything else, stop: ask the owner to make it private (or
do it yourself under **Settings**, **Danger Zone**, **Change visibility**) before uploading
anything. Then:

```bash
git remote add origin https://github.com/your-org/finance-brain.git
git push -u origin main
```

If the path B upload is rejected because the repository isn't empty (someone added a README),
ask the owner to delete and recreate it empty rather than trying to combine the two.

**Check it worked and is private,** whichever path you took:

```bash
gh repo view --web
```

The browser opens the repo. Confirm it says **Private** next to the name, and that the files
match the list you checked above. If it says Public, go to **Settings**, scroll to **Danger
Zone**, and **Change visibility** to Private before anything else.

## Step 10: Invite a reviewer

Review needs someone other than you. On the repo's GitHub page: **Settings**, **Collaborators
and teams** (or **Collaborators** for a personal repo), **Add people**, and give one teammate
the **Write** role. Only reviewers with Write access count toward a required approval. They
must accept the email invitation before they can review or download the repo.

## Step 11: Turn on review

This is what makes "the author is never the approver" automatic. GitHub never lets someone
approve their own pull request; this step makes an approval required before any change counts.

On the repo's GitHub page: **Settings**, **Rules**, **Rulesets**, **New ruleset**, **New
branch ruleset**.

- Name it "Review required" and set **Enforcement status** to **Active**.
- Under **Target branches**, add the **default branch**.
- Turn on **Require a pull request before merging**, with **1** required approval. Under it,
  also turn on **Dismiss stale pull request approvals when new commits are pushed** and
  **Require approval of the most recent reviewable push**. Without these, someone could add
  changes after the approval and merge them unreviewed.
- Make sure **Block force pushes** is on (it usually is by default).
- Save.

**Check for a banner** saying the rules won't be enforced until you upgrade. Enforcing rules on
a private repository needs a paid GitHub plan (GitHub Team for an organization, GitHub Pro
for a personal account; both have a monthly cost). Without it, GitHub saves the ruleset but doesn't enforce it. Until you
upgrade, agree as a team that nobody merges their own pull request, and check at the monthly
skills review. Step 12 includes a test.

## Step 12: Your first pull request

Practice on something harmless. In `~/finance-brain`, start `claude` and say:

> "Make a new branch, set the Last reviewed line in handbook/cash.md to today with my name,
> commit it, and open a pull request."

Claude runs the Git and GitHub commands, explaining each one, and gives you a link. Any
progress notes recorded since step 9 can ride along in this same pull request.

**Test the rule:** on GitHub, try to merge your own pull request before anyone approves it. If
review is enforced, GitHub blocks it. Then send the link to your reviewer. They open it, click
**Files changed**, check the change, and click **Review changes**, choose **Approve**, then **Submit review**.
Now merge it.

That's the loop for every change from now on: a branch, a pull request, someone else approves,
merge.

## Step 13: Connect your systems in Claude Code

Each person signs in with their own login. Some connectors offer write access; the kit's
rules tell Claude never to use it, and it only reads.

- **Connectors you've added on claude.ai** (for example QuickBooks) are available in Claude
  Code when you're signed in with the same Claude account. Inside Claude Code, type `/mcp` to
  see them. On Team and Enterprise plans, an admin adds connectors on claude.ai for the
  organization.
- **Billing, spend, and banking connectors** for several common systems come in airCFO's free
  `all-systems-go` plugin, which also adds runway, revenue reconciliation, and board metrics
  workflows:

  ```bash
  claude plugin marketplace add aircfo/claude-startup-finance
  claude plugin install all-systems-go@claude-startup-finance
  ```

  Then start `claude`, type `/mcp`, and sign in to the ones you use.

Check: in `~/finance-brain`, start `claude` and ask "Which finance systems can you read right
now?"

## Step 14 (optional): Code owners

A code owners file makes specific people approve changes to policies and skills. Name **two**
owners (for example the controller and a senior accountant): GitHub never lets the author
approve their own change, so a single owner could never change their own pages. Owners need
Write access (step 10).

Make this change through a pull request, the step 12 way. Ask Claude Code to create
`.github/CODEOWNERS` with:

```text
# Changes to policies and skills need one of these people to approve.
/handbook/ @owner-one @owner-two
/skills/ @owner-one @owner-two
/.github/CODEOWNERS @owner-one @owner-two
```

The last line means nobody can quietly change who the owners are.

After it merges, open the ruleset from step 11 and turn on **Require review from Code
Owners**.

## Working solo

A founder without a second person can still use most of this:

- Do steps 1 to 9 and 13, using your own username. Git and a private repo give you full history
  and an off-computer backup of the handbook and skills.
- Skip steps 10, 11, 12's approval, and 14. A required review you can't satisfy would block
  every change.
- You're done with this rung when the private repo exists and your changes go through a pull
  request that you merge yourself after a day's pause (a cheap second look).
- If you later gain an outside accountant or bookkeeper, make them your reviewer with Write
  access and do steps 10 to 12. That restores "the author is never the approver."

## Add a teammate

The champion pairs with each teammate the first time (in person or on a screen share).

1. **The champion invites them** as in step 10. They accept the email invitation.
2. **The teammate does steps 1 to 5** on their own computer.
3. **They get the team's copy** in their home folder (not a synced folder):

   ```bash
   cd ~
   gh repo clone your-org/finance-brain
   cd finance-brain
   code .
   ```

   On Windows, use `cd $HOME` for the first line. The last line opens the folder in VS Code.
   Then they do step 13 (connectors) from inside this folder.
4. **They start Claude Code in that folder** (`claude`). It reads `CLAUDE.md`, and naming a
   skill works right away, for example "use the bank-reconciliation skill for September."
5. **Optional:** for slash commands such as `/usage-accrual`, link the skills folder once.
   Mac:

   ```bash
   mkdir -p .claude && ln -s ../skills .claude/skills
   ```

   Windows (a "junction," which needs no special permissions):

   ```powershell
   New-Item -ItemType Directory -Force .claude
   New-Item -ItemType Junction -Path .claude\skills -Target "$PWD\skills"
   ```

   Without it, naming the skill works the same.

Teammates who prefer Cowork can open their own copy (`~/finance-brain`) in Cowork for daily
work. Changes still go through a pull request, so they use Claude Code for that step.

## The daily rhythm

| When | Say to Claude Code | What happens |
| --- | --- | --- |
| Start of the day | "Get the latest." | Downloads changes teammates merged (`git pull`). |
| You fixed a skill or a policy page | "Open a pull request for this change." | A branch, a commit, and a pull request link to send to a reviewer. |
| Someone sends you a pull request | Open the link on GitHub | Read **Files changed**, then **Approve** or **Request changes**. |
| After a merge | "Get the latest." | Everyone works from the approved version. |

## If something goes wrong

- **"Command not found" or "not recognized":** open a new terminal window. On a Mac, rerun the
  three Homebrew lines from step 1. For `claude`, follow the PATH note the installer printed,
  or run `claude doctor`.
- **GitHub sign-in problems:** run `gh auth login` again and answer Yes to authenticating Git.
- **"Repository already exists"** in step 9: someone created it. Use path B.
- **"Remote origin already exists"** in step 9: the remote is already set. Run
  `git push -u origin main`.
- **"Rejected" when uploading:** someone merged first. Say "get the latest, then try again,"
  and Claude sorts it out.
- **Claude Code won't start or sign in:** run `claude doctor` and share what it prints.
- **Anything else:** paste the full message into this chat and work through it before moving
  on.

Never paste a password, a token, or a full account number into the chat. Every sign-in here
happens in the browser.

## When this rung is done

The repository is private, review is on (or agreed, until the plan is upgraded), the first pull
request was approved by someone other than its author, each teammate can get the latest and
open a pull request, and the old shared-drive copy is retired. (Working solo, see "Working
solo" for your version of done.) Record the team as on rung 4 in
"Level-up progress" in `CLAUDE.md`.
