calls = [{"ok": True, "tries": 3}, {"ok": False, "tries": 2}, {"ok": False, "tries": 4}]
retried = 0
for c in calls:
    if c["tries"] > 1:
        retried = retried + 1
print(retried)
