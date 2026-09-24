log = [{"ok": True, "cost": 0.0027}, {"ok": False, "cost": 0.0}, {"ok": True, "cost": 0.0027}]

def spend(log):
    total = 0.0
    for row in log:
        total = total + row
    return total

print(spend(log))
