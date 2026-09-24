calls = [{"ok": True, "ms": 120}, {"ok": False, "ms": 900}, {"ok": True, "ms": 300}]
good = []
for c in calls:
    if c["ok"]:
        good.append(c)
slowest = 0
for c in calls:
    if c["ms"] > slowest:
        slowest = c["ms"]
print("slowest good call:", slowest)
