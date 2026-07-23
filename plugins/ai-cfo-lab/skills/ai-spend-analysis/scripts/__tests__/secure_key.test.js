'use strict';
// Tests for secure_key.py: the operator drops their Admin key into a plain file in
// the workspace root; the script extracts the sk-ant-… key, writes it to
// .secrets/anthropic_admin_key at 0600, and deletes the drop. The key must travel
// file → file only — never printed, never left lying around.
const { test } = require('node:test');
const assert = require('node:assert');
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const SKILL_DIR = path.resolve(__dirname, '..', '..');
const SCRIPTS = path.join(SKILL_DIR, 'scripts');
const PY = process.env.PYTHON || 'python3';

const pythonAvailable = () => spawnSync(PY, ['--version']).status === 0;
const run = (root) => spawnSync(PY, [path.join(SCRIPTS, 'secure_key.py'), root], { encoding: 'utf8' });
const skip = pythonAvailable() ? false : `${PY} not available`;

// A synthetic key (this file lives under __tests__, which the data-hygiene gate skips).
const FAKE_KEY = 'sk-ant-admin01-FAKEfakeFAKEfakeFAKEfakeFAKEfake1234567890abcdEFGH';

const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'ai-spend-key-'));
const secretPath = (root) => path.join(root, '.secrets', 'anthropic_admin_key');

test('ingests the key from the drop file, secures it 600, and deletes the drop', { skip }, () => {
  const root = tmp();
  try {
    const drop = path.join(root, 'PASTE_ADMIN_KEY_HERE.txt');
    // Instruction prose (which itself mentions "sk-ant-") must be ignored; only the real key is taken.
    fs.writeFileSync(drop,
      `HOW TO ADD YOUR KEY\nit begins with sk-ant- and is long\n----- paste below -----\n${FAKE_KEY}\n`);

    const r = run(root);
    assert.strictEqual(r.status, 0, r.stderr);
    assert.strictEqual(fs.readFileSync(secretPath(root), 'utf8'), FAKE_KEY, 'key stored verbatim');
    assert.ok(!fs.existsSync(drop), 'drop file is deleted after ingest');
    assert.strictEqual(fs.statSync(secretPath(root)).mode & 0o777, 0o600, 'secret file is chmod 600');
    assert.ok(!r.stdout.includes(FAKE_KEY), 'the key itself is never printed');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('is a no-op when there is no drop file', { skip }, () => {
  const root = tmp();
  try {
    assert.strictEqual(run(root).status, 0);
    assert.ok(!fs.existsSync(secretPath(root)), 'no secret written when nothing was dropped');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('leaves the drop file and writes no secret when it contains no key', { skip }, () => {
  const root = tmp();
  try {
    const drop = path.join(root, 'PASTE_ADMIN_KEY_HERE.txt');
    fs.writeFileSync(drop, 'I forgot to paste my key here.\n');

    assert.strictEqual(run(root).status, 0);
    assert.ok(fs.existsSync(drop), 'drop file is left in place so the user can fix it');
    assert.ok(!fs.existsSync(secretPath(root)), 'no secret written');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('also accepts the admin_key.txt filename', { skip }, () => {
  const root = tmp();
  try {
    fs.writeFileSync(path.join(root, 'admin_key.txt'), `${FAKE_KEY}\n`);

    assert.strictEqual(run(root).status, 0);
    assert.strictEqual(fs.readFileSync(secretPath(root), 'utf8'), FAKE_KEY);
    assert.ok(!fs.existsSync(path.join(root, 'admin_key.txt')), 'the alias drop is deleted too');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
