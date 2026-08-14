// Phase 2 backfill: seed tracks, map every v1 skill and lesson onto a track, and record the
// 44 v1 builds in `systems` as kind 'study' with no metric, which is the truthful state.
//
// Everything here is idempotent and touches ONLY new tables and new columns. No pre-existing
// row is modified in any pre-existing column, and nothing is deleted.
//
//   tsx src/backfill.ts run      steps 1 to 4 (tracks, skills, lessons, systems)
//   tsx src/backfill.ts errors   step 5 (error taxonomy seed; run only after in-chat approval)
import Database from 'better-sqlite3';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB = join(HERE, '..', 'data', 'faiz.db');
const AS_OF = '2026-08-14';

// --- 1. Tracks (spec section 5) -------------------------------------------------------------

interface TrackSeed {
  code: string;
  title: string;
  position: number;
  prereqs: string[];
  completionTest: string;
}

export const TRACKS: TrackSeed[] = [
  { code: 'T0', title: 'Python and engineering for machine learning', position: 0, prereqs: [], completionTest: 'Create a new project, add a dependency, write a failing test, make it pass, profile the hot path, and push with green CI, in under fifteen minutes without looking anything up.' },
  { code: 'T1', title: 'PyTorch fluency', position: 1, prereqs: ['T0'], completionTest: 'Given a shape mismatch error you have never seen, diagnose it from the traceback without running anything.' },
  { code: 'T2', title: 'Train a real model, and learn how to know whether it worked', position: 2, prereqs: ['T1'], completionTest: 'Produce a results table with mean and spread over three seeds, a compute matched baseline, and an ablation.' },
  { code: 'T3', title: 'Modern architecture, as of 2026', position: 3, prereqs: ['T2'], completionTest: 'A results table showing what each architectural component was worth on your budget, with seed spread, and an honest statement of which differences were inside the noise.' },
  { code: 'T4', title: 'Kernels and the hardware', position: 4, prereqs: ['T3'], completionTest: 'A kernel you wrote that beats a reference on real hardware, with a roofline analysis that predicted the result before you measured it.' },
  { code: 'T5', title: 'Inference and serving', position: 5, prereqs: ['T3'], completionTest: 'A serving benchmark report with your own numbers, and a written prediction of what each configuration change would do made before running it.' },
  { code: 'T6', title: 'Post-training and RL', position: 6, prereqs: ['T3'], completionTest: 'A reward curve, an entropy curve, and a written account of a failure mode you caused on purpose and then fixed.' },
  { code: 'T7', title: 'Agents, harnesses and evaluation', position: 7, prereqs: ['T3'], completionTest: 'FaizOS v2 running, plus a scored run on a public agent benchmark.' },
  { code: 'T8', title: 'Multimodal and retrieval', position: 8, prereqs: ['T3'], completionTest: 'A retrieval system over your own corpus with measured recall at 50 and precision at 5, before and after reranking, and a small VLM fine tune.' },
  { code: 'T9', title: 'Safety, interpretability and evaluation as a discipline', position: 9, prereqs: ['T3'], completionTest: 'A trained SAE with an interpretable feature, and a gated tool harness demonstrating a blocked injection.' },
  { code: 'T10', title: 'Ship', position: 10, prereqs: ['T3'], completionTest: 'One published MCP server or desktop extension, and one product with a user who is not you.' },
];

// --- 2. Skill to track mapping (66 skills, approved in the plan) ---------------------------

export const SKILL_TRACK: Record<string, string> = {
  // M1
  'dev-setup': 'T0', 'floating-point-logsumexp': 'T1', 'linalg-matmul': 'T1',
  // M2
  'svd-lowrank': 'T3', 'matrix-calculus-vjp': 'T1', 'probability-covariance': 'T2', 'highdim-geometry': 'T3',
  // M3
  'python-craft': 'T0', 'data-structures': 'T0', 'roofline-cost-model': 'T4', 'profiling': 'T0',
  // M4
  'regression-from-scratch': 'T1', 'ml-lifecycle-leakage': 'T2', 'double-descent': 'T2', 'pca-svd': 'T3',
  // M5
  'autograd-backprop': 'T1', 'pytorch-basics': 'T1',
  // M6
  'optimization-adam': 'T2', 'init-normalization': 'T2', 'torch-compile': 'T4',
  // M7
  'attention': 'T3', 'rope': 'T3', 'rmsnorm': 'T3',
  // M8
  'swiglu': 'T3', 'gqa': 'T3', 'ssm-mamba': 'T3',
  // M9
  'nanogpt-llama-block': 'T3', 'kv-cache': 'T5', 'tokenizer-bpe': 'T2',
  // M10
  'scaling-laws': 'T2', 'mla': 'T3', 'heldout-eval': 'T2',
  // M11
  'gpu-memory-hierarchy': 'T4', 'triton-basics': 'T4', 'flash-attention': 'T4',
  // M12
  'torch-compile-cuda-graphs': 'T4', 'profiling-nsight': 'T4', 'parallelism-axes': 'T2',
  // M13
  'collectives-interconnect': 'T2', 'fsdp-run': 'T2', 'pipeline-schedules': 'T2', 'fault-tolerant-checkpointing': 'T2',
  // M14
  'peft-lora': 'T6', 'quantization': 'T5', 'inference-internals': 'T5', 'serving-stacks': 'T5',
  // M15
  'rl-foundations': 'T6', 'rlvr-grpo': 'T6', 'reward-modeling-verifiers': 'T6',
  // M16
  'reasoning-distillation': 'T6', 'rlhf-dpo': 'T6', 'tool-calling': 'T7',
  // M17
  'rag-production': 'T8', 'agent-memory': 'T7', 'agentic-rl': 'T7', 'agent-evals-tracing': 'T7',
  // M18
  'vit-clip-siglip': 'T8', 'diffusion-flow-matching': 'T8', 'vlm-fusion': 'T8',
  // M19
  'alignment-methods': 'T9', 'interpretability-sae': 'T9', 'ai-security': 'T9',
  // M20
  'research-method': 'T2', 'paper-reproduction': 'T2', 'oss-contribution': 'T10', 'capstone-portfolio': 'T10',
};

// --- 5. Error taxonomy seed (inserted only after in-chat approval) --------------------------

export interface ErrorSeed {
  category: string;
  description: string;
  rule_broken: string;
  occurrences: number;
}

export const ERROR_SEEDS: ErrorSeed[] = [
  { category: 'inverse-relationship', description: 'Duration and rate inverted, and exp/ln not treated as inverses. Cases: Amdahl speedup written as new_time * original; tokens per second answered with the step duration; exp(0.693) answered as 0.693.', rule_broken: 'A rate is one over a duration. If an improvement should make the number bigger, the time goes on the bottom. exp undoes ln.', occurrences: 3 },
  { category: 'expression-vs-statement', description: 'An assignment or English written where a bare expression belongs. Cases: residual = seq[i] + attn[i] inside a comprehension; return 2 trips; rm_score = drift * -beta inside a return.', rule_broken: 'return and append already receive the value. Write only the expression, no equals sign, no units.', occurrences: 3 },
  { category: 'missing-call-brackets', description: 'Bare function name where a call was needed. Cases: "all gather pieces" for all_gather(pieces); decode_step_ms without brackets where a value was needed.', rule_broken: 'A name refers to the function. Round brackets with its input actually run it.', occurrences: 2 },
  { category: 'api-misuse', description: 'Prose leaked into code as names or the wrong bracket kind was used. Cases: min written instead of lo; "original time" as a variable name; tools(arg, name) with round brackets on a dictionary.', rule_broken: 'Square brackets look up, round brackets call. Variable names come from the code, never from the sentence describing it.', occurrences: 3 },
  { category: 'ordering-pairing', description: 'The right set of values paired with the wrong sources. Cases: advantages listed 2, 0, -2 for rewards 5, 7, 9 (reversed); RoPE query rotated by j instead of its own position i.', rule_broken: 'Pair each value with its own source. Lowest reward takes the most negative advantage; the query uses its own position.', occurrences: 2 },
  { category: 'off-by-one', description: 'An implicit gained or released term missed, and small count slips. Cases: speculative decoding answered accepted instead of accepted + 1; GPipe peak doubled because backward was counted as storing rather than freeing; 8192/1024 answered as 7.', rule_broken: 'Ask which half of a paired operation consumes rather than adds before counting. Verify powers of two by doubling.', occurrences: 3 },
  { category: 'shape-mismatch', description: 'Stored count confused with produced shape. Case: LoRA B@A said to produce 8000 when it stores 2dr numbers but produces a d by d grid; the matmul inner-cancel rule needed re-deriving.', rule_broken: 'How many numbers you store and what shape they produce are different questions. Inner dimensions cancel.', occurrences: 1 },
  { category: 'silent-truncation', description: 'A fractional part dropped from an answer. Case: 50/4 reported as 12x rather than 12.5x.', rule_broken: 'Keep the fraction. Rounding away the decimal can hide the size of the result.', occurrences: 1 },
];

// --- runners --------------------------------------------------------------------------------

export function seedTracks(db: Database.Database): number {
  const insert = db.prepare(
    `INSERT INTO tracks (code, title, position, status, prereq_codes, completion_test, current_as_of)
     SELECT ?, ?, ?, 'pending', ?, ?, ?
     WHERE NOT EXISTS (SELECT 1 FROM tracks WHERE code = ?)`,
  );
  let added = 0;
  for (const t of TRACKS) {
    const r = insert.run(t.code, t.title, t.position, JSON.stringify(t.prereqs), t.completionTest, AS_OF, t.code);
    added += r.changes;
  }
  return added;
}

function trackIdByCode(db: Database.Database): Map<string, number> {
  const rows = db.prepare('SELECT id, code FROM tracks').all() as Array<{ id: number; code: string }>;
  return new Map(rows.map((r) => [r.code, r.id]));
}

export function mapSkillTracks(db: Database.Database): { mapped: number; unmappedSkillIds: string[]; danglingMappings: string[] } {
  const byCode = trackIdByCode(db);
  const skillRows = db.prepare('SELECT id FROM skills').all() as Array<{ id: string }>;
  const liveIds = new Set(skillRows.map((r) => r.id));
  const update = db.prepare('UPDATE skills SET track_id = ? WHERE id = ?');
  let mapped = 0;
  for (const [skillId, trackCode] of Object.entries(SKILL_TRACK)) {
    if (!liveIds.has(skillId)) continue;
    const trackId = byCode.get(trackCode);
    if (trackId === undefined) continue;
    update.run(trackId, skillId);
    mapped += 1;
  }
  const unmappedSkillIds = skillRows.map((r) => r.id).filter((id) => !(id in SKILL_TRACK));
  const danglingMappings = Object.keys(SKILL_TRACK).filter((id) => !liveIds.has(id));
  return { mapped, unmappedSkillIds, danglingMappings };
}

export function mapLessonTracks(db: Database.Database): { mapped: number; unmapped: number } {
  const byCode = trackIdByCode(db);
  const lessons = db.prepare('SELECT id, skills FROM lessons').all() as Array<{ id: number; skills: string }>;
  const update = db.prepare('UPDATE lessons SET track_id = ? WHERE id = ?');
  let mapped = 0;
  let unmapped = 0;
  for (const lesson of lessons) {
    let skillIds: string[] = [];
    try {
      const parsed: unknown = JSON.parse(lesson.skills || '[]');
      if (Array.isArray(parsed)) skillIds = parsed.filter((s): s is string => typeof s === 'string');
    } catch {
      skillIds = [];
    }
    const firstMapped = skillIds.find((s) => s in SKILL_TRACK);
    if (firstMapped === undefined) {
      unmapped += 1;
      continue;
    }
    const code = SKILL_TRACK[firstMapped];
    const trackId = code !== undefined ? byCode.get(code) : undefined;
    if (trackId === undefined) {
      unmapped += 1;
      continue;
    }
    update.run(trackId, lesson.id);
    mapped += 1;
  }
  return { mapped, unmapped };
}

export function backfillSystems(db: Database.Database): number {
  const existing = (db.prepare("SELECT COUNT(*) AS c FROM systems WHERE kind = 'study'").get() as { c: number }).c;
  if (existing > 0) return 0; // already backfilled; idempotent
  const missions = db
    .prepare('SELECT id, title, repo_path, status, created_at, shipped_at, ship_url FROM missions ORDER BY id')
    .all() as Array<{
    id: number;
    title: string;
    repo_path: string | null;
    status: string;
    created_at: string;
    shipped_at: string | null;
    ship_url: string | null;
  }>;
  const lessonTrack = db.prepare(
    'SELECT track_id FROM lessons WHERE mission_id = ? AND track_id IS NOT NULL LIMIT 1',
  );
  const insert = db.prepare(
    `INSERT INTO systems (track_id, title, repo_url, kind, status, metric_name, metric_value, baseline_value, deployed_url, created_at, shipped_at)
     VALUES (?, ?, ?, 'study', ?, NULL, NULL, NULL, NULL, ?, ?)`,
  );
  let added = 0;
  for (const m of missions) {
    const track = lessonTrack.get(m.id) as { track_id: number } | undefined;
    insert.run(track?.track_id ?? null, m.title, m.ship_url ?? m.repo_path, m.status, m.created_at, m.shipped_at);
    added += 1;
  }
  return added;
}

export function seedErrors(db: Database.Database): number {
  const insert = db.prepare(
    `INSERT INTO errors (lesson_id, category, description, code_excerpt, rule_broken, resolved, occurrences, last_seen)
     SELECT NULL, ?, ?, '', ?, 0, ?, ?
     WHERE NOT EXISTS (SELECT 1 FROM errors WHERE category = ? AND lesson_id IS NULL)`,
  );
  let added = 0;
  for (const e of ERROR_SEEDS) {
    const r = insert.run(e.category, e.description, e.rule_broken, e.occurrences, AS_OF, e.category);
    added += r.changes;
  }
  return added;
}

// --- CLI ------------------------------------------------------------------------------------

const invokedDirectly =
  process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href;
if (invokedDirectly) {
  const command = process.argv[2] ?? 'run';
  const flagIndex = process.argv.indexOf('--db');
  const dbPath =
    flagIndex !== -1 && process.argv[flagIndex + 1] ? (process.argv[flagIndex + 1] as string) : DEFAULT_DB;
  const db = new Database(dbPath, { fileMustExist: true });
  db.pragma('journal_mode = WAL');
  if (command === 'run') {
    const tracks = seedTracks(db);
    const skills = mapSkillTracks(db);
    const lessons = mapLessonTracks(db);
    const systems = backfillSystems(db);
    console.log(`tracks seeded:    ${tracks} added (11 total expected)`);
    console.log(`skills mapped:    ${skills.mapped}`);
    if (skills.unmappedSkillIds.length) console.log(`skills WITHOUT mapping: ${skills.unmappedSkillIds.join(', ')}`);
    if (skills.danglingMappings.length) console.log(`mappings WITHOUT skill: ${skills.danglingMappings.join(', ')}`);
    console.log(`lessons mapped:   ${lessons.mapped} (${lessons.unmapped} with no mappable skill stay NULL)`);
    console.log(`systems backfilled: ${systems} study rows`);
  } else if (command === 'errors') {
    const added = seedErrors(db);
    console.log(`error seeds inserted: ${added}`);
  } else {
    console.error(`unknown command: ${command} (use run | errors)`);
    process.exit(1);
  }
  db.close();
}
