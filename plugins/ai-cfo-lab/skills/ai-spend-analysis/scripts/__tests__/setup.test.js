'use strict';
// Tests for the setup tools: doctor.py (offline checks, next step, the setup
// log), match_roster.py (every matching rule and every way it refuses to
// guess), install_mac_job.py (preview writes nothing; the generated command is
// well-formed) and uninstall.py (dry run by default). Synthetic data only.
const { test } = require('node:test');
const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SCRIPTS = path.resolve(__dirname, '..');
const PY = process.env.PYTHON || 'python3';
const skip = spawnSync(PY, ['--version']).status === 0 ? false : `${PY} not available`;

const ENV = { ...process.env };
delete ENV.ANTHROPIC_ADMIN_API_KEY;
const run = (script, args, env = ENV) =>
  spawnSync(PY, [path.join(SCRIPTS, script), ...args], { encoding: 'utf8', env });

function scaffolded() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-setup-'));
  assert.strictEqual(run('scaffold.py', [root]).status, 0);
  return root;
}
const readJson = (...parts) => JSON.parse(fs.readFileSync(path.join(...parts), 'utf8'));
const writeJson = (file, data) => fs.writeFileSync(file, JSON.stringify(data, null, 2));
const doctor = (root) => {
  const r = run('doctor.py', [root, '--offline', '--json']);
  return { status: r.status, ...JSON.parse(r.stdout) };
};
const byId = (report, id) => report.checks.find((c) => c.id === id);
const withRoot = (fn) => {
  const root = scaffolded();
  try { fn(root); } finally { fs.rmSync(root, { recursive: true, force: true }); }
};

test('the doctor on a fresh workspace points at the first real step and fails', { skip }, () => {
  withRoot((root) => {
    const report = doctor(root);
    assert.strictEqual(report.status, 1);
    assert.strictEqual(byId(report, 'workspace').status, 'ok');
    assert.strictEqual(report.next.id, 'company', 'the template company name is the first thing to fix');
    assert.strictEqual(byId(report, 'roster_real').status, 'fail', 'the sample @example.com roster is caught');
    assert.strictEqual(byId(report, 'seat_prices_confirmed').status, 'warn', 'template seat prices are questioned');
    assert.match(byId(report, 'admin_key').fix, /PASTE_ADMIN_KEY_HERE\.txt/, 'the key step names the exact file');
    assert.strictEqual(byId(report, 'admin_key').role, 'Console admin');
    assert.strictEqual(byId(report, 'org_id').role, 'claude.ai Owner');
  });
});

test('every doctor run is logged with statuses only, and setup time is measured', { skip }, () => {
  withRoot((root) => {
    fs.writeFileSync(path.join(root, '.secrets', 'anthropic_admin_key'), 'sk-ant-admin01-' + 'x'.repeat(40));
    doctor(root);
    const log = fs.readFileSync(path.join(root, 'logs', 'setup.jsonl'), 'utf8');
    assert.ok(!log.includes('sk-ant'), 'the log never holds the key');
    assert.ok(!log.includes('example.com'), 'the log never holds people');
    const runs = log.trim().split('\n').map((l) => JSON.parse(l));
    assert.strictEqual(runs.length, 1);
    assert.strictEqual(runs[0].checks.company, 'fail');

    // Two earlier runs a quarter of an hour apart, the second with nothing failing.
    const earlier = [{ at: '2026-10-01T10:00:00+00:00', checks: { company: 'fail' } },
      { at: '2026-10-01T10:15:00+00:00', checks: { company: 'ok' } }];
    fs.writeFileSync(path.join(root, 'logs', 'setup.jsonl'), earlier.map((r) => JSON.stringify(r)).join('\n') + '\n');
    assert.strictEqual(doctor(root).setup_minutes, 15);
  });
});

test('--fix-config adds missing settings without changing existing ones', { skip }, () => {
  withRoot((root) => {
    const cfgPath = path.join(root, 'config', 'pipeline.json');
    const cfg = readJson(cfgPath);
    delete cfg.dashboard_visibility;
    cfg.company_name = 'Northwind';
    writeJson(cfgPath, cfg);
    assert.strictEqual(byId(doctor(root), 'config_complete').status, 'warn');

    const r = run('doctor.py', [root, '--offline', '--fix-config']);
    assert.match(r.stdout, /added settings: dashboard_visibility/);
    const fixed = readJson(cfgPath);
    assert.strictEqual(fixed.dashboard_visibility, 'department');
    assert.strictEqual(fixed.company_name, 'Northwind');
  });
});

test('a filled roster with no premium seats or a one-person department is questioned', { skip }, () => {
  withRoot((root) => {
    fs.writeFileSync(path.join(root, 'config', 'org_chart.csv'),
      'email,name,department\na@acme.test,A,Sales\nb@acme.test,B,Sales\nc@acme.test,C,Sale\n');
    fs.writeFileSync(path.join(root, 'config', 'seats.csv'),
      'email,seat_type,monthly_rate\na@acme.test,standard,20\nb@acme.test,standard,20\nc@acme.test,standard,20\n');
    const report = doctor(root);
    assert.strictEqual(byId(report, 'roster_real').status, 'ok');
    assert.strictEqual(byId(report, 'roster_complete').status, 'warn');
    assert.match(byId(report, 'roster_departments').detail, /Sale\b/);
  });
});

// ---- match_roster.py ----

const ROSTER = ['email,name,department,seat_type',
  'ada.lovelace@acme.test,,,', 'grace@acme.test,,,', 'alan@acme.test,,,', 'linus.ext@acme.test,,,',
  'pat@acme.test,,,', 'newhire@acme.test,,,', 'kate.j@acme.test,,,'].join('\n') + '\n';
const HR = ['Employee,Email,Active T/F,Department',
  'Engineering,,,',
  'Ada Lovelace,,TRUE,Engineering',
  'Grace Hopper,,TRUE,Engineering',
  'Grace Hopper,,F,Engineering',
  'Alan Turing,,FALSE,Research',
  'Alan Kay,,TRUE,Design',
  'Linus (Fractional CTO),,TRUE,G&A',
  'Pat Smith,,TRUE,Sales',
  'Pat Jones,,TRUE,Support',
  'Katherine Johnson,kate.j@acme.test,TRUE,Finance'].join('\n') + '\n';

function rosterWorkspace() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-roster-'));
  fs.mkdirSync(path.join(root, 'config'));
  fs.writeFileSync(path.join(root, 'config', 'roster.csv'), ROSTER);
  fs.writeFileSync(path.join(root, 'hr.csv'), HR);
  return root;
}
const rosterRows = (root) => Object.fromEntries(fs.readFileSync(path.join(root, 'config', 'roster.csv'), 'utf8')
  .trim().split(/\r?\n/).slice(1).map((line) => { const [e, n, d, s] = line.split(','); return [e, { n, d, s }]; }));

test('the roster matcher applies each rule and reports what it will not guess', { skip }, () => {
  const root = rosterWorkspace();
  try {
    const r = run('match_roster.py', [root, path.join(root, 'hr.csv'), '--premium', 'Ada Lovelace']);
    assert.strictEqual(r.status, 2, 'unresolved people make the exit code non-zero');
    assert.match(r.stdout, /Matched 4 of 7/);
    assert.match(r.stdout, /\? alan@acme\.test could be: Alan Turing \/ Alan Kay/,
      'a departed Alan and an active Alan are two people: asked, not guessed');
    assert.match(r.stdout, /\? pat@acme\.test could be: Pat Smith \/ Pat Jones/);
    assert.match(r.stdout, /✗ newhire@acme\.test isn't in the HR export/);
    assert.match(r.stdout, /Nothing written/);
    assert.strictEqual(rosterRows(root)['ada.lovelace@acme.test'].d, '', 'a report-only run writes nothing');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('the roster matcher writes matches, resolutions and premium seats', { skip }, () => {
  const root = rosterWorkspace();
  try {
    const r = run('match_roster.py', [root, path.join(root, 'hr.csv'), '--premium', 'Ada Lovelace',
      '--set', 'pat@acme.test=Pat Jones', '--set', 'newhire@acme.test=New Hire|Sales',
      '--set', 'alan@acme.test=Alan Turing', '--write']);
    assert.strictEqual(r.status, 0, r.stdout);
    const rows = rosterRows(root);
    assert.deepStrictEqual(rows['ada.lovelace@acme.test'], { n: 'Ada Lovelace', d: 'Engineering', s: 'premium' });
    assert.strictEqual(rows['grace@acme.test'].d, 'Engineering', 'an inactive ("F") duplicate of the same person does not block a match');
    assert.strictEqual(rows['alan@acme.test'].d, 'Research', "the operator's choice is written, even for a departed employee");
    assert.strictEqual(rows['linus.ext@acme.test'].d, 'G&A', 'a first-name-only contractor row matches');
    assert.strictEqual(rows['kate.j@acme.test'].d, 'Finance', 'an email column beats name matching');
    assert.deepStrictEqual(rows['pat@acme.test'], { n: 'Pat Jones', d: 'Support', s: 'standard' });
    assert.deepStrictEqual(rows['newhire@acme.test'], { n: 'New Hire', d: 'Sales', s: 'standard' });
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

// ---- install_mac_job.py and uninstall.py ----

const mac = process.platform === 'darwin' ? false : 'macOS only';

test('the job installer previews everything and installs nothing without --load', { skip: skip || mac }, () => {
  withRoot((root) => {
    const cfgPath = path.join(root, 'config', 'pipeline.json');
    writeJson(cfgPath, { ...readJson(cfgPath), company_name: 'Northwind', org_id: 'org-test',
      dashboard_url: 'https://claude.ai/artifact/test', card_charges_source: 'ramp' });
    const bin = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-bin-'));
    for (const name of ['claude', 'uv']) {
      fs.writeFileSync(path.join(bin, name), '#!/bin/sh\nexit 0\n', { mode: 0o755 });
    }
    const r = run('install_mac_job.py', [root], { ...ENV, PATH: `${bin}:${ENV.PATH}` });
    fs.rmSync(bin, { recursive: true, force: true });
    assert.strictEqual(r.status, 0, r.stdout);
    assert.match(r.stdout, /--allowedTools "Bash\(python3:\*\),[^ "]+mcp__claude_ai_Ramp__ramp_get_transactions[^ "]*" < /,
      'one comma-separated tool list, prompt on stdin');
    assert.match(r.stdout, /--permission-mode dontAsk/);
    assert.match(r.stdout, /com\.aispend\.northwind/);
    assert.match(r.stdout, /Nothing installed/);
    assert.ok(!fs.existsSync(path.join(root, 'daily_refresh.sh')), 'preview writes no files');
    assert.ok(!readJson(cfgPath).mac_job_label);
  });
});

test('uninstall lists by default and removes only what was asked with --yes', { skip }, () => {
  withRoot((root) => {
    fs.mkdirSync(path.join(root, '.browser-profile'));
    fs.writeFileSync(path.join(root, '.secrets', 'anthropic_admin_key'), 'sk-ant-admin01-test');
    let r = run('uninstall.py', [root, '--remove-login', '--remove-key']);
    assert.match(r.stdout, /Would remove: Signed-in export browser profile/);
    assert.ok(fs.existsSync(path.join(root, '.browser-profile')), 'a dry run removes nothing');

    r = run('uninstall.py', [root, '--remove-login', '--yes']);
    assert.match(r.stdout, /Removed: Signed-in export browser profile/);
    assert.ok(!fs.existsSync(path.join(root, '.browser-profile')));
    assert.ok(fs.existsSync(path.join(root, '.secrets', 'anthropic_admin_key')), 'the key stays unless asked');
    assert.ok(fs.existsSync(path.join(root, 'config', 'pipeline.json')), 'config always stays');
  });
});

// ---- reconcile.py ----

test('reconciliation passes within $1 or 0.5% and fails beyond it', { skip }, () => {
  const fixtures = path.resolve(__dirname, '..', '..', 'fixtures');
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-reconcile-'));
  try {
    fs.cpSync(path.join(fixtures, 'config'), path.join(root, 'config'), { recursive: true });
    fs.cpSync(path.join(fixtures, 'raw'), path.join(root, 'raw'), { recursive: true });
    // 2026-05 in the fixtures: seats $1,420, API $155.
    let r = run('reconcile.py', [root, '2026-05', '--seats', '1420.80', '--api', '155']);
    assert.strictEqual(r.status, 0, r.stdout);
    assert.match(r.stdout, /Committed seats\s+1,420\.00\s+1,420\.80\s+-0\.80\s+pass/);
    assert.match(r.stdout, /Seat overage .* not checked/);
    assert.match(r.stdout, /seats are counted from today's roster/);

    r = run('reconcile.py', [root, '2026-05', '--api', '170']);
    assert.strictEqual(r.status, 1);
    assert.match(r.stdout, /API cost\s+155\.00\s+170\.00\s+-15\.00\s+FAIL \(allowed ±1\.00\)/);
    assert.match(r.stdout, /different Console organization/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('rerunning the matcher without --premium keeps the seat types already marked', { skip }, () => {
  const root = rosterWorkspace();
  try {
    fs.writeFileSync(path.join(root, 'config', 'roster.csv'),
      ROSTER.replace('ada.lovelace@acme.test,,,', 'ada.lovelace@acme.test,,,premium'));
    run('match_roster.py', [root, path.join(root, 'hr.csv'), '--write']);
    assert.strictEqual(rosterRows(root)['ada.lovelace@acme.test'].s, 'premium');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('an xlsx roster with its columns reordered is written by header, not position', { skip }, () => {
  if (spawnSync(PY, ['-c', 'import openpyxl']).status !== 0) return;
  const root = rosterWorkspace();
  try {
    fs.rmSync(path.join(root, 'config', 'roster.csv'));
    const xlsx = path.join(root, 'config', 'roster.xlsx');
    const make = spawnSync(PY, ['-c', `
import openpyxl
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Roster"
ws.append(["seat_type", "department", "email", "name"])
ws.append(["", "", "ada.lovelace@acme.test", ""])
wb.save(${JSON.stringify(xlsx)})`]);
    assert.strictEqual(make.status, 0, make.stderr.toString());
    run('match_roster.py', [root, path.join(root, 'hr.csv'), '--premium', 'Ada Lovelace', '--write']);
    const read = spawnSync(PY, ['-c', `
import openpyxl, json
ws = openpyxl.load_workbook(${JSON.stringify(xlsx)})["Roster"]
print(json.dumps([c.value for c in ws[2]]))`], { encoding: 'utf8' });
    assert.deepStrictEqual(JSON.parse(read.stdout), ['premium', 'Engineering', 'ada.lovelace@acme.test', 'Ada Lovelace']);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('--fix-config refuses an unreadable config instead of replacing it', { skip }, () => {
  withRoot((root) => {
    const cfgPath = path.join(root, 'config', 'pipeline.json');
    const broken = '{"company_name": "Northwind", "org_id": "keep-me",}';
    fs.writeFileSync(cfgPath, broken);
    const r = run('doctor.py', [root, '--offline', '--fix-config']);
    assert.strictEqual(r.status, 1);
    assert.match(r.stdout, /isn't valid JSON/);
    assert.strictEqual(fs.readFileSync(cfgPath, 'utf8'), broken, 'the file is untouched');
  });
});

test('the doctor reads the roster being filled in and picks up a pasted key', { skip }, () => {
  withRoot((root) => {
    fs.writeFileSync(path.join(root, 'config', 'roster.csv'),
      'email,name,department,seat_type\na@acme.test,A,Sales,premium\nb@acme.test,B,Sales,standard\n');
    const drop = path.join(root, 'PASTE_ADMIN_KEY_HERE.txt');
    fs.writeFileSync(drop, fs.readFileSync(drop, 'utf8') + 'sk-ant-admin01-' + 'k'.repeat(40) + '\n');
    const report = doctor(root);
    assert.strictEqual(byId(report, 'roster_real').status, 'ok', 'the sample org_chart.csv no longer counts');
    assert.strictEqual(byId(report, 'roster_complete').status, 'ok');
    assert.strictEqual(byId(report, 'admin_key').status, 'ok');
    assert.ok(!fs.existsSync(drop), 'the pasted key was moved into .secrets/');
  });
});

test('warnings with nothing to fix never block "All set"', { skip }, () => {
  withRoot((root) => {
    const cfgPath = path.join(root, 'config', 'pipeline.json');
    writeJson(cfgPath, { ...readJson(cfgPath), plan_tier: 'enterprise', company_name: 'Northwind',
      seat_rates: { standard: 20 }, dashboard_url: 'https://claude.ai/artifact/x', mac_job_label: 'com.test.none' });
    fs.writeFileSync(path.join(root, 'config', 'roster.csv'),
      'email,name,department,seat_type\na@acme.test,A,Sales,standard\nb@acme.test,B,Ops,standard\n');
    fs.mkdirSync(path.join(root, 'raw', '2026-06'), { recursive: true });
    fs.writeFileSync(path.join(root, 'raw', '2026-06', 'overage_spend.csv'), 'user_email\n');
    const report = doctor(root);
    const failing = report.checks.filter((c) => c.status === 'fail').map((c) => c.id);
    if (failing.length === 0) {
      assert.strictEqual(report.next, null);
      assert.ok(report.warnings.length > 0, 'the one-person departments are listed as warnings');
    } else {
      assert.deepStrictEqual(failing, ['mac_job'], 'only the uninstalled job may fail on a test machine');
    }
  });
});

test('Enterprise jobs need no org id and run no browser export; paths with spaces stay intact', { skip: skip || mac }, () => {
  const parent = fs.mkdtempSync(path.join(os.tmpdir(), 'ai spend '));
  const root = path.join(parent, 'My Workspace');
  try {
    assert.strictEqual(run('scaffold.py', [root]).status, 0);
    const cfgPath = path.join(root, 'config', 'pipeline.json');
    writeJson(cfgPath, { ...readJson(cfgPath), plan_tier: 'enterprise', company_name: 'Northwind',
      dashboard_url: 'https://claude.ai/artifact/test' });
    const bin = fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-bin-'));
    fs.writeFileSync(path.join(bin, 'claude'), '#!/bin/sh\nexit 0\n', { mode: 0o755 });
    const r = run('install_mac_job.py', [root], { ...ENV, PATH: `${bin}:/usr/bin:/bin` });
    fs.rmSync(bin, { recursive: true, force: true });
    assert.strictEqual(r.status, 0, r.stdout);
    assert.ok(!r.stdout.includes('fetch_surface_b_browser.py'), 'no browser stage on Enterprise');
    assert.match(r.stdout, /run_pipeline\.py '[^']*My Workspace' PERIOD/, 'paths are quoted in the job prompt');
  } finally { fs.rmSync(parent, { recursive: true, force: true }); }
});

test('a middle name doesn’t split one person in two, but a different surname always asks', { skip }, () => {
  const r = spawnSync(PY, ['-c', `
import json
from match_roster import prefer_active
def person(display, active):
    parts = display.split()
    return {"display": display, "first": parts[0].lower(), "last": parts[-1].lower(), "active": active}
same = prefer_active([person("Ada Byron Lovelace", True), person("Ada Lovelace", False)])
typo = prefer_active([person("Sam Leigh", True), person("Sam Lee", False)])
print(json.dumps([[p["display"] for p in same], [p["display"] for p in typo]]))`], { encoding: 'utf8', cwd: SCRIPTS });
  assert.strictEqual(r.status, 0, r.stderr);
  assert.deepStrictEqual(JSON.parse(r.stdout), [['Ada Byron Lovelace'], ['Sam Leigh', 'Sam Lee']]);
});
