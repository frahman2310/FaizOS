import time

PAUSES = [0.2, 0.4, 0.0]                  # seconds to wait after try 1, 2, 3 fails
outcomes = ["timeout", "ok", "ok"]        # what the fake provider does on each try

def fake_provider(prompt):
    outcome = outcomes.pop(0)             # take the first item out of the list
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "rate: " + prompt

def fetch(prompt):
    tries = 0
    for pause in PAUSES:
        tries = tries + 1
        try:
            return fake_provider(prompt), tries
        except RuntimeError:
            time.sleep(pause)
    return None, tries

print(fetch("hi"))
