---
description: Ramp's AI spend connection points at a different Console organization than the one in use; the skill names the mismatch and the Ramp admin's fix.
tags: [setup, ramp]
runs: 3
max_turns: 6
allowed_tools: [Read, Glob, Grep, Skill]
---
We set up AI spend tracking last week. This month's report shows API spend of $0.12, even though engineering calls the Anthropic API every day. Our engineers' Console organization is aaaaaaaa-1111-2222-3333-444444444444, and Ramp's ramp_get_ai_token_spend_connections returned an ANTHROPIC configuration, connected and VALIDATED, with platform_claude_dev.organization_id "bbbbbbbb-5555-6666-7777-888888888888". Is everything fine?
