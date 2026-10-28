# Commands

A command is a markdown file that tells Claude how to do one recurring task the way your team
does it. Anyone on the team can run it and get the same workpaper.

## Running a command

**Claude Cowork:** in a session working in this folder, say what you want and name the file:

> "Run `commands/jes/prepaid-amortization.md` for September 2026."

**Claude Code:** copy `commands/` into `.claude/commands/` (keep the subfolders, and leave out
`_templates/`, which are references rather than tasks) and run each one as a
slash command named after the file, for example `/prepaid-amortization 2026-09` (the
subfolder only organizes them). The text after the command name arrives as `$ARGUMENTS`; every
command here also works without it by asking for what it needs.

## How the folder is organized

By workflow, not by who built it:

| Folder | What goes in it |
| --- | --- |
| `setup/` | One-time and occasional tasks: building the handbook, creating new commands |
| `_templates/` | The workpaper standard every JE and rec follows. Copy these to start a new command. |
| `jes/` | Journal entries |
| `recs/` | Reconciliations |
| `publish/` | Turning the handbook into something others can read |

Add folders as you need them, for example `tieouts/` for recurring tie-outs or `reporting/`
for the monthly package.

## Anatomy of a command

Every command has the same sections, so anyone can read one and know what it does:

1. **Frontmatter:** a one-line `description` and an `argument-hint`.
2. **Purpose:** what it produces and when it runs in the close.
3. **Read first:** the handbook pages it depends on.
4. **Inputs:** what it needs and where each input comes from (a connected system, or a named
   export with a date range).
5. **Steps:** numbered, specific enough that two people get the same result.
6. **Output:** the workpaper, following `_templates/`, with its file name and save location.
7. **Checks before handoff:** the tests the output must pass.
8. **Never:** the lines it doesn't cross.

## Adding a command

Don't write one from scratch. Run `commands/setup/new-command.md`: Claude recreates last
month's version of the task, compares it to the real one until they match, and writes the
command from what worked.

## Changing a command

Commands are how the team's method improves. When a reviewer catches a problem:

1. Fix the command (or the handbook page it reads), not just this month's output.
2. Rerun into `testing/` and compare to a known-good result.
3. Add a line to the changelog in `CLAUDE.md`: what changed, why, and who approved it.

If you keep this folder in Git, make each change a pull request and require someone other than
the author to approve it. That's the same review rule as the workpapers, applied to the method.
