# Key check for Try with me 2
reply = {"text": "Due Friday", "usage": {"input_tokens": 15, "output_tokens": 3}}
print("after line 1, reply:", reply)
record = {"text": reply["text"], "tokens_in": reply["usage"]["input_tokens"]}
print("after line 2, record:", record)
log = []
print("after line 3, log:", log)
log.append(record)
print("after line 4, log:", log)
print(log[0]["tokens_in"])
