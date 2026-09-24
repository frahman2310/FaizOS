LOG = [
    {"ok": True, "tries": 1},
    {"ok": False, "tries": 3},
    {"ok": True, "tries": 2},
]

def report(log):
    # goal: count the calls that worked
    oks = []
    for row in log:
        if row["ok"]:
            oks.append(row)
    return {"worked": len(oks)}

print(report(LOG))
