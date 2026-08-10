/**
 * Deterministic CONTENT & BUILD summary — regenerated from DB facts, not the model.
 * Writes notebook/SUMMARY.md: overall coverage, per-module breakdown (skills + the builds that
 * touched them), and a full build table. Idempotent full rebuild, so running it after every lesson
 * or module completion always reflects the true current state. Wired into the Stop hook.
 *
 * "Ensure it doesn't fail": every DB read is defensive and the whole thing is wrapped so any error
 * exits 0 (never blocks the hook) and leaves any existing SUMMARY.md untouched.
 */
import Database from 'better-sqlite3';
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { MODULES } from './curriculum.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const DB_PATH = process.env.FAIZOS_DB || join(HERE, '..', 'data', 'faiz.db');
const OUT = process.env.FAIZOS_SUMMARY || join(ROOT, 'notebook', 'SUMMARY.md');

function main() {
  const db = new Database(DB_PATH, { readonly: true });
  const bar = (f: number, w = 20) => { const k = Math.round(Math.max(0, Math.min(1, f)) * w); return '▓'.repeat(k) + '░'.repeat(w - k); };
  const pct = (f: number) => `${Math.round(f * 100)}%`;

  const skills = db.prepare('SELECT id,name,last_seen,mastery FROM skills WHERE on_curriculum=1').all() as Array<{ id: string; name: string; last_seen: string | null; mastery: number }>;
  const skillName = new Map(skills.map((s) => [s.id, s.name]));
  const touched = new Set(skills.filter((s) => s.last_seen).map((s) => s.id));

  const missions = db.prepare("SELECT id,title,status,shipped_at FROM missions ORDER BY id").all() as Array<{ id: number; title: string; status: string; shipped_at: string | null }>;
  const lessons = db.prepare('SELECT mission_id,skills FROM lessons').all() as Array<{ mission_id: number | null; skills: string }>;

  // mission id -> set of skill ids it exercised (from its lessons)
  const missionSkills = new Map<number, Set<string>>();
  for (const l of lessons) {
    if (l.mission_id == null) continue;
    let ids: string[] = [];
    try { ids = JSON.parse(l.skills || '[]'); } catch { ids = []; }
    const set = missionSkills.get(l.mission_id) ?? new Set<string>();
    for (const id of ids) set.add(id);
    missionSkills.set(l.mission_id, set);
  }
  const missionById = new Map(missions.map((m) => [m.id, m]));

  const mods = MODULES.map((m) => {
    const hit = m.skills.filter((s) => touched.has(s));
    // builds that touched any of this module's skills
    const buildIds = [...missionSkills.entries()]
      .filter(([, set]) => m.skills.some((s) => set.has(s)))
      .map(([mid]) => mid)
      .filter((mid) => missionById.has(mid))
      .sort((a, b) => a - b);
    return { ...m, cov: hit.length / m.skills.length, hit, buildIds };
  });
  const coverage = mods.reduce((a, m) => a + m.cov, 0) / MODULES.length;
  const done = mods.filter((m) => m.cov >= 0.999).length;
  const shipped = missions.filter((m) => m.status === 'shipped');

  const lines: string[] = [];
  lines.push('# FaizOS — Content & Build Summary');
  lines.push('_Auto-generated from your progress after every lesson/module (Stop hook). Do not edit by hand._');
  lines.push('');
  lines.push(`**${pct(coverage)} coverage** · ${done}/20 modules complete · ${shipped.length} builds shipped · ${touched.size}/${skills.length} skills touched`);
  lines.push('');
  lines.push('```');
  lines.push(`OVERALL  ${bar(coverage)} ${pct(coverage)}`);
  lines.push('```');
  lines.push('');
  lines.push('## Modules');
  for (const m of mods) {
    if (m.cov === 0) continue;
    const mark = m.cov >= 0.999 ? '✅' : '🔄';
    lines.push(`### ${mark} Module ${m.id} — ${m.name} (${pct(m.cov)})`);
    lines.push(`- **skills:** ${m.skills.map((s) => `${touched.has(s) ? '✓' : '·'} ${skillName.get(s) ?? s}`).join(' · ')}`);
    if (m.buildIds.length) {
      lines.push(`- **builds:** ${m.buildIds.map((id) => `#${id} ${missionById.get(id)!.title}`).join(' · ')}`);
    }
    lines.push('');
  }
  lines.push('## All builds shipped (newest first)');
  lines.push('| # | build | skills exercised | shipped |');
  lines.push('|---|-------|------------------|---------|');
  for (const mm of [...shipped].reverse()) {
    const sk = [...(missionSkills.get(mm.id) ?? new Set())].map((s) => skillName.get(s) ?? s).join(', ') || '—';
    lines.push(`| ${mm.id} | ${mm.title} | ${sk} | ${mm.shipped_at ?? ''} |`);
  }
  lines.push('');

  writeFileSync(OUT, lines.join('\n') + '\n');
  console.log(`SUMMARY.md written: ${pct(coverage)} coverage, ${shipped.length} builds -> ${OUT}`);
}

try { main(); } catch (e) {
  console.error('build-summary failed (non-fatal, existing SUMMARY.md kept):', (e as Error).message);
}
process.exit(0);   // never fail the hook
