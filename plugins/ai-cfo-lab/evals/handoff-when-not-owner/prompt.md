---
description: An operator who isn't a claude.ai Owner reaches the export script's one-time sign-in; the skill drafts a forwardable request and keeps going with what doesn't depend on it.
tags: [setup, roles]
runs: 3
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---
I'm Jordan from ops, setting up AI spend tracking on my Mac. For the daily claude.ai spend export, the next step is:

  uv run --with playwright python .../fetch_spend_export.py "/Users/jordan/AI-Spend" --login

and it says a claude.ai Owner has to sign in. I'm not an Owner on claude.ai; our CEO is. What do I do?
