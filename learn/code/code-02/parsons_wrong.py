import time

BACKOFF = [0.5, 1.0, 0.0]
script = ["529 overloaded", "529 overloaded", "ok"]

def fake_provider(prompt):
    outcome = script.pop(0)
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "reply to: " + prompt

def call(prompt):
    attempts = 0
    for wait in BACKOFF:
        attempts = 0
        attempts = attempts + 1
        try:
            return fake_provider(prompt), attempts
        except RuntimeError:
            time.sleep(wait)
    return None, attempts

print(call("hi"))
