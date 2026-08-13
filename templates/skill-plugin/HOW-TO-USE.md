# How to use this scaffold

A copy-ready skeleton for a **new skill shipped as its own plugin** — the default shape for
an AI CFO newsletter drop. Read
[docs/authoring-conventions.md](../../docs/authoring-conventions.md) first; it explains when
a skill deserves its own plugin versus joining an existing one.

## Steps

1. **Copy the directory** into `plugins/`, named for your plugin:

   ```bash
   cp -R templates/skill-plugin plugins/my-plugin-name
   ```

2. **Rename the skill directory** from `skills/skill-name/` to your skill's real name
   (lowercase, hyphen-separated). This name is also the slash command, so
   `skills/close-checklist/` becomes `/close-checklist`.

3. **Fill in `.claude-plugin/plugin.json`** — replace every `REPLACE:` placeholder. `name`
   must match the plugin directory name exactly.

4. **Fill in `skills/<name>/SKILL.md`** — the frontmatter `description` is the trigger
   surface that decides whether the skill ever fires. Write what it does *and* the phrases a
   user would actually say. Read an existing skill (for example
   `plugins/all-systems-go/skills/runway-and-burn/SKILL.md`) for the house style before
   writing your own.

5. **Fill in `README.md`** — keep the Unofficial disclaimer.

6. **Register the plugin** in `.claude-plugin/marketplace.json`, including the `skills`
   array. A skill that isn't listed there is invisible to the `skills` CLI.

7. **Delete this file** (`HOW-TO-USE.md`) from your copy.

8. **Verify** before opening a pull request:

   ```bash
   jq . .claude-plugin/marketplace.json
   jq . plugins/my-plugin-name/.claude-plugin/plugin.json
   npx skills add . --list          # your new skill should appear by name
   ```

   Then load the marketplace in Claude Cowork and install the plugin. The manual install
   check is not optional — a malformed manifest breaks installation for every existing user.

## If the plugin bundles a connector

Add a `.mcp.json` alongside `.claude-plugin/`, following
`plugins/finance-contextos/.mcp.json`. Connectors must be **read-only** wherever they touch
money or accounting records, and must authenticate as the user (their own OAuth login) —
never a shared airCFO credential.
