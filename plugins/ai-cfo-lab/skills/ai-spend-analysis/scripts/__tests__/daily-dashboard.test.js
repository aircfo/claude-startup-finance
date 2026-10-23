'use strict';
// Tests for the daily Claude Dashboard path: the Ramp importer, the Claude Code
// report flattening, the dataset builder (and its visibility filter), and the
// pipeline's period registration. Everything runs offline over the synthetic
// fixtures; the Admin-key env vars are stripped so no script can reach the network.
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
const DAILY_MONTH = '2026-06';

const OFFLINE_ENV = { ...process.env };
delete OFFLINE_ENV.ANTHROPIC_ADMIN_API_KEY;
delete OFFLINE_ENV.ANTHROPIC_ANALYTICS_API_KEY;

const skip = spawnSync(PY, ['--version']).status === 0 ? false : `${PY} not available`;
const run = (script, ...args) =>
  spawnSync(PY, [path.join(SCRIPTS, script), ...args], { encoding: 'utf8', env: OFFLINE_ENV });
const python = (code) =>
  spawnSync(PY, ['-c', code], { encoding: 'utf8', cwd: SCRIPTS, env: OFFLINE_ENV });

function freshWorkspace(pipelineOverrides = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-daily-'));
  fs.cpSync(path.join(FIXTURES, 'config'), path.join(root, 'config'), { recursive: true });
  fs.cpSync(path.join(FIXTURES, 'raw'), path.join(root, 'raw'), { recursive: true });
  const pipelinePath = path.join(root, 'config', 'pipeline.json');
  const pipeline = JSON.parse(fs.readFileSync(pipelinePath, 'utf8'));
  fs.writeFileSync(pipelinePath, JSON.stringify({ ...pipeline, ...pipelineOverrides }));
  return root;
}

const readJson = (...parts) => JSON.parse(fs.readFileSync(path.join(...parts), 'utf8'));
const readRows = (root, id) => readJson(root, 'dashboard', `${id}.json`).rows;
const csvLines = (file) => fs.readFileSync(file, 'utf8').trim().split(/\r?\n/);
const withWorkspace = (overrides, fn) => {
  const root = freshWorkspace(overrides);
  try { fn(root); } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

test('the Ramp importer turns saved answers into API cost and card charge tables', { skip }, () => {
  withWorkspace({ api_cost_source: 'ramp', card_charges_source: 'ramp' }, (root) => {
    const monthDir = path.join(root, 'raw', DAILY_MONTH);
    assert.strictEqual(run('ingest_ramp.py', root, DAILY_MONTH).status, 0);

    const apiLines = csvLines(path.join(monthDir, 'api_usage_cost.csv'));
    assert.strictEqual(apiLines.length - 1, 40, 'one cost row per day (20) per model (2)');
    assert.match(apiLines[1], /^cost,2026-06-01,\(via Ramp\),,claude-opus-4-1,/);
    assert.match(apiLines[1], /Ramp estimate from token usage$/);

    const cardLines = csvLines(path.join(monthDir, 'card_charges.csv'));
    assert.strictEqual(cardLines.length - 1, 6, 'both saved pages read, the declined charge dropped');
    assert.strictEqual(readJson(monthDir, 'card_charges_status.json').state, 'ok');
    assert.strictEqual(readJson(monthDir, 'surface_c_status.json').source, 'ramp_api_cost');
  });
});

test('a configured Ramp source with no saved answer is reported missing, not zero', { skip }, () => {
  withWorkspace({ card_charges_source: 'ramp' }, (root) => {
    const monthDir = path.join(root, 'raw', DAILY_MONTH);
    fs.rmSync(path.join(monthDir, 'ramp_card_transactions.json'));
    assert.strictEqual(run('ingest_ramp.py', root, DAILY_MONTH).status, 0);
    assert.strictEqual(readJson(monthDir, 'card_charges_status.json').state, 'missing');
    assert.ok(!fs.existsSync(path.join(monthDir, 'card_charges.csv')), 'no empty table is written');
  });
});

test('a saved card answer missing a page is rejected, not published', { skip }, () => {
  withWorkspace({ card_charges_source: 'ramp' }, (root) => {
    const monthDir = path.join(root, 'raw', DAILY_MONTH);
    const savedPath = path.join(monthDir, 'ramp_card_transactions.json');
    const pages = readJson(savedPath);
    fs.writeFileSync(savedPath, JSON.stringify(pages.slice(0, 1)));
    run('ingest_ramp.py', root, DAILY_MONTH);
    const status = readJson(monthDir, 'card_charges_status.json');
    assert.strictEqual(status.state, 'error');
    assert.match(status.detail, /4 of the 7 transactions/);
    assert.ok(!fs.existsSync(path.join(monthDir, 'card_charges.csv')));
  });
});

test('saved daily API cost that does not add up to Ramp’s total is rejected', { skip }, () => {
  withWorkspace({ api_cost_source: 'ramp' }, (root) => {
    const monthDir = path.join(root, 'raw', DAILY_MONTH);
    const savedPath = path.join(monthDir, 'ramp_api_cost.json');
    const saved = readJson(savedPath);
    saved.cost.data[0].total_cost += 5;
    fs.writeFileSync(savedPath, JSON.stringify(saved));
    const before = fs.readFileSync(path.join(monthDir, 'api_usage_cost.csv'), 'utf8');
    run('ingest_ramp.py', root, DAILY_MONTH);
    const status = readJson(monthDir, 'surface_c_status.json');
    assert.strictEqual(status.state, 'error');
    assert.match(status.detail, /claude-opus-4-1 daily rows sum to .* but Ramp's total is/);
    assert.strictEqual(fs.readFileSync(path.join(monthDir, 'api_usage_cost.csv'), 'utf8'), before,
      'the previous table is left as it was');
  });
});

test('the Claude Code report flattens to one row per model with dollars from cents', { skip }, () => {
  const r = python(`
import json
from fetch_claude_code import flatten
user = {"actor": {"type": "user_actor", "email_address": "Ada@Example.com"}, "date": "2026-06-03T00:00:00Z",
        "customer_type": "subscription", "subscription_type": "team", "is_remote": False,
        "model_breakdown": [{"model": "m1", "estimated_cost": {"amount": 186, "currency": "USD"},
                             "tokens": {"input": 1, "output": 2, "cache_read": 3, "cache_creation": 4}},
                            {"model": "m2", "estimated_cost": {"amount": 42, "currency": "USD"}, "tokens": {}}]}
key = {"actor": {"type": "api_actor", "api_key_name": "ci"}, "date": "2026-06-03T00:00:00Z", "model_breakdown": []}
print(json.dumps([flatten(user), flatten(key)]))`);
  assert.strictEqual(r.status, 0, r.stderr);
  const [userRows, keyRows] = JSON.parse(r.stdout);
  assert.strictEqual(userRows.length, 2);
  assert.strictEqual(userRows[0].email, 'ada@example.com');
  assert.strictEqual(userRows[0].date, '2026-06-03');
  assert.strictEqual(userRows[0].est_cost_usd, 1.86);
  assert.strictEqual(userRows[1].output_tokens, 0, 'missing token counts read as zero');
  assert.deepStrictEqual(keyRows, [], 'a record with no model breakdown adds no rows');
});

test('the Claude Code fetch covers the period through yesterday only', { skip }, () => {
  const r = python(`
import datetime
from fetch_claude_code import days_to_fetch
today = datetime.date(2026, 6, 21)
print(len(days_to_fetch("2026-06", today)), len(days_to_fetch("2026-05", today)), len(days_to_fetch("2026-07", today)))`);
  assert.strictEqual(r.status, 0, r.stderr);
  assert.strictEqual(r.stdout.trim(), '20 31 0');
});

test('the browser export covers through yesterday and finishes a half-captured month first', { skip }, () => {
  withWorkspace({}, (root) => {
    fs.mkdirSync(path.join(root, 'raw', '2026-09'), { recursive: true });
    fs.writeFileSync(path.join(root, 'raw', '2026-09', 'meta.json'), JSON.stringify({ partial: true }));
    const r = python(`
import datetime, json
from fetch_surface_b_browser import export_window, target_periods, looks_like_export
d = datetime.date
show = lambda w: None if w is None else [w[0].isoformat(), w[1].isoformat(), w[2]]
print(json.dumps({
  "mid": show(export_window("2026-10", d(2026, 10, 23))),
  "closing": show(export_window("2026-09", d(2026, 10, 1))),
  "first_day": show(export_window("2026-10", d(2026, 10, 1))),
  "catch_up": target_periods(${JSON.stringify(root)}, d(2026, 10, 23)),
  "on_first": target_periods(${JSON.stringify(root)}, d(2026, 10, 1)),
  "export": looks_like_export("user_email,product,total_net_spend_usd\\nx"),
  "login_page": looks_like_export("<!doctype html><title>Sign in</title>")}))`);
    assert.strictEqual(r.status, 0, r.stderr);
    const out = JSON.parse(r.stdout);
    assert.deepStrictEqual(out.mid, ['2026-10-01', '2026-10-22', true]);
    assert.deepStrictEqual(out.closing, ['2026-09-01', '2026-09-30', false], 'the 1st closes out the previous month');
    assert.strictEqual(out.first_day, null, 'nothing to fetch for a month with no completed days');
    assert.deepStrictEqual(out.catch_up, ['2026-09', '2026-10'], 'a partial previous month is finished first');
    assert.deepStrictEqual(out.on_first, ['2026-09']);
    assert.strictEqual(out.export, true);
    assert.strictEqual(out.login_page, false, 'a sign-in page is never saved as the export');
  });
});

test('a failed scheduled fetch says why on the dashboard', { skip }, () => {
  withWorkspace({}, (root) => {
    const monthDir = path.join(root, 'raw', '2026-07');
    fs.mkdirSync(monthDir);
    fs.writeFileSync(path.join(monthDir, 'meta.json'),
      JSON.stringify({ period: '2026-07', fetch_error: 'claude.ai session signed out — run fetch_surface_b_browser.py --login' }));
    run('validate_surface_b.py', path.join(monthDir, 'overage_spend.csv'), '2026-07');
    const status = readJson(monthDir, 'surface_b_status.json');
    assert.strictEqual(status.state, 'missing');
    assert.match(status.detail, /signed out/);
  });
});

test('department visibility uploads no names or emails', { skip }, () => {
  withWorkspace({ card_charges_source: 'ramp' }, (root) => {
    run('ingest_ramp.py', root, DAILY_MONTH);
    assert.strictEqual(run('build_dashboard_datasets.py', root).status, 0);

    const manifest = readJson(root, 'dashboard', 'manifest.json');
    assert.strictEqual(manifest.visibility, 'department');
    const names = fs.readFileSync(path.join(root, 'config', 'org_chart.csv'), 'utf8')
      .trim().split('\n').slice(1).map((line) => line.split(',')[1]);
    for (const id of Object.keys(manifest.datasets)) {
      const text = fs.readFileSync(path.join(root, 'dashboard', `${id}.json`), 'utf8');
      assert.ok(!text.includes('@example.com'), `${id} must not carry an email`);
      for (const name of names) assert.ok(!text.includes(name), `${id} must not carry ${name}`);
    }
    const departments = new Set(readRows(root, 'card_charges').map((r) => r.department));
    assert.ok(departments.has('(unmapped)'), 'a cardholder missing from the roster lands in (unmapped)');
    assert.ok(new Set(readRows(root, 'claude_code').map((r) => r.department)).has('(API keys)'));
  });
});

test('person visibility keeps per-person rows joined to the roster', { skip }, () => {
  withWorkspace({ dashboard_visibility: 'person', card_charges_source: 'ramp' }, (root) => {
    run('ingest_ramp.py', root, DAILY_MONTH);
    assert.strictEqual(run('build_dashboard_datasets.py', root).status, 0);

    const ada = readRows(root, 'claude_code').filter((r) => r.email === 'ada@example.com');
    assert.ok(ada.length > 0);
    assert.ok(ada.every((r) => r.name === 'Ada Lovelace' && r.department === 'Engineering'));
    const cards = readRows(root, 'card_charges');
    assert.ok(cards.some((r) => r.cardholder === 'Steve Wozniak' && r.department === 'Product'));
    assert.ok(readRows(root, 'overage').every((r) => r.email && r.period));
  });
});

test('--only writes just the named datasets and records the Ramp query behind them', { skip }, () => {
  withWorkspace({ api_cost_source: 'ramp' }, (root) => {
    run('ingest_ramp.py', root, DAILY_MONTH);
    assert.strictEqual(run('build_dashboard_datasets.py', root, '--only', 'api_cost').status, 0);

    assert.deepStrictEqual(fs.readdirSync(path.join(root, 'dashboard')).sort(), ['api_cost.json', 'manifest.json']);
    const entry = readJson(root, 'dashboard', 'manifest.json').datasets.api_cost;
    assert.strictEqual(entry.request.tool, 'ramp_get_ai_token_spend_aggregates');
    assert.strictEqual(entry.request.args.start_at, '2026-04-01');
    const juneDays = readRows(root, 'api_cost').filter((r) => r.period === DAILY_MONTH);
    assert.strictEqual(new Set(juneDays.map((r) => r.date)).size, 20, 'daily rows keep their own dates');
  });
});

test('an unknown visibility setting stops the build instead of guessing', { skip }, () => {
  withWorkspace({ dashboard_visibility: 'everyone' }, (root) => {
    const r = run('build_dashboard_datasets.py', root);
    assert.strictEqual(r.status, 1);
    assert.match(r.stdout, /must be 'department' or 'person'/);
  });
});

// The page's calcs run in each viewer's browser. Load the page script with just
// enough of the browser and the dashboard runtime stubbed to collect them.
function pageCalcs() {
  const html = fs.readFileSync(path.join(SCRIPTS, 'dashboard_page.html'), 'utf8');
  const script = html.slice(html.indexOf('<script>') + '<script>'.length, html.indexOf('</script>'));
  const calcs = {};
  const formatter = () => (value) => String(value);
  const sandbox = {
    dash: { calc: (id, spec) => { calcs[id] = spec; }, onData: () => {}, data: () => ({ status: 'loading', data: [] }),
      colors: [], setLink: () => {} },
    d3: { format: formatter, utcFormat: formatter },
    document: { querySelectorAll: () => [], getElementById: () => null },
    location: { hash: '' },
    Intl,
  };
  require('node:vm').runInNewContext(script, sandbox);
  return calcs;
}

test('the dashboard page adds the three surfaces and projects a partial month', { skip }, () => {
  withWorkspace({ api_cost_source: 'ramp', card_charges_source: 'ramp' }, (root) => {
    run('ingest_ramp.py', root, DAILY_MONTH);
    assert.strictEqual(run('build_dashboard_datasets.py', root).status, 0);
    const calcs = pageCalcs();
    const rowsFor = (id) => readRows(root, id);
    const call = (id, inputs) => calcs[id].fn(...calcs[id].inputs.map((input) => inputs[input] || rowsFor(input)));

    const monthly = call('monthly', {});
    assert.deepStrictEqual(monthly.map((m) => m.period), ['2026-04', '2026-05', DAILY_MONTH]);
    const june = monthly[2];
    const sum = (rows, field) => rows.filter((r) => r.period === DAILY_MONTH).reduce((t, r) => t + r[field], 0);
    const overage = sum(rowsFor('overage'), 'net_usd');
    const api = sum(rowsFor('api_cost'), 'cost_usd');
    assert.strictEqual(june.seats_usd, 1420, 'committed = 5 premium x $200 + 14 standard x $30');
    assert.ok(Math.abs(june.total_usd - (1420 + overage + api)) < 1e-6);
    assert.ok(Math.abs(june.projected_usd - (1420 + (overage + api) * 30 / 20)) < 1e-6,
      'only the variable surfaces scale to the full month');
    assert.strictEqual(monthly[1].projected_usd, monthly[1].total_usd, 'a full month projects to itself');
    assert.deepStrictEqual(call('current', { monthly }), [june]);

    const cardTotal = call('card_total', {})[0];
    assert.ok(cardTotal.amount_usd > 0 && cardTotal.period === DAILY_MONTH);
    const flags = call('flag_rows', {});
    assert.deepStrictEqual(flags.map((f) => f.id), flags.map((_, i) => String(i + 1)));
    assert.ok(!flags.some((f) => f.flag_label.includes('_')));
    const shares = call('models', {}).reduce((t, r) => t + r.share, 0);
    assert.ok(Math.abs(shares - 1) < 1e-9, 'model family shares add to 100%');
  });
});

test('the pipeline registers a month that has no export yet and still builds the datasets', { skip }, () => {
  withWorkspace({}, (root) => {
    const r = run('run_pipeline.py', root, '2026-07');
    assert.strictEqual(r.status, 0, r.stderr);
    const meta = readJson(root, 'raw', '2026-07', 'meta.json');
    assert.match(meta.source, /registered by run_pipeline/);
    const status = readRows(root, 'status');
    assert.ok(status.some((s) => s.period === '2026-07' && s.state === 'missing'),
      'the missing export is flagged on the dashboard');
    assert.ok(readRows(root, 'periods').some((p) => p.period === '2026-07'));
  });
});
