"""The judge, built to Faiz's four decisions (lesson 6). A modelled world: no real AI calls, fixed seed.

  1 label 200 random notes + 200 from the complaints table     2 two rules: the total, and the due date
  3 strong AI on 800 random notes (the rest unmarked; changed from 'cheap AI on the rest' after the first run)  4 block a change only on a fall bigger than the wobble
"""
import math
import random
import sqlite3

random.seed(6)
WEEK = 4000
TYPED_FAIL = 0.0622                  # scans fail 3x as often; with 1 in 7 notes a scan, 8% of notes are bad
DUE_DATE_FAIL = 0.005                # a kind nobody complains about (fixed before the run, never counted in Round 1)
STRONG, CHEAP = 0.003, 0.0004        # $ per call
CATCH = {"strong": {"typed": 0.93, "scan": 0.93}, "cheap": {"typed": 0.93, "scan": 0.50}}
FALSE_ALARM_PER_RULE = 0.02
RULES = 2                            # decision 2


def week(scan_share):
    notes = []
    for i in range(WEEK):
        scan = random.random() < scan_share
        kind = None
        if random.random() < TYPED_FAIL * (3 if scan else 1):
            kind = "total"
        elif random.random() < DUE_DATE_FAIL:
            kind = "due_date"
        notes.append({"id": i, "scan": scan, "bad": kind})
    return notes


def judge(note, ai):
    if note["bad"]:
        return "FAIL" if random.random() < CATCH[ai]["scan" if note["scan"] else "typed"] else "PASS"
    alarms = sum(random.random() < FALSE_ALARM_PER_RULE for _ in range(RULES))
    return "FAIL" if alarms else "PASS"


def rate(hits, n):
    p = hits / n
    return p, 2 * math.sqrt(p * (1 - p) / n)


notes = week(1 / 7)

# Decision 1: pick the labels. The complaints table holds bad notes about the total (nobody complains about due dates).
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE complaints (id INTEGER)")
db.executemany("INSERT INTO complaints VALUES (?)", [(n["id"],) for n in notes if n["bad"] == "total"][:320])
from_complaints = {r[0] for r in db.execute("SELECT id FROM complaints ORDER BY RANDOM() LIMIT 200")}
rest = [n for n in notes if n["id"] not in from_complaints]
labelled = random.sample(rest, 200) + [notes[i] for i in from_complaints]

print(f"\n  hand labels        {len(labelled)} notes, {len(labelled) * 40 / 3600:.1f} hours")
for ai in ("strong", "cheap"):
    bad = [n for n in labelled if n["bad"]]
    good = [n for n in labelled if not n["bad"]]
    c, cw = rate(sum(judge(n, ai) == "FAIL" for n in bad), len(bad))
    k, kw = rate(sum(judge(n, ai) == "PASS" for n in good), len(good))
    print(f"  {ai:6} judge       catch {c:.0%} (wobble {cw * 100:.0f} pts, {len(bad)} bad)   clear {k:.0%} (wobble {kw * 100:.0f} pts, {len(good)} good)")
print(f"  due-date failures  {sum(n['bad'] == 'due_date' for n in labelled)} among the labels")

# Decision 3: weekly judging.
random.shuffle(notes)
strong_part, cheap_part = notes[:800], []          # decision 3, plain C
cost = len(strong_part) * RULES * STRONG + len(cheap_part) * RULES * CHEAP
missed = sum(1 for n in cheap_part if n["bad"] and judge(n, "cheap") == "PASS")
print(f"  weekly cost        ${cost:.2f}  (strong ${len(strong_part) * RULES * STRONG:.2f} + cheap ${len(cheap_part) * RULES * CHEAP:.2f}), target under $5")
print(f"  unmarked notes     {len(notes) - len(strong_part)}, holding {sum(1 for n in notes[800:] if n['bad'])} bad ones nobody looks at")


# Decision 4: a harmless change, gated by rule B, 1,000 times.
def weekly_pass(scan_share):
    return sum(judge(n, "strong") == "PASS" for n in random.sample(week(scan_share), 800)) / 800


def blocked(before, after, wobble=0.02):
    return before - after > wobble


mid = sum(blocked(weekly_pass(1 / 7), weekly_pass(1 / 7)) for _ in range(200)) / 200
end = sum(blocked(weekly_pass(1 / 7), weekly_pass(1 / 3)) for _ in range(200)) / 200
print(f"  harmless change    blocked {mid:.0%} of the time mid-month, {end:.0%} at month end")
