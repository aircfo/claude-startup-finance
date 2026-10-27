# Evals

Behavior tests for the skills in this plugin, run with `claude plugin eval`.
Each case is one decision point where a wrong answer would hurt a real
operator: accepting a key pasted in chat, typing a password into claude.ai,
publishing per-person spend by default. Add a case whenever a real install
finds Claude saying or doing the wrong thing.

Run them (they call the model, so they cost money — about $1 for one pass of
every case, about $3 for three):

```bash
claude plugin eval plugins/ai-cfo-lab --runs 3 --ablation none --trust-plugin --no-publish --max-cost-usd 5
```

Results land in `evals/results/` (gitignored). The offline tests of the skill's
two scripts, which CI runs on every pull request, live in
`skills/ai-spend-analysis/scripts/__tests__/`. The engine's own tests live in
[aircfo/aicfo-spend-analysis](https://github.com/aircfo/aicfo-spend-analysis).
