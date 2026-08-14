// Frontier ingest. Same split as the venture arm: this file only fetches and seeds
// (deterministic); classification and summarisation happen in session through the tools.
//
//   tsx src/frontier.ts seed  [--db <path>]    one row per spec section 6 subsection
//   tsx src/frontier.ts fetch [--db <path>]    weekly arXiv pull for current + next track
import Database from 'better-sqlite3';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { realFetch, type FetchLike } from './venture.js';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB = join(HERE, '..', 'data', 'faiz.db');
const now = (): string => new Date().toISOString();

// ---- seeds: spec section 6, one row per subsection -----------------------------------------

export const FRONTIER_SEEDS: Array<{ area: string; title: string; url: string; summary: string; track_code: string | null }> = [
  {
    area: '6.1', track_code: 'T3', url: 'https://huggingface.co/models',
    title: 'The attention consensus collapsed',
    summary: 'The GQA/MLA monoculture is gone. Qwen3.5 runs Gated DeltaNet linear attention 3:1, Kimi K3 runs KDA plus Gated MLA, GLM-5 layers DeepSeek Sparse Attention on MLA, MiniMax M2.5 deliberately runs full MHA, Gemma 4 runs sliding window plus global, Nemotron 3 runs Mamba-2 with attention anchors. RoPE, GQA and MLA builds stay correct as the baseline the variations are measured against.',
  },
  {
    area: '6.2', track_code: 'T3', url: 'https://huggingface.co/models',
    title: 'MoE went extremely sparse',
    summary: 'Active fractions of 3 to 5 percent (DeepSeek V4-Pro 3.1, Kimi K3 3.7, Qwen3.5 4.3). Expert counts to 896 with top-16. LatentMoE appeared at Moonshot and NVIDIA independently: routing and compute in a reduced latent dimension. Consumer consequence: a 35B-A3B MoE at 4 bit beats a 27B dense at 4 bit on memory and speed.',
  },
  {
    area: '6.3', track_code: 'T5', url: 'https://arxiv.org/list/cs.LG/recent',
    title: 'Precision fell to four bits in production',
    summary: 'FP8 is the floor. FP4 shipped: DeepSeek V4 FP4 experts, Kimi K3 MXFP4 weights via QAT, Nemotron 3 trained in NVFP4. Decision rule on Blackwell: NVFP4 for weights at 30B and above, MXFP4 where the checkpoint ships it, FP8 elsewhere. NVFP4 recovery improves with scale, 99 percent at 70B but 95 to 98 at 7 to 14B.',
  },
  {
    area: '6.4', track_code: 'T2', url: 'https://github.com/KellerJordan/modded-nanogpt',
    title: 'Muon is confirmed at frontier scale',
    summary: 'DeepSeek V4 discloses Muon in production, the first frontier scale disclosure. No evidence of Shampoo, SOAP or true second order methods in production runs. modded-nanogpt already uses it; it lands in T2 as a working component.',
  },
  {
    area: '6.5', track_code: 'T3', url: 'https://arxiv.org/list/cs.LG/recent',
    title: 'Residual stream engineering became a thing',
    summary: 'Manifold constrained hyper-connections restore the identity mapping that plain hyper-connections break, shipped in DeepSeek V4. Kimi K3 Attention Residuals is a parallel thread. Direct descendant of the residual lesson: 30 blocks gave RMS 27.7 with residuals versus 0.07 without.',
  },
  {
    area: '6.6', track_code: 'T6', url: 'https://arxiv.org/list/cs.LG/recent',
    title: 'Post-training moved past plain GRPO',
    summary: 'The 2026 default is a GRPO family recipe: clip-higher, dynamic sampling, sequence level or reshaped importance ratio, off policy. DAPO, GSPO, CISPO, VESPO are shipped loss types. ScaleRL: RL compute curves are sigmoidal, recipe choices split into asymptote movers and efficiency movers. Length bias impossibility: no weighting is both gradient unbiased and length invariant.',
  },
  {
    area: '6.7', track_code: 'T5', url: 'https://docs.vllm.ai',
    title: 'Inference: the interesting layer moved above the engine',
    summary: 'Prefix caching is default on; the work moved to tiered KV storage and disaggregated prefill/decode (RDMA required for production). Decode context parallelism: 6091 tok/s/GPU at 512 concurrency on MLA models. Speculative decoding moved to parallel drafting (P-EAGLE, DFlash); MTP heads ship in weights so speculation needs no drafter.',
  },
  {
    area: '6.8', track_code: 'T4', url: 'https://arxiv.org/abs/2501.01005',
    title: 'Kernels: bottleneck moved off matmul, Python became competitive',
    summary: 'FlashAttention 4 is the reference text: Blackwell scales tensor cores but not the other units, so softmax and exponentials become the bottleneck. Written in CuTe DSL in Python, 20 to 30x faster compiles. With Inductor CuTe backend and Helion, C++ templates are no longer the entry fee for state of the art kernels. That fact makes T4 feasible.',
  },
  {
    area: '6.9', track_code: 'T7', url: 'https://os-world.github.io',
    title: 'Agents: the verification gap and the context ceiling',
    summary: 'Marginal test time compute is better spent on a better verifier or selector than on more samples or longer traces. OSWorld 2.0: best model 20.6 percent on long horizon computer use. ARC-AGI-3: frontier models at 0.5 percent where humans hit 100. Computer use and novel interactive environments are the open research ground.',
  },
  {
    area: '6.10', track_code: null, url: 'https://huggingface.co/google/gemma-4-27b-it',
    title: 'Who publishes: the open weight frontier is Chinese plus Gemma',
    summary: 'Study DeepSeek, Qwen, Moonshot, Z.ai, MiniMax, Mistral, NVIDIA and Gemma (unusually detailed model card). Anthropic, OpenAI, Gemini and xAI disclose zero architecture, so architectural claims about closed models are not primary sourced. Do not build a mental model of the frontier from speculation.',
  },
];

export function seedFrontier(db: Database.Database): number {
  const insert = db.prepare(
    `INSERT INTO frontier (area, title, url, summary, affects_track_id, ingested_at, actioned)
     SELECT ?, ?, ?, ?, ?, ?, 0
     WHERE NOT EXISTS (SELECT 1 FROM frontier WHERE area = ? AND title = ?)`,
  );
  const trackId = db.prepare('SELECT id FROM tracks WHERE code = ?');
  let created = 0;
  for (const s of FRONTIER_SEEDS) {
    const t = s.track_code ? (trackId.get(s.track_code) as { id: number } | undefined) : undefined;
    created += insert.run(s.area, s.title, s.url, s.summary, t?.id ?? null, now(), s.area, s.title).changes;
  }
  return created;
}

// ---- weekly fetch: arXiv only, for the current and next track ------------------------------
// Lab blogs have no stable free API; arXiv covers the research half deterministically and the
// session model fills the rest when it classifies. Fetch stores raw rows, nothing more.

export const TRACK_QUERIES: Record<string, string> = {
  T0: 'cat:cs.SE AND abs:"developer tooling"',
  T1: 'cat:cs.LG AND abs:"automatic differentiation"',
  T2: 'cat:cs.LG AND abs:"scaling laws" AND abs:"language model"',
  T3: 'cat:cs.CL AND abs:"attention" AND abs:"architecture"',
  T4: 'cat:cs.DC AND abs:"GPU kernel"',
  T5: 'cat:cs.LG AND abs:"LLM inference"',
  T6: 'cat:cs.LG AND abs:"reinforcement learning" AND abs:"language model"',
  T7: 'cat:cs.AI AND abs:"LLM agent"',
  T8: 'cat:cs.CV AND abs:"vision language model"',
  T9: 'cat:cs.LG AND abs:"interpretability"',
  T10: 'cat:cs.SE AND abs:"open source" AND abs:"machine learning"',
};

const ENTRY_RE = /<entry>[\s\S]*?<id>([^<]+)<\/id>[\s\S]*?<title>([\s\S]*?)<\/title>[\s\S]*?<summary>([\s\S]*?)<\/summary>[\s\S]*?<\/entry>/g;
const clip = (t: string, n = 400): string => t.replace(/\s+/g, ' ').trim().slice(0, n);
const sleep = (ms: number): Promise<void> => new Promise((r) => setTimeout(r, ms));
const UA = { 'User-Agent': 'FaizOS-frontier faiz.rahman.research@proton.me' };

// arXiv throttles hard and intermittently (429/503 even on the first request). One polite
// retry; a still-failing source is reported, never fatal, and the weekly cron tries again.
async function fetchArxivXml(fetchImpl: FetchLike, url: string, retryDelayMs: number): Promise<string> {
  let res = await fetchImpl(url, { headers: UA });
  if ((res.status === 429 || res.status === 503) && retryDelayMs > 0) {
    await sleep(retryDelayMs);
    res = await fetchImpl(url, { headers: UA });
  }
  if (!res.ok) throw new Error(`arxiv -> ${res.status}`);
  return res.text();
}

export async function fetchFrontier(
  db: Database.Database,
  fetchImpl: FetchLike,
  delayMs = 1100,
): Promise<{ inserted: number; perTrack: Record<string, number>; failures: Record<string, string> }> {
  // Current track plus the next one by position; frontier for tracks far ahead is noise.
  const targets = db
    .prepare(
      `SELECT id, code FROM tracks WHERE status IN ('active', 'pending') ORDER BY (status = 'active') DESC, position LIMIT 2`,
    )
    .all() as Array<{ id: number; code: string }>;
  const insert = db.prepare(
    `INSERT INTO frontier (area, title, url, summary, affects_track_id, ingested_at, actioned)
     SELECT 'weekly', ?, ?, ?, ?, ?, 0
     WHERE NOT EXISTS (SELECT 1 FROM frontier WHERE url = ? AND title = ?)`,
  );
  const perTrack: Record<string, number> = {};
  const failures: Record<string, string> = {};
  let inserted = 0;
  for (const t of targets) {
    const q = TRACK_QUERIES[t.code];
    if (!q) continue;
    try {
      const xml = await fetchArxivXml(
        fetchImpl,
        `https://export.arxiv.org/api/query?search_query=${encodeURIComponent(q)}&sortBy=submittedDate&sortOrder=descending&max_results=5`,
        delayMs > 0 ? 5000 : 0,
      );
      let count = 0;
      for (const m of xml.matchAll(ENTRY_RE)) {
        const url = (m[1] ?? '').trim();
        const title = clip(m[2] ?? '', 200);
        const summary = clip(m[3] ?? '');
        count += insert.run(title, url, summary, t.id, now(), url, title).changes;
      }
      perTrack[t.code] = count;
      inserted += count;
    } catch (e) {
      failures[t.code] = e instanceof Error ? e.message : String(e);
    }
    if (delayMs > 0) await sleep(delayMs);
  }
  return { inserted, perTrack, failures };
}

export function driftedTracks(db: Database.Database): Array<{ code: string; title: string; days: number }> {
  const rows = db.prepare('SELECT code, title, current_as_of FROM tracks ORDER BY position').all() as Array<{
    code: string;
    title: string;
    current_as_of: string | null;
  }>;
  const today = Date.now();
  const out: Array<{ code: string; title: string; days: number }> = [];
  for (const r of rows) {
    if (!r.current_as_of) continue;
    const days = Math.floor((today - new Date(r.current_as_of).getTime()) / 86400000);
    if (days > 60) out.push({ code: r.code, title: r.title, days });
  }
  return out;
}

// ---- CLI -----------------------------------------------------------------------------------

const invokedDirectly = process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  const command = process.argv[2] ?? 'fetch';
  const flag = process.argv.indexOf('--db');
  const dbPath = flag !== -1 && process.argv[flag + 1] ? (process.argv[flag + 1] as string) : DEFAULT_DB;
  const db = new Database(dbPath, { fileMustExist: true });
  db.pragma('journal_mode = WAL');
  if (command === 'seed') {
    console.log(`seeded ${seedFrontier(db)} frontier rows from spec section 6`);
    db.close();
  } else if (command === 'fetch') {
    fetchFrontier(db, realFetch)
      .then((r) => {
        console.log(`fetched ${r.inserted} new frontier rows`);
        for (const [code, cnt] of Object.entries(r.perTrack)) console.log(`  ${code}: ${cnt}`);
        for (const [code, err] of Object.entries(r.failures)) console.log(`  ${code} FAILED: ${err}`);
        db.close();
      })
      .catch((e) => {
        console.error(e);
        db.close();
        process.exit(1);
      });
  } else {
    console.error(`unknown command: ${command} (use seed | fetch)`);
    db.close();
    process.exit(1);
  }
}
