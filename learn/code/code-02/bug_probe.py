import time

PAUSES = [0.2, 0.4, 0.0]                  # seconds to wait after try 1, 2, 3 fails
outcomes = ["timeout", "ok", "ok"]        # what the fake provider does on each try

def fake_provider(prompt):
    outcome = outcomes.pop(0)             # take the first item out of the list
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "rate: " + prompt

def fetch(prompt, records):
    tries = 0
    reason = ""
    for pause in PAUSES:
        tries = tries + 1
        try:
            text = fake_provider(prompt)
            records.append({"done": True, "tries": tries})
            print("after the success line: tries =", tries, "records =", records)
            return text
        except RuntimeError as err:
            reason = str(err)
            time.sleep(pause)
        records.append({"done": False, "tries": tries, "reason": reason})
        print("after the failure line: tries =", tries, "records =", records)
    return None

fetch("USD to PKR", [])
