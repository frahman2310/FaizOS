/**
 * Deterministic session summary — written from DB facts, NOT the model.
 * Run modes:
 *   tsx src/session-log.ts --start   -> stamp session_start_ts = now (called by SessionStart hook)
 *   tsx src/session-log.ts           -> upsert this session's summary block into notebook/SESSIONS.md
 *
 * The Stop hook calls the default mode every turn; the block is keyed by session_start_ts, so all
 * turns in one session update the SAME block (idempotent). Guarantees a summary is logged every
 * session that shipped anything — with or without the model doing the close-loop.
 */
import Database from 'better-sqlite3';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { MODULES } from './curriculum.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');                       // project root (AI OS for Learning)
const DB_PATH = process.env.FAIZOS_DB || join(HERE, '..', 'data', 'faiz.db');
const LOG_PATH = process.env.FAIZOS_SESSIONS || join(ROOT, 'notebook', 'SESSIONS.md');
const HEADER = '# FaizOS — Session Log\n_Auto-written after every session by the Stop hook. Newest first._\n';

const db = new Database(DB_PATH);
const getMeta = (k: string): string =>
  (db.prepare('SELECT value FROM meta WHERE key=?').get(k) as { value: string } | undefined)?.value ?? '';
const setMeta = (k: string, v: string): void =>
  void db.prepare('INSERT INTO meta (key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run(k, v);

// nowISO passed in via arg (scripts can't call Date.now here reliably across environments) — but this
// is a plain node script, so real Date is fine.
const nowISO = () => new Date().toISOString();

if (process.argv.includes('--start')) {
  // Watermark the session: ships are keyed by mission id (shipped_at is date-only), revisions by ts.
  const maxId = (db.prepare('SELECT COALESCE(MAX(id),0) m FROM missions').get() as { m: number }).m;
  setMeta('session_start_mid', String(maxId));
  setMeta('session_start_ts', nowISO());
  process.exit(0);
}

// --- default mode: write the summary for the current session window ---
let start = getMeta('session_start_ts');
if (!start) {                                              // fallback: today's UTC midnight
  const d = new Date(); d.setUTCHours(0, 0, 0, 0); start = d.toISOString();
}
const startMid = Number(getMeta('session_start_mid') || 0);
const dayLabel = start.slice(0, 10);

const ships = db.prepare(
  "SELECT id,title,ship_url FROM missions WHERE status='shipped' AND id > ? ORDER BY id",
).all(startMid) as Array<{ id: number; title: string; ship_url: string | null }>;

if (ships.length === 0) process.exit(0);                   // nothing shipped this session -> nothing to log

const revs = db.prepare('SELECT topic FROM revisions WHERE ts >= ? ORDER BY ts').all(start) as Array<{ topic: string }>;
const milestones = revs.filter((r) => /Module \d+ Complete/i.test(r.topic)).map((r) => r.topic);
const learned = revs.filter((r) => !/Module \d+ Complete/i.test(r.topic)).map((r) => r.topic);

const touched = new Set((db.prepare('SELECT id FROM skills WHERE last_seen IS NOT NULL').all() as Array<{ id: string }>).map((r) => r.id));
const mods = MODULES.map((m) => m.skills.filter((s) => touched.has(s)).length / m.skills.length);
const coverage = Math.round((mods.reduce((a, c) => a + c, 0) / MODULES.length) * 100);
const done = mods.filter((c) => c >= 0.999).length;
const totalShips = (db.prepare("SELECT COUNT(*) c FROM missions WHERE status='shipped'").get() as { c: number }).c;

const block = [
  `<!-- session ${start} -->`,
  `## ${dayLabel} — ${ships.length} ship${ships.length === 1 ? '' : 's'}`,
  `**Shipped:** ${ships.map((s) => s.title).join(' · ')}`,
  learned.length ? `**Learned:** ${learned.join(' · ')}` : '',
  milestones.length ? `**🏁 Milestones:** ${milestones.join(' · ')}` : '',
  `**Coverage:** ${coverage}% · ${done}/20 modules complete · ${totalShips} total ships`,
  `<!-- /session ${start} -->`,
].filter(Boolean).join('\n');

let body = existsSync(LOG_PATH) ? readFileSync(LOG_PATH, 'utf8') : `${HEADER}\n`;
if (!body.startsWith('# FaizOS — Session Log')) body = `${HEADER}\n${body}`;
const open = `<!-- session ${start} -->`;
const close = `<!-- /session ${start} -->`;
const i = body.indexOf(open);
if (i !== -1) {                                            // replace existing block for this session
  const j = body.indexOf(close, i) + close.length;
  body = body.slice(0, i) + block + body.slice(j);
} else {                                                   // insert newest-first, right after the header
  const afterHeader = body.indexOf('\n', body.indexOf('_Auto-written')) + 1;
  body = body.slice(0, afterHeader) + '\n' + block + '\n' + body.slice(afterHeader);
}
writeFileSync(LOG_PATH, body);
console.log(`session log updated: ${ships.length} ships, ${coverage}% coverage -> ${LOG_PATH}`);
