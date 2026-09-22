"""The options Faiz did not pick, run in the same modelled world."""
import contextlib
import io
import random

with contextlib.redirect_stdout(io.StringIO()):
    import judge_build as jb

random.seed(7)
notes = jb.week(1 / 7)

# D1 B: 400 random notes instead of 200 random + 200 complaints.
lab = random.sample(notes, 400)
bad = [n for n in lab if n["bad"]]
c, cw = jb.rate(sum(jb.judge(n, "strong") == "FAIL" for n in bad), len(bad))
print(f"  D1 B 400 random         catch {c:.0%} wobble {cw * 100:.0f} pts on {len(bad)} bad notes")

# D2 B: one rule (total only). Clear rate rises, due-date failures are never caught.
jb.RULES = 1
good = [n for n in lab if not n["bad"]]
k, _ = jb.rate(sum(jb.judge(n, "strong") == "PASS" for n in good), len(good))
due = sum(n["bad"] == "due_date" for n in notes)
print(f"  D2 B one rule           clear {k:.0%}; misses all {due} due-date failures a week; strong-800 cost ${800 * 0.003:.2f}")
jb.RULES = 2

# D3 C unmodified: strong AI on 800 only.
print(f"  D3 C strong-800 only    ${800 * 2 * jb.STRONG:.2f} a week, 3,200 notes never marked")


# D4 C: old and new versions on the same 400 labelled emails; a harmless change only flips on judge noise.
def paired_blocked():
    flips = sum((jb.judge(n, "strong") == "PASS") - (jb.judge(n, "strong") == "PASS") for n in lab)
    return flips / 400 > 0.02


print(f"  D4 C same 400 emails    harmless change blocked {sum(paired_blocked() for _ in range(200)) / 200:.0%} of the time, "
      f"month end or not; $4.80 per change")
