def fake_provider(prompt):
    return {"text": "ok: " + prompt, "tokens_in": 1200, "tokens_out": 300}

def call(prompt, log):
    # goal: make one AI call and write one record
    answer = fake_provider(prompt)                     # send the request
    log.append({"tokens_in": answer["tokens_in"]})     # write the record
    return answer["text"]                              # hand back the text

log = []
text = call("hi", log)
print(text)
print(log)
