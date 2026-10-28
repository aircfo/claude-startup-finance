# Contributing

Thanks for looking. This is a small, opinionated repo maintained by
[airCFO](https://aircfo.com) — an unofficial set of Claude plugins for startup finance
teams. Bug reports and skill requests are the most useful things you can send; code
contributions are welcome too.

## Ways to help, in order of usefulness

1. **Tell us a skill got something wrong.** A skill that produced a wrong number, missed a
   review gate, or didn't fire when it should have is the highest-value report we can get.
   [Open a bug report](https://github.com/aircfo/claude-startup-finance/issues/new/choose).
2. **Request a workflow.** If there's a finance job you keep doing by hand, describe it —
   including the systems involved and what the finished output looks like.
   [Open a skill request](https://github.com/aircfo/claude-startup-finance/issues/new/choose).
3. **Fix docs.** Anything unclear, stale, or wrong in the README or the
   [docs site](https://aircfo.github.io/claude-startup-finance/). Small pull requests
   welcome, no issue needed.
4. **Contribute a skill.** Please open an issue first so we can agree on the shape before you
   invest the work.

## Repository layout

```
claude-startup-finance/
├── .claude-plugin/marketplace.json   # the storefront — every plugin must be listed here
├── plugins/<name>/                   # one directory per plugin
│   ├── .claude-plugin/plugin.json
│   ├── .mcp.json                     # only if the plugin bundles connectors
│   ├── skills/<skill-name>/SKILL.md
│   └── README.md
├── templates/skill-plugin/           # copy-ready scaffold for a new skill plugin
├── docs/                             # the published docs site (GitHub Pages, Jekyll)
│   ├── _tools/                       # one page per tool in the library
│   └── _data/                        # library themes + which plugin provides each connector
├── CHANGELOG.md
└── SECURITY.md
```

MCP servers and webapps live in their **own repositories** (for example
[`aircfo/qbo-mcp`](https://github.com/aircfo/qbo-mcp)) and are indexed in the root README's
"What's in this repo" table. The marketplace pulls this entire repo on install, so nothing
that doesn't need to ship to users belongs in it.

Every reader-facing tool also gets a page in the docs site's tool library, one file in
`docs/_tools/` — see "Adding a tool to the library" in
[docs/authoring-conventions.md](docs/authoring-conventions.md).

## Non-negotiables

These are the rules a pull request has to satisfy. They exist because this software runs
against people's real books and bank accounts.

- **Read-only wherever it touches money.** No write, send, transfer, or delete tools against
  an accounting, banking, payments, or spend system. A skill may *draft* something for a
  human to send; it may never send it.
- **No secrets, ever.** No API keys, OAuth tokens, client secrets, or account numbers in
  code, config, fixtures, tests, issues, or commit messages. See [SECURITY.md](./SECURITY.md).
- **No real financial or customer data.** Fixtures and examples must be synthetic. Not
  anonymized production data — synthetic.
- **Per-user auth.** Connectors authenticate as the user through their own OAuth login. Never
  a shared airCFO credential.
- **Don't break the install path.** `.claude-plugin/marketplace.json` must be valid and
  loadable at every commit, and published plugins are never renamed, moved, or split — that
  breaks everyone who already installed them.
- **Keep the disclaimers.** Every README keeps its Unofficial / not-affiliated notice and its
  read-only language.
- **Fill or placeholder, never guess.** Skills mark unknowns explicitly instead of inventing
  a plausible value. A confidently wrong number is worse than an acknowledged gap.

## Adding a skill or plugin

Read [docs/authoring-conventions.md](./docs/authoring-conventions.md) first — it covers when
a skill gets its own plugin, required files, naming, marketplace registration (including the
`skills` array), and the release process.

The short version:

```bash
cp -R templates/skill-plugin plugins/my-plugin-name    # then follow its HOW-TO-USE.md
```

Write the `SKILL.md` frontmatter `description` carefully. It's the trigger surface — the
agent decides whether to run your skill from that text alone, so it needs both the outcome
and the phrases a real user would say. Read an existing skill for the house style; matching
the surrounding voice matters more here than in most repos, because these skills are read
aloud, in effect, by a model.

## Testing your change

There's no test suite — these are prompt-shaped artifacts, so verification is a real run.

**Validate the manifests** with Claude Code's own validator:

```bash
claude plugin validate .                               # the marketplace
claude plugin validate plugins/<name>                  # each plugin you touched
npx skills add . --list                                # your skill appears by name
```

**Install it for real,** in a throwaway config directory so your own setup is untouched:

```bash
export CLAUDE_CONFIG_DIR=$(mktemp -d)
claude plugin marketplace add ./                       # trailing slash required
claude plugin install <plugin>@claude-startup-finance
claude plugin details <plugin>                         # component inventory + token cost
unset CLAUDE_CONFIG_DIR
```

`claude plugin details` is the high-value check: it prints the skills the loader actually
resolved, so a skill count that's off by one tells you something failed to load. It also
shows the always-on token cost, which every session pays for your skill's description.

**Then run the skill itself:**

1. Run it end to end against a **sandbox or your own** systems — never someone else's data.
2. Confirm it asks before anything irreversible, cites its numbers, and degrades gracefully
   when a connector isn't authorized.

Note in the pull request what you ran it against and what the output looked like. A spot
check in Claude Cowork is still worth doing before a release, since that's the supported
install path for most users.

## Pull requests

- Branch names: `feat/description`, `fix/description`, `docs/description`,
  `chore/description`.
- [Conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`,
  `chore:`, `refactor:`, with a scope where it helps (`feat(finance-contextos): …`). Include
  a body for anything non-trivial.
- Bump `plugin.json` and the matching `marketplace.json` entry in lockstep, and add a
  `CHANGELOG.md` entry, when behavior changes.
- Fill out the pull-request checklist honestly. "Not applicable" is a fine answer; a
  silently unchecked box is not.

## Questions

[alex@aircfo.com](mailto:alex@aircfo.com), or open an issue. If it's a security concern,
email — don't file publicly. See [SECURITY.md](./SECURITY.md).
