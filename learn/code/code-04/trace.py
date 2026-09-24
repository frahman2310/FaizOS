LOG = [
    {"ok": True, "tries": 1},
    {"ok": False, "tries": 3},
    {"ok": True, "tries": 2},
]

def report(log):
    # goal: sum up a log: how many calls worked, and how many of those needed a retry
    # 1. keep the calls that worked
    oks = []                                   # (a)
    for row in log:
        if row["ok"]:
            oks.append(row)                    # (b)
    # 2. count the ones that needed more than one try
    retried = 0                                # (c)
    for row in oks:
        if row["tries"] > 1:
            retried = retried + 1              # (d)
    # 3. hand back the summary
    return {"worked": len(oks), "retried": retried}

print(report(LOG))
