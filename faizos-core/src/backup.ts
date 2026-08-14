// Backs up the live database with the SQLite online backup API (WAL safe, unlike a plain file
// copy), then verifies the backup by opening it read only and comparing per table row counts
// against the live database. Exits non zero on any mismatch.
//
// Usage: tsx src/backup.ts [destDir]        default destDir: ~/faizos-backups
import Database from 'better-sqlite3';
import { existsSync, mkdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const LIVE = join(HERE, '..', 'data', 'faiz.db');

function tableNames(db: Database.Database): string[] {
  const rows = db
    .prepare("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
    .all() as Array<{ name: string }>;
  return rows.map((r) => r.name);
}

function rowCounts(db: Database.Database): Record<string, number> {
  const counts: Record<string, number> = {};
  for (const name of tableNames(db)) {
    const row = db.prepare(`SELECT COUNT(*) AS c FROM "${name}"`).get() as { c: number };
    counts[name] = row.c;
  }
  return counts;
}

async function main(): Promise<void> {
  if (!existsSync(LIVE)) {
    console.error(`live database not found: ${LIVE}`);
    process.exit(1);
  }
  const destDir = process.argv[2] ?? join(homedir(), 'faizos-backups');
  mkdirSync(destDir, { recursive: true });
  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const dest = join(destDir, `faiz-${stamp}.db`);

  const live = new Database(LIVE);
  const liveCounts = rowCounts(live);
  await live.backup(dest);
  live.close();

  const copy = new Database(dest, { readonly: true, fileMustExist: true });
  const copyCounts = rowCounts(copy);
  copy.close();

  let ok = true;
  console.log(`backup: ${dest}`);
  console.log(`${'table'.padEnd(16)} ${'live'.padStart(6)} ${'backup'.padStart(6)}`);
  const names = new Set([...Object.keys(liveCounts), ...Object.keys(copyCounts)]);
  for (const name of [...names].sort()) {
    const a = liveCounts[name] ?? -1;
    const b = copyCounts[name] ?? -1;
    const mark = a === b ? 'ok' : 'MISMATCH';
    if (a !== b) ok = false;
    console.log(`${name.padEnd(16)} ${String(a).padStart(6)} ${String(b).padStart(6)}  ${mark}`);
  }
  if (!ok) {
    console.error('BACKUP VERIFICATION FAILED');
    process.exit(1);
  }
  console.log('backup verified: every table row count matches');
}

await main();
