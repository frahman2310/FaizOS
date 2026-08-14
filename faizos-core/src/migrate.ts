// Minimal migration runner. The project had none, so this is it: a schema_migrations table,
// a static registry in migrations/index.ts, and three commands.
//
//   tsx src/migrate.ts up     [--db <path>]   apply every unapplied migration, in order
//   tsx src/migrate.ts down   [--db <path>]   revert the single most recent applied migration
//   tsx src/migrate.ts status [--db <path>]   list migrations and their state
//
// Default database: faizos-core/data/faiz.db. Each migration runs inside a transaction.
import Database from 'better-sqlite3';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { migrations } from '../migrations/index.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB = join(HERE, '..', 'data', 'faiz.db');

function parseArgs(argv: string[]): { command: string; dbPath: string } {
  const command = argv[0] ?? 'status';
  const flagIndex = argv.indexOf('--db');
  const dbPath = flagIndex !== -1 && argv[flagIndex + 1] ? (argv[flagIndex + 1] as string) : DEFAULT_DB;
  return { command, dbPath };
}

function ensureMigrationsTable(db: Database.Database): void {
  db.exec(`CREATE TABLE IF NOT EXISTS schema_migrations (
    version    INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    applied_at TEXT NOT NULL
  )`);
}

function appliedVersions(db: Database.Database): Set<number> {
  const rows = db.prepare('SELECT version FROM schema_migrations ORDER BY version').all() as Array<{
    version: number;
  }>;
  return new Set(rows.map((r) => r.version));
}

export function migrateUp(dbPath: string): string[] {
  const db = new Database(dbPath, { fileMustExist: true });
  db.pragma('journal_mode = WAL');
  ensureMigrationsTable(db);
  const applied = appliedVersions(db);
  const ran: string[] = [];
  for (const m of migrations) {
    if (applied.has(m.version)) continue;
    const run = db.transaction(() => {
      m.up(db);
      db.prepare('INSERT INTO schema_migrations (version, name, applied_at) VALUES (?, ?, ?)').run(
        m.version,
        m.name,
        new Date().toISOString(),
      );
    });
    run();
    ran.push(`${m.version} ${m.name}`);
  }
  db.close();
  return ran;
}

export function migrateDown(dbPath: string): string | null {
  const db = new Database(dbPath, { fileMustExist: true });
  db.pragma('journal_mode = WAL');
  ensureMigrationsTable(db);
  const applied = appliedVersions(db);
  const target = [...migrations].reverse().find((m) => applied.has(m.version));
  if (!target) {
    db.close();
    return null;
  }
  const run = db.transaction(() => {
    target.down(db);
    db.prepare('DELETE FROM schema_migrations WHERE version = ?').run(target.version);
  });
  run();
  db.close();
  return `${target.version} ${target.name}`;
}

export function migrationStatus(dbPath: string): Array<{ version: number; name: string; applied: boolean }> {
  const db = new Database(dbPath, { fileMustExist: true });
  ensureMigrationsTable(db);
  const applied = appliedVersions(db);
  const status = migrations.map((m) => ({ version: m.version, name: m.name, applied: applied.has(m.version) }));
  db.close();
  return status;
}

// pathToFileURL handles spaces and other URL-encoded characters in the repo path.
const invokedDirectly =
  process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  const { command, dbPath } = parseArgs(process.argv.slice(2));
  if (command === 'up') {
    const ran = migrateUp(dbPath);
    console.log(ran.length ? `applied: ${ran.join(', ')}` : 'nothing to apply');
  } else if (command === 'down') {
    const reverted = migrateDown(dbPath);
    console.log(reverted ? `reverted: ${reverted}` : 'nothing to revert');
  } else if (command === 'status') {
    for (const s of migrationStatus(dbPath)) {
      console.log(`${s.applied ? 'applied' : 'pending'}  ${s.version} ${s.name}`);
    }
  } else {
    console.error(`unknown command: ${command} (use up | down | status)`);
    process.exit(1);
  }
}
