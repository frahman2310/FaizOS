import time

BACKOFF = [0.5, 1.0, 0.0]                             # seconds to wait after try 1, 2, 3 fails
script = ["529 overloaded", "529 overloaded", "ok"]   # what the fake provider does on each try

def fake_provider(prompt):
    outcome = script.pop(0)              # take the first item out of the list
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "reply to: " + prompt

def call(prompt, log):
    attempts = 0                                          # (a)
    why = ""
    for wait in BACKOFF:
        attempts = attempts + 1                           # (b)
        try:
            text = fake_provider(prompt)                  # (c)
            log.append({"ok": True, "attempts": attempts})   # (d)
            return text
        except RuntimeError as err:
            why = str(err)                                # (e)
            time.sleep(wait)                              # (f)
    log.append({"ok": False, "attempts": attempts, "why": why})
    return None

log = []
print(call("summarise this invoice", log))
print(log)
