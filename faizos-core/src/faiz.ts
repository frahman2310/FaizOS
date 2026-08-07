// Tiny CLI to call the real faizos-core brain from the shell (and for demos).
// Usage: tsx src/faiz.ts <tool> '<jsonArgs>'   e.g.  tsx src/faiz.ts faizos_state
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const [, , tool, argsJson] = process.argv;
if (!tool) { console.error('usage: tsx src/faiz.ts <tool> [jsonArgs]'); process.exit(1); }

const transport = new StdioClientTransport({
  command: join(HERE, '..', 'node_modules', '.bin', 'tsx'),
  args: [join(HERE, 'server.ts')],
  env: process.env as Record<string, string>, // FAIZOS_HOME unset -> real data dir
});
const client = new Client({ name: 'faiz-cli', version: '0.1.0' });
await client.connect(transport);
const r: any = await client.callTool({ name: tool, arguments: argsJson ? JSON.parse(argsJson) : {} });
console.log(r.content.map((c: any) => c.text).join('\n'));
await client.close();
