LOG = [
    {"ok": True,  "attempts": 1, "cost": 0.0027},
    {"ok": True,  "attempts": 3, "cost": 0.0027},
    {"ok": False, "attempts": 3, "cost": 0.0},
    {"ok": True,  "attempts": 2, "cost": 0.0027},
]

def report(log):
    oks = []                                       # (a)
    for row in log:
        if row["ok"]:
            oks.append(row)                        # (b)
    retried = 0                                    # (c)
    for row in oks:
        if row["attempts"] > 1:
            retried = retried + 1                  # (d)
    spend = 0.0
    for row in log:
        spend = spend + row["cost"]                # (e)
    return {"succeeded": len(oks), "retried": retried,
            "cost per success": round(spend / len(oks), 4)}

print(report(LOG))
