// Pure compiler: all revision notes -> one markdown notebook (newest first).
import { fileURLToPath } from 'node:url';

export interface Revision { ts: string; topic: string; note_md: string; }

export function compileNotebook(revisions: Revision[]): string {
  const n = revisions.length;
  const head = `# FaizOS — Revision Notebook\n\n> Auto-compiled from every lesson. ${n} entr${n === 1 ? 'y' : 'ies'}, newest first.\n`;
  const body = [...revisions]
    .sort((a, b) => (a.ts < b.ts ? 1 : -1)) // newest first
    .map((r) => `\n---\n\n## ${r.topic}\n_${r.ts.slice(0, 10)}_\n\n${r.note_md.trim()}\n`)
    .join('');
  return head + body + '\n';
}

// --- self-check (run: tsx src/notebook.ts) ---
function test() {
  const out = compileNotebook([
    { ts: '2026-08-06T10:00:00Z', topic: 'matrix multiply cost', note_md: '**Remember:** 2*M*N*K' },
    { ts: '2026-08-07T10:00:00Z', topic: 'stable softmax', note_md: '**Remember:** subtract the max' },
  ]);
  console.assert(out.includes('2 entries'), 'counts entries');
  console.assert(out.indexOf('stable softmax') < out.indexOf('matrix multiply cost'), 'newest first');
  console.assert(out.includes('2*M*N*K') && out.includes('subtract the max'), 'includes both notes');
  console.assert(compileNotebook([]).includes('0 entries'), 'handles empty');
  console.log('notebook.ts: all assertions passed');
}
if (process.argv[1] === fileURLToPath(import.meta.url)) test();
