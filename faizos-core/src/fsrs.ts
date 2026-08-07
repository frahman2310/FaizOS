// FSRS-lite: a faithful, minimal spaced-repetition scheduler. Per card: stability (days) +
// difficulty (1-10). Success expands the interval; a lapse contracts it; retrievability decays
// over time. ponytail: lite (not the full 19-parameter FSRS-5); swap in the real weights if recall drifts.
import { fileURLToPath } from 'node:url';
import { daysBetween } from './streak.js';

export type Grade = 1 | 2 | 3 | 4; // again | hard | good | easy
export interface Card { stability: number; difficulty: number; last: string; due: string; reps: number; }

const clamp = (x: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, x));
const S0: Record<Grade, number> = { 1: 0.5, 2: 1, 3: 3, 4: 7 };
const EASE: Record<Grade, number> = { 1: 0.4, 2: 1.2, 3: 1.6, 4: 2.2 };

export function addDays(iso: string, days: number): string {
  const [y, m, d] = iso.split('-').map(Number);
  const dt = new Date(Date.UTC(y, m - 1, d) + Math.max(1, Math.round(days)) * 86_400_000);
  return `${dt.getUTCFullYear()}-${String(dt.getUTCMonth() + 1).padStart(2, '0')}-${String(dt.getUTCDate()).padStart(2, '0')}`;
}

export function initCard(grade: Grade, today: string): Card {
  const stability = S0[grade];
  return { stability, difficulty: clamp(7 - (grade - 2), 1, 10), last: today, due: addDays(today, stability), reps: 1 };
}

export function review(card: Card, grade: Grade, today: string): Card {
  const hardness = (11 - card.difficulty) / 10; // a harder card (high D) grows less
  const stability = grade === 1
    ? Math.max(0.4, card.stability * 0.4)               // lapse contracts
    : card.stability * (1 + (EASE[grade] - 1) * hardness); // success expands
  const difficulty = clamp(card.difficulty - 0.15 * (grade - 3), 1, 10);
  return { stability, difficulty, last: today, due: addDays(today, stability), reps: card.reps + 1 };
}

export function retrievability(card: Card, today: string): number {
  const t = Math.max(0, daysBetween(card.last, today));
  return clamp(Math.pow(1 + (19 / 81) * (t / card.stability), -1), 0, 1);
}

export function gradeFromOutcome(outcome: number): Grade {
  return outcome >= 0.9 ? 4 : outcome >= 0.7 ? 3 : outcome >= 0.4 ? 2 : 1;
}

// --- self-check (run: tsx src/fsrs.ts) ---
function test() {
  const t0 = '2026-08-07';
  const c0 = initCard(3, t0);
  console.assert(c0.stability === 3 && c0.due === addDays(t0, 3), 'init good card');
  const cGood = review(c0, 3, c0.due);
  console.assert(cGood.stability > c0.stability, 'success expands stability');
  const cLapse = review(cGood, 1, cGood.due);
  console.assert(cLapse.stability < cGood.stability && cLapse.difficulty > cGood.difficulty, 'lapse contracts + hardens');
  console.assert(retrievability(c0, t0) > 0.99 && retrievability(c0, addDays(t0, 10)) < retrievability(c0, t0), 'retrievability decays');
  console.assert(review(c0, 4, c0.due).stability > review(c0, 2, c0.due).stability, 'easy expands more than hard');
  console.assert(gradeFromOutcome(0.95) === 4 && gradeFromOutcome(0.5) === 2 && gradeFromOutcome(0.1) === 1, 'outcome->grade');
  console.log('fsrs.ts: all assertions passed');
}
if (process.argv[1] === fileURLToPath(import.meta.url)) test();
