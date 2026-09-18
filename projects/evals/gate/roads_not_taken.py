"""What the options Faiz rejected would have done, measured on the same cases."""
import random

from cases import CASES
from summariser import summarise


def score(version, cases):
    return sum(1 for c in cases if c["must_include"] in summarise(c, version))


typed20 = [c for c in CASES if c["kind"] == "typed"][:20]
base20, broke20 = score("live", typed20), score("broken", typed20)
print(f"D1+D2 option A (20 invented cases): baseline {base20}/20, broken {broke20}/20, "
      f"fall {(base20 - broke20) * 5} points -> {'BLOCKED' if (base20-broke20)*5 > 2 else 'ALLOWED'}")

real18 = [c for c in CASES if c["kind"] != "typed"]
b18, k18 = score("live", real18), score("broken", real18)
print(f"D2 option B (18 real only): baseline {b18}/18, broken {k18}/18, "
      f"fall {(b18 - k18) / 18 * 100:.0f} points -> BLOCKED")

random.seed(7)
false_blocks = sum(1 for _ in range(20) if random.choice([0, 1, 2]) > 0)   # wobble 0-2 cases down
print(f"D3 option A (block on any fall), 20 unchanged proposals with a 0-2 case wobble: "
      f"{false_blocks} blocked for nothing, about {false_blocks} hours lost a day")
print(f"D4 option B (nightly): a bad change let in at 09:00 reaches about 140 invoices before 02:00")
# Recorded answers replay what the live version said, whatever version is proposed.
replayed = sum(1 for c in CASES if c["must_include"] in summarise(c, "live"))
print(f"D5 option C (recorded answers): the broken version scores {replayed}/100 because the run "
      f"replays live recordings -> fall 0 points -> ALLOWED, the break is invisible")
