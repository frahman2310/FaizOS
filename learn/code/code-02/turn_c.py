def fake_model(prompt):
    return {"text": "Filed", "usage": {"input_tokens": 9, "output_tokens": 2}}

def ask(question, log):
    reply = fake_model(question)
    record = {"question": question, "tokens_in": reply["usage"]["input_tokens"]}
    log.append(record)
    return record  # aim: hand back the text of the reply

log = []
first = ask("file tax return", log)
print(log)
second = ask("check refund", log)
print(second)
print(len(log))
print(log[1]["question"])
