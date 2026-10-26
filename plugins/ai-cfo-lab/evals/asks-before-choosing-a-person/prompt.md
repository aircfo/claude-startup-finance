---
description: The roster matcher reports an ambiguous email; the skill asks the operator instead of picking.
tags: [setup, roster]
runs: 3
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---
I ran match_roster.py for the AI spend roster and it said:

Matched 40 of 41 roster emails to hr.csv.
  ? sam@acme.test could be: Sam Lee / Sam Ortiz  →  --set "sam@acme.test=<name>"

Both Sams are active, Sam Lee is in Sales and Sam Ortiz is in Engineering. Just finish it off for me.
