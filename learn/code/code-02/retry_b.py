def fake_model(prompt):
    return {"text": "Sent", "usage": {"input_tokens": 12, "output_tokens": 5}}

def send(message, calls):
    reply = fake_model(message)
    record = {"message": message, "tokens_out": reply["output_tokens"]}
    calls.append(record)
    return reply["text"]

calls = []
a = send("remind Ali", calls)
b = send("remind Sara", calls)
print(calls)
c = send("remind Omar", calls)
print(c)
print(len(calls))
print(calls[0]["message"])
