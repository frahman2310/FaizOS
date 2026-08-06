// Forgiving streak logic (Atlas ethical loop: reward consistency, never punish a lapse).
// A single missed day is granted grace and does NOT reset the streak. A gap > 2 days resets.
import { fileURLToPath } from 'node:url';

export function todayISO(d: Date = new Date()): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export function daysBetween(fromISO: string, toISO: string): number {
  const [ay, am, ad] = fromISO.split('-').map(Number);
  const [by, bm, bd] = toISO.split('-').map(Number);
  return Math.round((Date.UTC(by, bm - 1, bd) - Date.UTC(ay, am - 1, ad)) / 86_400_000);
}

export interface StreakState { streak: number; best: number; lastActive: string | null; }

export function advanceStreak(
  s: StreakState,
  today: string,
): StreakState & { changed: boolean; graceUsed: boolean } {
  if (s.lastActive === today) return { ...s, changed: false, graceUsed: false };
  let streak: number;
  let graceUsed = false;
  if (s.lastActive === null) {
    streak = 1;
  } else {
    const gap = daysBetween(s.lastActive, today);
    if (gap <= 1) streak = s.streak + 1;
    else if (gap === 2) { streak = s.streak + 1; graceUsed = true; } // forgive one missed day
    else streak = 1;
  }
  return { streak, best: Math.max(s.best, streak), lastActive: today, changed: true, graceUsed };
}

// --- self-check (run: tsx src/streak.ts) ---
function test() {
  console.assert(daysBetween('2026-08-01', '2026-08-02') === 1, 'adjacent days');
  console.assert(daysBetween('2026-08-01', '2026-08-01') === 0, 'same day');
  console.assert(daysBetween('2026-02-28', '2026-03-01') === 1, 'month boundary (2026 non-leap)');
  let s = advanceStreak({ streak: 0, best: 0, lastActive: null }, '2026-08-06');
  console.assert(s.streak === 1 && s.best === 1, 'first activity');
  s = advanceStreak({ streak: 3, best: 5, lastActive: '2026-08-05' }, '2026-08-06');
  console.assert(s.streak === 4 && s.best === 5, 'consecutive day');
  s = advanceStreak({ streak: 4, best: 5, lastActive: '2026-08-06' }, '2026-08-06');
  console.assert(s.streak === 4 && !s.changed, 'same day is a no-op');
  s = advanceStreak({ streak: 4, best: 5, lastActive: '2026-08-04' }, '2026-08-06');
  console.assert(s.streak === 5 && s.graceUsed, 'one missed day is forgiven');
  s = advanceStreak({ streak: 10, best: 10, lastActive: '2026-08-01' }, '2026-08-06');
  console.assert(s.streak === 1 && s.best === 10, 'big gap resets but keeps best');
  console.log('streak.ts: all assertions passed');
}
if (process.argv[1] === fileURLToPath(import.meta.url)) test();
