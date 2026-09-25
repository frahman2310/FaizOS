reply = {"text": "Paid", "usage": {"input_tokens": 11, "output_tokens": 2}}
record = {"text": reply["text"], "tokens_out": reply["usage"]["output_tokens"]}
log = []
log.append(record)
print(log)
