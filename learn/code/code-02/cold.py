import time

DELAYS = [0.1, 0.3, 0.0]
replies = ["busy", "busy", "ok"]

def ask():
    r = replies.pop(0)
    if r != "ok":
        raise RuntimeError(r)
    return "price 42"

def get(history):
    for delay in DELAYS:
        waited = 0.0
        try:
            value = ask()
            history.append({"worked": True, "waited": waited})
            return value
        except RuntimeError:
            time.sleep(delay)
            waited = waited + delay

history = []
print(get(history))
print(history)
