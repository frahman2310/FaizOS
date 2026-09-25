def fake_model(prompt):
    return {"text": "Approved", "usage": {"input_tokens": 20, "output_tokens": 1}}

def review(claim, history):
    reply = fake_model(claim)
    record = {"claim": claim, "tokens_in": reply["input_tokens"]}
    history.append(record)
    return reply["text"]

history = []
r1 = review("fuel receipt", history)
print(history)
r2 = review("hotel bill", history)
print(r2)
print(len(history))
print(history[1]["claim"])
print(history[0]["tokens_in"])
