# Key check for Show 2
reply = {"text": "Paid", "usage": {"input_tokens": 11, "output_tokens": 2}}
print("after line 1, reply:", reply)
record = {"text": reply["text"], "tokens_out": reply["usage"]["output_tokens"]}
print("after line 2, record:", record)
log = []
print("after line 3, log:", log)
log.append(record)
print("after line 4, log:", log)
print(log)
