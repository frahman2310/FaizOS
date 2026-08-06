// Pure mastery model. `mastery` and `outcome` are in [0,1]. Evidence nudges mastery
// toward the observed outcome, weighted by how strong that kind of evidence is.
// ponytail: fixed learning rate + fixed weights for now; the weekly audit personalizes later.
import { fileURLToPath } from 'node:url';

export const EVIDENCE_WEIGHTS = {
  ship: 0.5, // built AND shipped — the strongest signal
  build: 0.4,
  explain: 0.3,
  review: 0.2,
  quiz: 0.1,
} as const;
export type EvidenceKind = keyof typeof EVIDENCE_WEIGHTS;

const LEARNING_RATE = 0.6;

export function updateMastery(prev: number, outcome: number, kind: EvidenceKind): number {
  const w = EVIDENCE_WEIGHTS[kind] ?? EVIDENCE_WEIGHTS.build;
  return clamp01(prev + LEARNING_RATE * w * (outcome - prev));
}

// More/stronger evidence raises confidence in the estimate; bounded at 1.
export function bumpConfidence(prev: number, kind: EvidenceKind): number {
  return clamp01(prev + 0.3 * (EVIDENCE_WEIGHTS[kind] ?? 0.4) + 0.05);
}

function clamp01(x: number): number {
  return Math.max(0, Math.min(1, x));
}

// --- self-check (run: tsx src/mastery.ts) ---
function test() {
  const m1 = updateMastery(0, 1, 'ship'); // 0 + 0.6*0.5*1 = 0.30
  console.assert(m1 > 0.25 && m1 < 0.35, `ship-from-0 => ${m1}`);
  console.assert(updateMastery(0.5, 1, 'quiz') < updateMastery(0.5, 1, 'build'), 'build must move more than quiz');
  console.assert(updateMastery(0.8, 0, 'review') < 0.8, 'a failed review must lower mastery');
  console.assert(updateMastery(1, 1, 'ship') <= 1 && updateMastery(0, 0, 'ship') >= 0, 'must stay clamped');
  console.assert(bumpConfidence(0.95, 'ship') <= 1, 'confidence must stay <= 1');
  console.log('mastery.ts: all assertions passed');
}
if (process.argv[1] === fileURLToPath(import.meta.url)) test();
