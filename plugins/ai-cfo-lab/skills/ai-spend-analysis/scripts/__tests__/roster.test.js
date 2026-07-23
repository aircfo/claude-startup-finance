'use strict';
// Tests for the roster bootstrap/apply flow: pull people out of a real Surface B
// export into a fill-in roster, then convert that roster into the org_chart.csv /
// seats.csv the pipeline reads. Assertions are format-agnostic — they run the
// scripts and read the plain-CSV outputs, so they pass whether bootstrap wrote an
// .xlsx (openpyxl present) or a .csv fallback.
const { test } = require('node:test');
const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SKILL_DIR = path.resolve(__dirname, '..', '..');
const SCRIPTS = path.join(SKILL_DIR, 'scripts');
const FIXTURES = path.join(SKILL_DIR, 'fixtures');
const EXAMPLE = path.join(SKILL_DIR, 'config.example');
const PY = process.env.PYTHON || 'python3';

const pythonAvailable = () => spawnSync(PY, ['--version']).status === 0;
const run = (script, ...args) => spawnSync(PY, [path.join(SCRIPTS, script), ...args], { encoding: 'utf8' });
const skip = pythonAvailable() ? false : `${PY} not available`;

function tmp() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-roster-'));
}
function seedConfig(root) {
  fs.mkdirSync(path.join(root, 'config'), { recursive: true });
  for (const f of ['pipeline.json', 'thresholds.json']) {
    fs.copyFileSync(path.join(EXAMPLE, f), path.join(root, 'config', f));
  }
}
function seedExport(root, period = '2026-06') {
  fs.mkdirSync(path.join(root, 'raw', period), { recursive: true });
  fs.copyFileSync(path.join(FIXTURES, 'raw', period, 'overage_spend.csv'),
    path.join(root, 'raw', period, 'overage_spend.csv'));
}
function readCsv(p) {
  const [head, ...lines] = fs.readFileSync(p, 'utf8').trim().split(/\r?\n/);
  const cols = head.split(',');
  return lines.map((line) => {
    const cells = line.split(',');
    return Object.fromEntries(cols.map((c, i) => [c, cells[i] ?? '']));
  });
}
function byEmail(rows) {
  return Object.fromEntries(rows.map((r) => [r.email, r]));
}

test('bootstrap builds a roster from the export that applies to standard seats', { skip }, () => {
  const root = tmp();
  try {
    seedConfig(root);
    seedExport(root);

    const b = run('bootstrap_roster.py', root, '2026-06');
    assert.strictEqual(b.status, 0, `bootstrap failed: ${b.stderr}`);
    const hasRoster = fs.existsSync(path.join(root, 'config', 'roster.xlsx'))
      || fs.existsSync(path.join(root, 'config', 'roster.csv'));
    assert.ok(hasRoster, 'bootstrap should create a roster file (xlsx or csv)');

    assert.strictEqual(run('apply_roster.py', root).status, 0, 'apply should exit 0');
    const seats = readCsv(path.join(root, 'config', 'seats.csv'));
    const org = readCsv(path.join(root, 'config', 'org_chart.csv'));
    assert.ok(seats.length > 10, `expected many people from the export, got ${seats.length}`);
    assert.ok(seats.every((s) => s.seat_type === 'standard'), 'a fresh roster defaults everyone to standard');
    assert.ok(org.some((o) => o.email === 'ada@example.com'), 'people come from the real export emails');
    assert.ok(org.every((o) => o.department === ''), 'departments start blank until the user fills them');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('apply derives monthly_rate from seat_rates and carries departments through', { skip }, () => {
  const root = tmp();
  try {
    seedConfig(root); // config.example seat_rates: standard 30, premium 150
    fs.writeFileSync(path.join(root, 'config', 'roster.csv'),
      'email,name,department,seat_type\n'
      + 'ada@example.com,Ada Lovelace,Engineering,standard\n'
      + 'grace@example.com,Grace Hopper,Engineering,premium\n');

    assert.strictEqual(run('apply_roster.py', root).status, 0);
    const seats = byEmail(readCsv(path.join(root, 'config', 'seats.csv')));
    assert.strictEqual(seats['ada@example.com'].monthly_rate, '30', 'standard rate from seat_rates');
    assert.strictEqual(seats['grace@example.com'].monthly_rate, '150', 'premium rate from seat_rates');
    assert.strictEqual(seats['grace@example.com'].seat_type, 'premium');
    const org = byEmail(readCsv(path.join(root, 'config', 'org_chart.csv')));
    assert.strictEqual(org['grace@example.com'].department, 'Engineering');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('bootstrap never overwrites an existing (possibly filled-in) roster', { skip }, () => {
  const root = tmp();
  try {
    seedConfig(root);
    seedExport(root);
    const sentinel = 'email,name,department,seat_type\nkeep@example.com,Keep Me,Ops,premium\n';
    fs.writeFileSync(path.join(root, 'config', 'roster.csv'), sentinel);

    assert.strictEqual(run('bootstrap_roster.py', root, '2026-06').status, 0);
    assert.strictEqual(fs.readFileSync(path.join(root, 'config', 'roster.csv'), 'utf8'), sentinel,
      'an existing roster must be left byte-for-byte untouched');
    assert.ok(!fs.existsSync(path.join(root, 'config', 'roster.xlsx')), 'no second roster gets created');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('apply is a no-op when there is no roster (hand-maintained CSVs keep working)', { skip }, () => {
  const root = tmp();
  try {
    fs.mkdirSync(path.join(root, 'config'), { recursive: true });
    const org = 'email,name,department,team,manager,cost_center\nz@example.com,Zed,Sales,,,\n';
    const seats = 'email,seat_type,monthly_rate\nz@example.com,standard,20\n';
    fs.writeFileSync(path.join(root, 'config', 'org_chart.csv'), org);
    fs.writeFileSync(path.join(root, 'config', 'seats.csv'), seats);

    assert.strictEqual(run('apply_roster.py', root).status, 0);
    assert.strictEqual(fs.readFileSync(path.join(root, 'config', 'org_chart.csv'), 'utf8'), org,
      'org_chart.csv untouched when no roster is present');
    assert.strictEqual(fs.readFileSync(path.join(root, 'config', 'seats.csv'), 'utf8'), seats,
      'seats.csv untouched when no roster is present');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
