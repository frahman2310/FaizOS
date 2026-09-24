import time

RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per 1_000_000 tokens

def fake_provider(prompt):
    time.sleep(0.3)                  # pretend the AI takes a moment
    return {"text": "ok: " + prompt, "tokens_in": 1200, "tokens_out": 300}

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

def call(prompt, model, log):
    # goal: make one AI call and write one record of what it cost and how long it took
    # 1. start the clock
    start = time.time()                                               # (a)
    # 2. send the request
    answer = fake_provider(prompt)                                    # (b)
    # 3. pull the fields out of the reply
    ms = round((time.time() - start) * 1000, -2)                      # (c)
    cost = cost_of(model, answer["tokens_in"], answer["tokens_out"])  # (d)
    # 4. write the record, then hand back the text
    log.append({"model": model, "ms": ms, "cost": cost})              # (e)
    return answer["text"]

log = []
text = call("hi", "haiku", log)
print(text)
print(log)
