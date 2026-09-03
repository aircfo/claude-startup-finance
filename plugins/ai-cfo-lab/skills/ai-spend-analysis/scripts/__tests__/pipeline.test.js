'use strict';
// End-to-end smoke test for the ai-spend-analysis scripts, driven over the
// committed synthetic fixtures. It exercises the deterministic OFFLINE core
// (validate Surface B -> build workbooks -> build artifact -> Slack draft) — it
// never touches the network, so the two fetch steps (Surface B browser/manual
// export, Surface C Admin API) are out of scope here and covered by their own
// no-network paths. openpyxl is optional: the .xlsx assertions run only when it
// is importable, matching the pipeline's graceful-degradation contract.
const { test } = require('node:test');
const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SKILL_DIR = path.resolve(__dirname, '..', '..');
const SCRIPTS = path.join(SKILL_DIR, 'scripts');
const FIXTURES = path.join(SKILL_DIR, 'fixtures');
const PY = process.env.PYTHON || 'python3';
const PERIODS = ['2026-04', '2026-05', '2026-06'];

const pythonAvailable = () => spawnSync(PY, ['--version']).status === 0;
const openpyxlAvailable = () => spawnSync(PY, ['-c', 'import openpyxl']).status === 0;
const run = (script, ...args) => spawnSync(PY, [path.join(SCRIPTS, script), ...args], { encoding: 'utf8' });
const skip = pythonAvailable() ? false : `${PY} not available`;

function freshWorkspace() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-'));
  fs.cpSync(path.join(FIXTURES, 'config'), path.join(root, 'config'), { recursive: true });
  fs.cpSync(path.join(FIXTURES, 'raw'), path.join(root, 'raw'), { recursive: true });
  return root;
}

// The artifact embeds its data as `<script>const DATA = {...};</script>`.
function embeddedData(html) {
  const marker = 'const DATA = ';
  const start = html.indexOf(marker) + marker.length;
  const end = html.indexOf(';</script>', start);
  return JSON.parse(html.slice(start, end));
}

test('pipeline builds summary, artifact, and Slack draft from fixtures', { skip }, () => {
  const root = freshWorkspace();
  try {
    for (const p of PERIODS) {
      const r = run('validate_surface_b.py', path.join(root, 'raw', p, 'overage_spend.csv'), p);
      assert.strictEqual(r.status, 0, `validate ${p} failed: ${r.stderr}`);
      const st = JSON.parse(fs.readFileSync(path.join(root, 'raw', p, 'surface_b_status.json')));
      assert.strictEqual(st.state, 'ok', `Surface B ${p} should validate ok`);
    }

    assert.strictEqual(run('build_workbooks.py', root).status, 0, 'build_workbooks should exit 0');
    const summary = JSON.parse(fs.readFileSync(path.join(root, 'workbooks', 'build_summary.json')));
    assert.strictEqual(summary.company, 'Northwind Analytics');
    assert.deepStrictEqual(summary.periods, PERIODS);
    assert.ok(summary.b_rows > 100, `expected many overage rows, got ${summary.b_rows}`);
    assert.ok(summary.c_rows > 0, 'expected Surface C rows from the fixture');
    const flagTypes = new Set(summary.flag_list.map((f) => f.flag));
    for (const want of ['reclaim_candidate', 'premium_underutilized', 'consistent_overage', 'product_spike', 'unowned_api_key']) {
      assert.ok(flagTypes.has(want), `expected the fixtures to trigger a ${want} flag`);
    }

    assert.strictEqual(run('build_artifact.py', root).status, 0, 'build_artifact should exit 0');
    const htmlPath = path.join(root, 'artifacts', '2026-06_ai_spend.html');
    assert.ok(fs.existsSync(htmlPath), 'artifact HTML should exist for the latest period');
    const html = fs.readFileSync(htmlPath, 'utf8');
    const data = embeddedData(html);
    assert.strictEqual(data.company, 'Northwind Analytics', 'artifact title/data driven by company_name config');
    assert.deepStrictEqual(data.periods, PERIODS);
    assert.strictEqual(data.families.length, 4, 'four model families from models.json');
    assert.strictEqual(data.committed, 1420, 'committed = 5 premium x $200 + 14 standard x $30');
    assert.ok(!html.toLowerCase().includes('aircfo'), 'artifact must carry no airCFO branding');
    assert.ok(!/https?:\/\//.test(html), 'artifact must be self-contained (no external calls)');

    assert.strictEqual(run('draft_slack.py', root).status, 0, 'draft_slack should exit 0');
    const draft = fs.readFileSync(path.join(root, 'artifacts', '2026-06_slack_draft.txt'), 'utf8');
    assert.match(draft, /AI spend 2026-06/);
    assert.match(draft, /\$[\d,]+ total/);

    if (openpyxlAvailable()) {
      assert.ok(fs.existsSync(path.join(root, 'workbooks', 'ai_spend_output.xlsx')), 'output workbook when openpyxl present');
      assert.ok(fs.existsSync(path.join(root, 'workbooks', 'ai_spend_sources.xlsx')), 'sources workbook when openpyxl present');
    }
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('a period with meta but no export registers as missing and the artifact still builds', { skip }, () => {
  const root = freshWorkspace();
  try {
    const p = '2026-07';
    fs.mkdirSync(path.join(root, 'raw', p));
    fs.writeFileSync(path.join(root, 'raw', p, 'meta.json'),
      JSON.stringify({ period: p, days_covered: 31, partial: false, source: 'test' }));

    // Validating the absent export must fail loud (exit 1) and stamp "missing".
    const r = run('validate_surface_b.py', path.join(root, 'raw', p, 'overage_spend.csv'), p);
    assert.strictEqual(r.status, 1, 'missing export should exit non-zero');
    const st = JSON.parse(fs.readFileSync(path.join(root, 'raw', p, 'surface_b_status.json')));
    assert.strictEqual(st.state, 'missing');

    // ...but the pipeline still produces a summary and an artifact (no silent gap).
    assert.strictEqual(run('build_workbooks.py', root).status, 0);
    assert.strictEqual(run('build_artifact.py', root).status, 0);
    const html = fs.readFileSync(path.join(root, 'artifacts', '2026-07_ai_spend.html'), 'utf8');
    const data = embeddedData(html);
    assert.ok(data.periods.includes('2026-07'), 'the empty period still registers');
    assert.strictEqual(data.status.B.state, 'missing', 'Surface B carries the missing status');
    assert.ok(html.includes('Surface B'), 'artifact carries a Surface B banner');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('a period with a truncated meta.json degrades instead of crashing the whole build', { skip }, () => {
  const root = freshWorkspace();
  try {
    const p = '2026-08';
    fs.mkdirSync(path.join(root, 'raw', p));
    fs.writeFileSync(path.join(root, 'raw', p, 'overage_spend.csv'),
      'user_email,product,model,total_requests,total_prompt_tokens,total_completion_tokens,total_net_spend_usd,total_gross_spend_usd\n' +
      'ada@example.com,Chat,claude-opus-4-1,10,1000,500,5.00,5.25\n');
    fs.writeFileSync(path.join(root, 'raw', p, 'meta.json'), '{');

    const r = run('build_workbooks.py', root);
    assert.strictEqual(r.status, 0, `build_workbooks should still exit 0 with an invalid meta.json: ${r.stderr}`);
    const summary = JSON.parse(fs.readFileSync(path.join(root, 'workbooks', 'build_summary.json')));
    assert.ok(summary.periods.includes(p), 'the period with bad meta.json still registers');
    assert.ok(summary.meta_alerts && summary.meta_alerts[p] && summary.meta_alerts[p].startsWith('invalid'),
      'build_summary.json flags the bad meta.json instead of crashing silently');
    assert.deepStrictEqual(summary.periods.filter((x) => x !== p), PERIODS, 'the other periods still build normally');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
