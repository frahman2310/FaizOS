calls = [{"ok": False, "tries": 2}, {"ok": True, "tries": 1}]
retried = 0
for c in calls:
    if c["tries"] > 1:
        retried = retried + 1
print(retried)
