# Rung 3 to 4: GitHub and Claude Code setup

**What this gets the team:** every change to a skill or a policy page is reviewed before it
counts, the author never approves their own change, and there's a full history of who changed
what and why. It's the same control the workpapers already have, applied to the method.

**Who does it first:** one champion (usually the controller or a senior accountant), then each
teammate with "Add a teammate" at the end. Budget 60 to 90 minutes for the champion.

**Coach it one step at a time.** Give one step, have them run it, ask them to paste back what
it printed, and check it before the next step. Every command below is typed into the
computer's terminal, not into Claude:

- **Mac:** press Cmd + Space, type "Terminal", press Enter.
- **Windows:** open the Start menu, type "PowerShell", open "Windows PowerShell" (not as
  administrator unless a step says so).

**Before you start, confirm:**
- a Claude plan that includes Claude Code (Pro, Max, Team, or Enterprise);
- a GitHub account for each person (free is fine to start);
- permission to install software on the computer;
- the company's answer to "may we store financial data in GitHub?" Until someone with the
  authority says yes, the repository holds the handbook and skills only, and workpapers and
  exports stay out (step 7 sets that up).

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

It asks for the Mac's login password (nothing shows while typing; that's normal). At the end
it may print "Next steps" with two or three lines to run. Run those lines exactly as printed.
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

Python: on a Mac, `python3 --version`. On Windows, `python --version` (if that opens the
Microsoft Store instead, use `py --version`).

If a check says "command not found" or "not recognized," open a new terminal window and try
again. On a Mac, rerun the "Next steps" lines from step 1. If it still fails, install that one
tool from its website (git-scm.com, cli.github.com, nodejs.org, python.org,
code.visualstudio.com) and check again.

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

Choose **GitHub.com**, then **HTTPS**, then **Login with a web browser**. It shows a one-time
code; copy it, press Enter, paste the code in the browser, and approve. Check:

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

It shows no progress while it downloads; wait for it to finish. Open a new terminal window,
then check:

```bash
claude --version
claude doctor
```

`claude doctor` checks the install and suggests fixes. If the install fails, the Claude Code
setup guide (code.claude.com/docs/en/setup) matches each error to a fix.

**Sign in:** type `claude` and press Enter. It opens the browser to sign in with your Claude
account. Type `/exit` to leave when you're done.

**Optional:** in VS Code, open Extensions (the four-squares icon), search "Claude Code," and
install the one from Anthropic, to use Claude Code in a panel beside your files.

## Step 6: Create a GitHub organization for the team

An organization is a shared GitHub account for the company, so the repository doesn't belong
to one person who might leave. On github.com: your profile picture, **Your organizations**,
**New organization**, the free plan. Invite teammates later.

Skip this if the company already has a GitHub organization; ask its owner to create the
repository for you or give you permission.

## Step 7: Put the Finance Brain in a private repository

**First, keep financial data out.** Ask Claude to create a file called `.gitignore` in the
Finance Brain folder with these lines. It tells Git which files never to upload:

```text
# Financial data stays out unless the company has approved storing it in GitHub.
handbook/sources/
testing/*
!testing/README.md
site/
*.xlsx
*.csv
!examples/workpapers/*.xlsx
.claude/skills
.DS_Store
~$*
```

**Then go to the folder in the terminal.** Type `cd`, a space, drag the Finance Brain folder
from Finder or File Explorer into the terminal window, and press Enter. Check you're in the
right place:

```bash
ls
```

(On Windows, `dir`.) You should see `CLAUDE.md`, `handbook`, and `skills`.

**Save the first version and upload it** (replace `your-org` with the organization's name):

```bash
git init
git add .
git commit -m "Start our Finance Brain"
gh repo create your-org/finance-brain --private --source=. --remote=origin --push
```

In order, these: start tracking the folder, stage every file (except what `.gitignore`
excludes), save the first version with a note, and create the private repo on GitHub and
upload to it. Check it worked and is private:

```bash
gh repo view --web
```

The browser opens the repo. Confirm it says **Private** next to the name, and that no
workpapers or exports are in it.

## Step 8: Turn on review

This is what makes "the author is never the approver" automatic. GitHub never lets someone
approve their own pull request; this step makes approval required.

On the repo's GitHub page: **Settings**, **Rules**, **Rulesets**, **New ruleset**, **New
branch ruleset**.

- Name it "Review required" and set **Enforcement status** to **Active**.
- Under **Target branches**, add the **default branch**.
- Turn on **Require a pull request before merging**, with **1** required approval.
- Turn on **Block force pushes**.
- Save.

**If GitHub says this needs an upgrade:** enforcing rules on private repositories needs a paid
GitHub plan (GitHub Team for organizations). Until then, agree as a team that nobody merges
their own pull request, and check at the monthly skills review.

**Optional, recommended: code owners.** Ask Claude to create `.github/CODEOWNERS` so the
controller must approve changes to policies and skills (use their GitHub username), then turn
on **Require review from Code Owners** in the ruleset:

```text
# The controller approves every change to policies and skills.
/handbook/ @controller-username
/skills/ @controller-username
/CLAUDE.md @controller-username
```

Make this change through a pull request (step 10 shows how). It's good practice.

## Step 9: Connect your systems in Claude Code

Connectors stay read-only, and each person signs in with their own login.

- **Connectors you've added on claude.ai** (for example QuickBooks) are available in Claude
  Code when you're signed in with the same Claude account. Inside Claude Code, type `/mcp` to
  see them.
- **Billing, spend, and banking connectors** for several common systems come in airCFO's free
  `all-systems-go` plugin, which also adds runway, revenue reconciliation, and board metrics
  workflows:

  ```bash
  claude plugin marketplace add aircfo/claude-startup-finance
  claude plugin install all-systems-go@claude-startup-finance
  ```

  Then start `claude`, type `/mcp`, and sign in to the ones you use.

Check: in the Finance Brain folder, start `claude` and ask "Which finance systems can you read
right now?"

## Step 10: Your first pull request

Practice on something harmless. In the Finance Brain folder, start `claude` and say:

> "Make a new branch, set the Last reviewed line in handbook/cash.md to today with my name,
> commit it, and open a pull request."

Claude runs the Git and GitHub commands, explaining each one, and gives you a link. Send it to
a teammate. They open it, click **Files changed**, check the change, and click **Review
changes**, **Approve**. Then merge it on GitHub.

That's the loop for every change from now on: a branch, a pull request, someone else approves,
merge.

## Add a teammate

1. **The champion invites them:** the organization's **People** page, **Invite member**, then
   give them access to the `finance-brain` repo.
2. **The teammate does steps 1 to 5 and step 9** on their own computer.
3. **They get the team's copy** (somewhere permanent, such as Documents):

   ```bash
   cd ~/Documents
   gh repo clone your-org/finance-brain
   cd finance-brain
   code .
   ```

   On Windows, use `cd $HOME\Documents` for the first line. The last line opens the folder in
   VS Code.
4. **They start Claude Code in that folder** (`claude`). It reads `CLAUDE.md`, and saying
   "use the setup-finance-brain skill" (or any skill's name) works right away.
5. **Optional, Mac:** for slash commands such as `/usage-accrual`, link the skills folder once:

   ```bash
   mkdir -p .claude && ln -s ../skills .claude/skills
   ```

   On Windows this needs Developer Mode, so skip it; naming the skill works the same.

Teammates who prefer Cowork can open this same folder in Cowork for daily work. Their changes
still go through a pull request, so they'll use Claude Code (or GitHub Desktop) for that step.

## The daily rhythm

| When | Say to Claude Code | What happens |
| --- | --- | --- |
| Start of the day | "Get the latest." | Downloads changes teammates merged (`git pull`). |
| You fixed a skill or a policy page | "Open a pull request for this change." | A branch, a commit, and a pull request link to send to a reviewer. |
| Someone sends you a pull request | Open the link on GitHub | Read **Files changed**, then **Approve** or **Request changes**. |
| After a merge | "Get the latest." | Everyone works from the approved version. |

## If something goes wrong

- **"Command not found" or "not recognized":** open a new terminal window. On a Mac, rerun the
  Homebrew "Next steps" lines.
- **GitHub sign-in problems:** run `gh auth login` again.
- **"Rejected" when uploading:** someone merged first. Say "get the latest, then try again,"
  and Claude sorts it out.
- **Claude Code won't start or sign in:** run `claude doctor` and share what it prints.
- **Anything else:** paste the full message into this chat and work through it before moving
  on.

Never paste a password, a token, or a full account number into the chat. Every sign-in here
happens in the browser.

## When this rung is done

The repository is private, review is on (or agreed), the first pull request was approved by
someone other than its author, and each teammate can get the latest and open a pull request.
Record the team as on rung 4 in "Level-up progress" in `CLAUDE.md`.
