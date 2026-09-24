import time

BACKOFF = [0.5, 1.0, 0.0]
script = ["529 overloaded", "529 overloaded", "ok"]

def fake_provider(prompt):
    time.sleep(0.3)                    # every try takes 0.3 seconds
    outcome = script.pop(0)
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "reply to: " + prompt

def call(prompt, log):
    for wait in BACKOFF:
        start = time.time()
        try:
            text = fake_provider(prompt)
            ms = round((time.time() - start) * 1000, -2)
            log.append({"ok": True, "ms": ms})
            return text
        except RuntimeError:
            time.sleep(wait)

log = []
outside = time.time()                  # a second stopwatch, held by the user
call("summarise this invoice", log)
print("the user waited (ms):", round((time.time() - outside) * 1000, -2))
print("the log says:", log)
