"""The gate, built to Faiz's five decisions (lesson 5).

  1 100 cases                         2 18 real complaints + 82 invented
  3 block only on a fall of MORE than 2 points     4 runs on instruction changes, nightly otherwise
  5 a short-lived pass, never a stored password    (see evals.yml.example)
"""
import sys

from cases import CASES
from summariser import summarise

TOLERANCE = 2          # decision 3
PRICE_PER_CALL = 0.0027


def score(version):
    passed = 0
    failing = []
    for case in CASES:
        if case["must_include"] in summarise(case, version):
            passed = passed + 1
        else:
            failing.append(case["invoice"])
    return passed, failing


def gate(proposed):
    base, _ = score("live")
    new, new_failing = score(proposed)
    fall = base - new
    blocked = fall > TOLERANCE
    print(f"\n  proposed version   {proposed}")
    print(f"  baseline           {base} of {len(CASES)}  ({base / len(CASES) * 100:.0f}%)")
    print(f"  proposed           {new} of {len(CASES)}  ({new / len(CASES) * 100:.0f}%)")
    print(f"  change             {new - base:+d} points, tolerance {TOLERANCE}")
    print(f"  cost of this run   ${len(CASES) * 2 * PRICE_PER_CALL:.2f}  ({len(CASES) * 2} AI calls, modelled)")
    print(f"  VERDICT            {'BLOCKED' if blocked else 'ALLOWED'}")
    if blocked:
        newly = [i for i in new_failing if i not in score('live')[1]]
        print(f"  newly failing      {len(newly)}: {', '.join(newly[:6])}")
    return 1 if blocked else 0


if __name__ == "__main__":
    sys.exit(max(gate(v) for v in (sys.argv[1:] or ["broken", "better"])))
