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
            return text
        except RuntimeError as err:
            reason = str(err)
            time.sleep(pause)
        records.append({"done": False, "tries": tries, "reason": reason})
    return None

records = []
calls = 0
fetch("USD to PKR", records)
calls = calls + 1
failed = 0
for r in records:
    if not r["done"]:
        failed = failed + 1
print("calls made:", calls)
print("records:", len(records))
print("records saying failed:", failed)
