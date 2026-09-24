import time

BACKOFF = [0.5, 1.0, 0.0]
script = ["529 overloaded", "529 overloaded", "ok"]

def fake_provider(prompt):
    outcome = script.pop(0)
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "reply to: " + prompt

def call(prompt, log):
    attempts = 0
    why = ""
    for wait in BACKOFF:
        attempts = attempts + 1
        try:
            text = fake_provider(prompt)
            log.append({"ok": True, "attempts": attempts})
            return text
        except RuntimeError as err:
            why = str(err)
            time.sleep(wait)
        log.append({"ok": False, "attempts": attempts, "why": why})
    return None

log = []
call("summarise this invoice", log)
print("calls made:", 1)
print("records in log:", len(log))
print("records saying failed:", len([row for row in log if not row["ok"]]))
