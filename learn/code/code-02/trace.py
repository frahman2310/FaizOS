import time

PAUSES = [0.2, 0.4, 0.0]                  # seconds to wait after try 1, 2, 3 fails
outcomes = ["timeout", "ok", "ok"]        # what the fake provider does on each try

def fake_provider(prompt):
    outcome = outcomes.pop(0)
    if outcome != "ok":
        raise RuntimeError(outcome)
    return "rate: " + prompt

def fetch(prompt, records):
    # goal: get one reply, trying again after a failure, and write one record
    # 1. set start values
    tries = 0
    reason = ""
    for pause in PAUSES:
        # 2. try
        tries = tries + 1                                    # (a)
        try:
            text = fake_provider(prompt)                     # (b)
            # 3. record the success and leave
            records.append({"done": True, "tries": tries})   # (c)
            return text
        except RuntimeError as err:
            # 4. note why, wait, go round again
            reason = str(err)                                # (d)
            time.sleep(pause)
    # 5. give up: record the failure once
    records.append({"done": False, "tries": tries, "reason": reason})
    return None

records = []
print(fetch("USD to PKR", records))
print(records)
