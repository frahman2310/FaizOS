import time

PAUSES = [0.1, 0.1, 0.0]
answers = ["busy", "ok"]

def fake_provider(q):
    time.sleep(0.1)                    # every try takes 0.1 seconds
    a = answers.pop(0)
    if a != "ok":
        raise RuntimeError(a)
    return "answer to " + q

def ask(q, log):
    clock = time.time()
    for pause in PAUSES:
        try:
            text = fake_provider(q)
            ms = round((time.time() - clock) * 1000, -2)
            log.append({"ok": True, "ms": ms})
            return text
        except RuntimeError:
            time.sleep(pause)

log = []
outside = time.time()                  # a second stopwatch, held by the user
ask("tax rate", log)
print("the user waited (ms):", round((time.time() - outside) * 1000, -2))
print("the log says:", log)
