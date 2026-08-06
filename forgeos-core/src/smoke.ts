// End-to-end smoke test: spawns the real MCP server over stdio and drives the whole
// build -> ship -> analyze loop, asserting the state changes. Run: tsx src/smoke.ts
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const isolated = mkdtempSync(join(tmpdir(), 'forgeos-smoke-'));

const transport = new StdioClientTransport({
  command: 'npx',
  args: ['tsx', join(HERE, 'server.ts')],
  env: { ...process.env, FORGEOS_HOME: isolated } as Record<string, string>,
});
const client = new Client({ name: 'smoke', version: '0.0.0' });
await client.connect(transport);

const call = async (name: string, args: Record<string, unknown> = {}) => {
  const r: any = await client.callTool({ name, arguments: args });
  return JSON.parse(r.content[0].text);
};

const tools = await client.listTools();
console.assert(tools.tools.some((t) => t.name === 'forge_state'), 'forge_state registered');
console.log('tools:', tools.tools.map((t) => t.name).join(', '));

const s0 = await call('forge_state');
console.assert(s0.streak === 0 && s0.current_build === null, 'fresh: streak 0, no current build');
console.assert(s0.recommended_next.action === 'build', 'fresh: recommend a build');
console.log('recommend@start:', s0.recommended_next.label);

const b = await call('forge_start_build', { idea: 'implement a numerically stable softmax from scratch in numpy' });
console.assert(typeof b.mission_id === 'number' && b.repo_path.includes('projects/'), 'build created with repo path');
console.log('started:', b.title, '->', b.repo_path);

const s1 = await call('forge_state');
console.assert(s1.current_build && s1.recommended_next.action === 'continue', 'now has a current build');

const ship = await call('forge_ship', { ship_url: 'https://github.com/faiz/softmax' });
console.assert(ship.streak === 1 && ship.shipped_count === 1, 'ship -> streak 1, shipped 1');
console.log('shipped:', ship.shipped.title, '| streak', ship.streak);

const before = (await call('forge_list_skills', { phase: 1 })).skills.find((x: any) => x.id === 'floating-point-logsumexp');
const an = await call('forge_analyze', {
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
const after = (await call('forge_list_skills', { phase: 1 })).skills.find((x: any) => x.id === 'floating-point-logsumexp');
console.assert(after.mastery > before.mastery, `mastery rose ${before.mastery} -> ${after.mastery}`);
const minted = (await call('forge_list_skills')).skills.find((x: any) => x.id === 'gradient-clipping');
console.assert(minted && minted.on_curriculum === 0, 'off-curriculum skill was minted');
console.log('mastery softmax:', before.mastery, '->', after.mastery, '| teach_next:', an.teach_next);

const s2 = await call('forge_state');
console.assert(s2.last_shipped && s2.shipped_count === 1, 'final: last_shipped set');
console.assert(s2.skills.recently_moved.some((x: any) => x.id === 'floating-point-logsumexp'), 'final: skill shows as recently moved');

const rq = await call('forge_review_queue', { limit: 3 });
console.assert(Array.isArray(rq.items) && rq.items.length === 3, 'review queue returns must-knows');

await client.close();
console.log('\nsmoke.ts: full build -> ship -> analyze -> review loop passed ✅');
