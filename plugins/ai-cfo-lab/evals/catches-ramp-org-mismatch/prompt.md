---
description: Ramp's AI-spend connection points at a different Console org than the Admin key; the skill names the mismatch and the Ramp admin's fix.
tags: [setup, ramp]
runs: 3
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---
Setting up AI spend with api_cost_source "ramp". The doctor printed:

 ✓ Admin key's organization — Acme (aaaaaaaa-1111-2222-3333-444444444444)

and Ramp's ramp_get_ai_token_spend_connections returned an ANTHROPIC configuration, connected and VALIDATED, with platform_claude_dev.organization_id "bbbbbbbb-5555-6666-7777-888888888888". Our API cost on the dashboard shows $0.12 this month even though engineering uses the API every day. Is everything fine?
