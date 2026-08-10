/**
 * Deterministic REVISION study guide — compiles your saved revision notes into notebook/REVISION.md,
 * grouped BY MODULE (module order), each module ending with its "Module Complete" capstone. This is
 * the re-learnable content (the notes YOU built), reorganized for study — regenerated after every
 * lesson/module so it's always current. Complements REVISIONS.md (chronological log).
 *
 * "Ensure it doesn't fail": defensive throughout; any error exits 0 and keeps the existing file.
 * Mapping is deterministic: a note's module = the module of its lesson's PRIMARY (first) skill;
 * "Module N Complete" notes attach to module N; anything unmatched lands in a Foundations section.
 */
import Database from 'better-sqlite3';
import { writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { MODULES } from './curriculum.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const DB_PATH = process.env.FAIZOS_DB || join(HERE, '..', 'data', 'faiz.db');
const OUT = process.env.FAIZOS_REVISION || join(ROOT, 'notebook', 'REVISION.md');

function main() {
  const db = new Database(DB_PATH, { readonly: true });

  const skillToModule = new Map<string, number>();
  for (const m of MODULES) for (const s of m.skills) skillToModule.set(s, m.id);
  const moduleName = new Map(MODULES.map((m) => [m.id, m.name]));

  // lesson topic -> its primary (first) skill's module
  const topicToModule = new Map<string, number>();
  const lessons = db.prepare('SELECT topic,skills FROM lessons ORDER BY id').all() as Array<{ topic: string; skills: string }>;
  for (const l of lessons) {
    let ids: string[] = [];
    try { ids = JSON.parse(l.skills || '[]'); } catch { ids = []; }
    for (const id of ids) { const mod = skillToModule.get(id); if (mod != null) { topicToModule.set(l.topic.trim(), mod); break; } }
  }

  const revisions = db.prepare('SELECT topic,note_md FROM revisions ORDER BY id').all() as Array<{ topic: string; note_md: string }>;

  const byModule = new Map<number, Array<{ topic: string; note_md: string; capstone: boolean }>>();
  const orphans: Array<{ topic: string; note_md: string }> = [];
  for (const r of revisions) {
    const done = /Module\s+(\d+)\s+Complete/i.exec(r.topic);
    let mod: number | undefined = done ? Number(done[1]) : topicToModule.get(r.topic.trim());
    if (mod == null || !moduleName.has(mod)) { orphans.push(r); continue; }
    const arr = byModule.get(mod) ?? [];
    arr.push({ topic: r.topic, note_md: r.note_md, capstone: !!done });
    byModule.set(mod, arr);
  }

  const lines: string[] = [];
  lines.push('# FaizOS — Revision Study Guide');
  lines.push('_Auto-compiled from your revision notes, grouped by module, regenerated after every lesson/module. Do not edit by hand — edit lessons, not this file._');
  lines.push('');

  const activeModules = MODULES.filter((m) => byModule.has(m.id));
  lines.push('## Contents');
  for (const m of activeModules) lines.push(`- [Module ${m.id} — ${m.name}](#module-${m.id})`);
  if (orphans.length) lines.push('- [Foundations & other](#foundations)');
  lines.push('');

  for (const m of activeModules) {
    const notes = byModule.get(m.id)!;
    // non-capstone notes first (in saved order), capstone last
    notes.sort((a, b) => Number(a.capstone) - Number(b.capstone));
    lines.push(`<a id="module-${m.id}"></a>`);
    lines.push(`# Module ${m.id} — ${m.name}`);
    lines.push('');
    for (const n of notes) {
      lines.push(`## ${n.capstone ? '🏁 ' : ''}${n.topic}`);
      lines.push('');
      // drop a leading markdown heading inside the note (our ## topic already labels it)
      lines.push(n.note_md.trim().replace(/^#{1,6}\s.*(?:\r?\n)+/, ''));
      lines.push('');
      lines.push('---');
      lines.push('');
    }
  }
  if (orphans.length) {
    lines.push('<a id="foundations"></a>');
    lines.push('# Foundations & other');
    lines.push('');
    for (const n of orphans) {
      lines.push(`## ${n.topic}`);
      lines.push('');
      lines.push(n.note_md.trim());
      lines.push('');
      lines.push('---');
      lines.push('');
    }
  }

  writeFileSync(OUT, lines.join('\n'));
  console.log(`REVISION.md compiled: ${revisions.length} notes across ${activeModules.length} modules -> ${OUT}`);
}

try { main(); } catch (e) {
  console.error('revision-compile failed (non-fatal, existing REVISION.md kept):', (e as Error).message);
}
process.exit(0);
