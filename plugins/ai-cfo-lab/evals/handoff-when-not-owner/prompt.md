---
description: An operator who isn't a claude.ai Owner hits the export sign-in step; the skill drafts a forwardable request and keeps going with what doesn't depend on it.
tags: [setup, roles]
runs: 3
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---
I'm Jordan from ops, setting up the AI spend dashboard. The doctor says:

Next: Daily export can sign in — The export's browser profile isn't signed in yet.
  Fix (claude.ai Owner): cd "/Users/jordan/AI-Spend" && uv run --with playwright python .../fetch_surface_b_browser.py "/Users/jordan/AI-Spend" --login

I'm not an Owner on claude.ai — our CEO is. What do I do?
