'use strict';
// How the daily refresh behaves when something goes wrong: a failed export, a
// month first seen mid-month, a multi-month Ramp pull, an incomplete or non-USD
// card answer, a source that failed this run, a cloud-owned API cost. Each test
// pins one way stale or wrong numbers could otherwise reach the dashboard.
// Offline, synthetic fixtures only.
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
const skip = spawnSync(PY, ['--version']).status === 0 ? false : `${PY} not available`;

const ENV = { ...process.env };
delete ENV.ANTHROPIC_ADMIN_API_KEY;
const run = (script, ...args) => spawnSync(PY, [path.join(SCRIPTS, script), ...args], { encoding: 'utf8', env: ENV });
const python = (code) => spawnSync(PY, ['-c', code], { encoding: 'utf8', cwd: SCRIPTS, env: ENV });
const readJson = (...parts) => JSON.parse(fs.readFileSync(path.join(...parts), 'utf8'));
const writeJson = (file, data) => fs.writeFileSync(file, JSON.stringify(data));

function withWorkspace(overrides, fn) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-robust-'));
  try {
    fs.cpSync(path.join(FIXTURES, 'config'), path.join(root, 'config'), { recursive: true });
    fs.cpSync(path.join(FIXTURES, 'raw'), path.join(root, 'raw'), { recursive: true });
    const cfgPath = path.join(root, 'config', 'pipeline.json');
    writeJson(cfgPath, { ...readJson(cfgPath), ...overrides });
    fn(root);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

test('a failed export keeps the last good file, its true coverage, and is reported stale', { skip }, () => {
  withWorkspace({}, (root) => {
    const monthDir = path.join(root, 'raw', '2026-06');
    const before = readJson(monthDir, 'meta.json');
    const r = python(`
import datetime
from periods import record_fetch_error
record_fetch_error(${JSON.stringify(monthDir)}, "2026-06", datetime.date(2026, 6, 25),
                   "claude.ai session signed out", "daily browser export (failed)")`);
    assert.strictEqual(r.status, 0, r.stderr);
    const after = readJson(monthDir, 'meta.json');
    assert.strictEqual(after.end, before.end, 'the window does not move to yesterday');
    assert.strictEqual(after.days_covered, before.days_covered);
    assert.strictEqual(after.fetch_error, 'claude.ai session signed out');

    assert.strictEqual(run('validate_surface_b.py', path.join(monthDir, 'overage_spend.csv'), '2026-06').status, 1);
    const status = readJson(monthDir, 'surface_b_status.json');
    assert.strictEqual(status.state, 'stale');
    assert.match(status.detail, /signed out — showing the export through 2026-06-20/);
  });
});

test('a stale or failed source is left out of the upload rather than republished as fresh', { skip }, () => {
  withWorkspace({ card_charges_source: 'ramp' }, (root) => {
    run('ingest_ramp.py', root, '2026-06');
    writeJson(path.join(root, 'raw', '2026-06', 'surface_b_status.json'),
      { state: 'stale', detail: 'signed out — showing the export through 2026-06-20' });
    writeJson(path.join(root, 'raw', '2026-06', 'card_charges_status.json'), { state: 'error', detail: 'incomplete' });
    assert.strictEqual(run('build_dashboard_datasets.py', root).status, 0);
    const manifest = readJson(root, 'dashboard', 'manifest.json');
    assert.ok(!manifest.datasets.overage && !manifest.datasets.card_charges);
    assert.match(manifest.skipped.overage, /^stale/);
    assert.match(manifest.skipped.card_charges, /^error/);
    assert.ok(manifest.datasets.status, 'the status dataset still goes up, so the page says what failed');
    assert.ok(!fs.existsSync(path.join(root, 'dashboard', 'overage.json')));
  });
});

test('a month registered mid-month is refreshed once it ends; an export’s own meta is left alone', { skip }, () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-period-'));
  try {
    const r = python(`
import datetime, json, os
from periods import register_period, write_meta, coverage
d = ${JSON.stringify(dir)}
register_period(d + "/a", "2026-10", datetime.date(2026, 10, 6))
first = json.load(open(d + "/a/meta.json"))
register_period(d + "/a", "2026-10", datetime.date(2026, 11, 3))
later = json.load(open(d + "/a/meta.json"))
write_meta(d + "/b", "2026-10", coverage("2026-10", datetime.date(2026, 10, 10)), "manual export")
register_period(d + "/b", "2026-10", datetime.date(2026, 11, 3))
kept = json.load(open(d + "/b/meta.json"))
print(json.dumps([first["days_covered"], first["partial"], later["days_covered"], later["partial"], kept["days_covered"]]))`);
    assert.strictEqual(r.status, 0, r.stderr);
    assert.deepStrictEqual(JSON.parse(r.stdout), [5, true, 31, false, 9]);
  } finally { fs.rmSync(dir, { recursive: true, force: true }); }
});

test('a multi-month Ramp pull is filed by month and replaces each month instead of doubling it', { skip }, () => {
  withWorkspace({ api_cost_source: 'ramp' }, (root) => {
    const juneDir = path.join(root, 'raw', '2026-06');
    fs.rmSync(path.join(juneDir, 'ramp_api_cost_total.json'));
    const pull = { cost: { data: [
      { period_start_at: '2026-04-10T00:00:00+00:00', model: 'claude-opus-4-1', total_cost: 7 },
      { period_start_at: '2026-05-10T00:00:00+00:00', model: 'claude-opus-4-1', total_cost: 11 },
      { period_start_at: '2026-06-10T00:00:00+00:00', model: 'claude-opus-4-1', total_cost: 13 }] } };
    writeJson(path.join(juneDir, 'ramp_api_cost.json'), pull);
    run('ingest_ramp.py', root, '2026-06');
    run('ingest_ramp.py', root, '2026-06'); // the next day's pull covers the same months again
    const costs = (month) => fs.readFileSync(path.join(root, 'raw', month, 'api_usage_cost.csv'), 'utf8')
      .trim().split(/\r?\n/).slice(1).map((line) => Number(line.split(',')[10]));
    assert.deepStrictEqual(costs('2026-04'), [7]);
    assert.deepStrictEqual(costs('2026-05'), [11]);
    assert.deepStrictEqual(costs('2026-06'), [13]);
    assert.match(readJson(juneDir, 'surface_c_status.json').detail, /2026-04, 2026-05, 2026-06/);
  });
});

test('when a cloud job owns API cost, the Mac workspace neither imports nor flags it', { skip }, () => {
  withWorkspace({ api_cost_source: 'ramp', api_cost_refreshed_by: 'cloud' }, (root) => {
    const juneDir = path.join(root, 'raw', '2026-06');
    fs.rmSync(path.join(juneDir, 'ramp_api_cost.json'));
    const before = readJson(juneDir, 'surface_c_status.json');
    run('ingest_ramp.py', root, '2026-06');
    assert.deepStrictEqual(readJson(juneDir, 'surface_c_status.json'), before, 'no "missing" status is written');
  });
});

test('card pages without Ramp’s count, or a foreign charge without its dollar amount, are rejected', { skip }, () => {
  withWorkspace({ card_charges_source: 'ramp' }, (root) => {
    const juneDir = path.join(root, 'raw', '2026-06');
    const savedPath = path.join(juneDir, 'ramp_card_transactions.json');
    const pages = readJson(savedPath);

    delete pages[0].total_count;
    writeJson(savedPath, pages);
    run('ingest_ramp.py', root, '2026-06');
    assert.match(readJson(juneDir, 'card_charges_status.json').detail, /don't include Ramp's total_count/);

    pages[0].total_count = 7;
    pages[0].transactions[0] = { ...pages[0].transactions[0], original_currency: 'EUR', original_amount: '40.00' };
    writeJson(savedPath, pages);
    run('ingest_ramp.py', root, '2026-06');
    assert.match(readJson(juneDir, 'card_charges_status.json').detail, /EUR charge was saved without its US-dollar/);

    pages[0].transactions[0].amount = '$1,043.10';
    writeJson(savedPath, pages);
    run('ingest_ramp.py', root, '2026-06');
    assert.strictEqual(readJson(juneDir, 'card_charges_status.json').state, 'ok');
    const first = fs.readFileSync(path.join(juneDir, 'card_charges.csv'), 'utf8').split(/\r?\n/)[1];
    assert.match(first, /,1043\.1,/, 'the settled dollar amount is used, not the euro figure');
  });
});

test('the Claude Code fetch asks only for new days and the two still settling', { skip }, () => {
  const r = python(`
import datetime, json
from fetch_claude_code import days_to_fetch, days_needed
days = days_to_fetch("2026-10", datetime.date(2026, 10, 23))
have = {d.isoformat() for d in days if d.day not in (5,)}
print(json.dumps([d.isoformat() for d in days_needed(days, have)]))`);
  assert.strictEqual(r.status, 0, r.stderr);
  assert.deepStrictEqual(JSON.parse(r.stdout), ['2026-10-05', '2026-10-21', '2026-10-22']);
});
