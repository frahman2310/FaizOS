LOG = [
    {"ok": True, "tries": 1},
    {"ok": False, "tries": 3},
    {"ok": True, "tries": 2},
]

def report(log):
    oks = []
    for row in log:
        if row["ok"]:
            oks.append(row)
    retried = 0
    for row in log:
        if row["tries"] > 1:
            retried = retried + 1
    return {"worked": len(oks), "retried": retried}

print(report(LOG))
