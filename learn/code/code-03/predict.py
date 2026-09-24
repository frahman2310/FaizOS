log = [{"ok": True, "cost": 0.0027}, {"ok": False, "cost": 0.0}, {"ok": True, "cost": 0.0027}]
passed = 0
for row in log:
    if row["ok"]:
        passed = passed + 1
print(passed)
print(log[1])
print(log[1]["cost"] + log[2])
