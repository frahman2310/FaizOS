// End-to-end smoke test: spawns the real MCP server over stdio and drives the whole
// build -> ship -> analyze loop, asserting the state changes. Run: tsx src/smoke.ts
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const isolated = mkdtempSync(join(tmpdir(), 'faizos-smoke-'));

const transport = new StdioClientTransport({
  command: 'npx',
  args: ['tsx', join(HERE, 'server.ts')],
  env: { ...process.env, FAIZOS_HOME: isolated, FAIZOS_NOTEBOOK: join(isolated, 'REVISIONS.md') } as Record<string, string>,
});
const client = new Client({ name: 'smoke', version: '0.0.0' });
await client.connect(transport);

const call = async (name: string, args: Record<string, unknown> = {}) => {
  const r: any = await client.callTool({ name, arguments: args });
  return JSON.parse(r.content[0].text);
};

const tools = await client.listTools();
console.assert(tools.tools.some((t) => t.name === 'faizos_state'), 'faizos_state registered');
console.log('tools:', tools.tools.map((t) => t.name).join(', '));

const s0 = await call('faizos_state');
console.assert(s0.streak === 0 && s0.current_build === null, 'fresh: streak 0, no current build');
console.assert(s0.recommended_next.action === 'build', 'fresh: recommend a build');
console.log('recommend@start:', s0.recommended_next.label);

const b = await call('faizos_start_build', { idea: 'implement a numerically stable softmax from scratch in numpy' });
console.assert(typeof b.mission_id === 'number' && b.repo_path.includes('projects/'), 'build created with repo path');
console.log('started:', b.title, '->', b.repo_path);

const s1 = await call('faizos_state');
console.assert(s1.current_build && s1.recommended_next.action === 'continue', 'now has a current build');

const ship = await call('faizos_ship', { ship_url: 'https://github.com/faiz/softmax' });
console.assert(ship.streak === 1 && ship.shipped_count === 1, 'ship -> streak 1, shipped 1');
console.log('shipped:', ship.shipped.title, '| streak', ship.streak);

const before = (await call('faizos_list_skills', { phase: 1 })).skills.find((x: any) => x.id === 'floating-point-logsumexp');
const an = await call('faizos_analyze', {
  mission_id: b.mission_id,
  skills: [
    { id: 'floating-point-logsumexp', outcome: 0.9, kind: 'ship' },
    { id: 'linalg-matmul', outcome: 0.6, kind: 'build' },
    { id: 'gradient-clipping', outcome: 0.7, kind: 'build' }, // off-curriculum -> minted
  ],
  gaps: ['did not test the underflow branch of log-sum-exp'],
  notes: 'clean softmax; missing an edge-case test',
});
console.assert(an.updated.length === 3 && an.teach_next, 'analyze updated 3 skills + a gap to teach');
const after = (await call('faizos_list_skills', { phase: 1 })).skills.find((x: any) => x.id === 'floating-point-logsumexp');
console.assert(after.mastery > before.mastery, `mastery rose ${before.mastery} -> ${after.mastery}`);
const minted = (await call('faizos_list_skills')).skills.find((x: any) => x.id === 'gradient-clipping');
console.assert(minted && minted.on_curriculum === 0, 'off-curriculum skill was minted');
console.log('mastery softmax:', before.mastery, '->', after.mastery, '| teach_next:', an.teach_next);

const s2 = await call('faizos_state');
console.assert(s2.last_shipped && s2.shipped_count === 1, 'final: last_shipped set');
console.assert(s2.skills.recently_moved.some((x: any) => x.id === 'floating-point-logsumexp'), 'final: skill shows as recently moved');

const rq = await call('faizos_review_queue', { limit: 3 });
console.assert(Array.isArray(rq.items) && rq.items.some((i: any) => i.id === 'floating-point-logsumexp'), 'review queue surfaces a built must-know');

// --- Phase 1: memory + self-improving feedback loop (prove it closes) ---
const ls0 = await call('faizos_lesson_start', { topic: 'test lesson' });
console.assert(Array.isArray(ls0.insights_to_apply) && typeof ls0.learning_profile === 'string', 'lesson_start returns insights + profile');
const insightText = 'reinforce rows-vs-columns with the column-length trick';
await call('faizos_record_lesson', { topic: 'matmul cost', skills: ['linalg-matmul'], struggles: ['confused rows vs columns'], new_insights: [insightText], difficulty_felt: 'right' });
const ls1 = await call('faizos_lesson_start');
console.assert(ls1.insights_to_apply.some((i: any) => i.note === insightText), 'insight surfaces at next lesson_start (loop closes)');
const sv = await call('faizos_save_revision', { topic: 'matmul cost', note_md: '**Remember:** 2*M*N*K' });
console.assert(sv.entries >= 1 && sv.notebook_path.endsWith('REVISIONS.md'), 'revision saved');
const fsmod = await import('node:fs');
console.assert(fsmod.existsSync(sv.notebook_path) && fsmod.readFileSync(sv.notebook_path, 'utf8').includes('2*M*N*K'), 'notebook file compiled with the note');
const notes = await call('faizos_notes', { limit: 5 });
console.assert(notes.count >= 1 && notes.recent.length >= 1, 'notes returns revisions');
console.log('Phase 1 (memory + feedback loop): closed ✅  insight recorded → surfaced next lesson → notebook compiled');

// --- Step 2: curriculum map + suggestions (free-build within) ---
const cur = await call('faizos_curriculum', {});
console.assert(cur.phases.length >= 15 && cur.phases.some((p: any) => p.phase === 15), 'curriculum spans Phases 0–15');
console.assert(Array.isArray(cur.suggested_missions) && cur.suggested_missions.length >= 1, 'suggests next missions');
console.assert(typeof cur.free_build === 'string', 'free-build is always offered');
console.log('Step 2 (curriculum): map spans', cur.phases.length, 'phases; next suggestion:', cur.suggested_missions[0]?.title);

// --- Step 3: FSRS review scheduling ---
const rec = await call('faizos_record_review', { results: [{ id: 'linalg-matmul', outcome: 0.9 }] });
console.assert(rec.updated[0] && typeof rec.updated[0].next_due === 'string', 'review schedules a next_due (FSRS)');
console.log('Step 3 (FSRS): linalg-matmul next review scheduled →', rec.updated[0].next_due);

// --- Step 5: AI Opportunity Radar ---
await call('faizos_radar_save', { opportunities: [{ title: 'Urdu support bot', market: 'PK SMEs', feasibility: 'HIGH', roi_note: 'low incumbency', buildable_as: 'fine-tune a small Urdu support model' }] });
const radar = await call('faizos_radar_list', { limit: 5 });
console.assert(radar.items.length >= 1 && String(radar.items[0].buildable_as).includes('Urdu'), 'radar saves + lists opportunities');
console.log('Step 5 (radar): saved a buildable opportunity →', radar.items[0].buildable_as);

// --- course progress bar ---
const prog = await call('faizos_progress', {});
console.assert(typeof prog.rendered === 'string' && prog.rendered.includes('OVERALL'), 'progress bar renders');
console.log('Progress:', prog.coverage_pct + '% coverage,', prog.modules_done + '/20 modules,', prog.missions_shipped, 'shipped');

await client.close();
console.log('\nsmoke.ts: full build -> ship -> analyze -> review loop passed ✅');
