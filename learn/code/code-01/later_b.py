reply = {"choices": [{"message": {"role": "assistant", "content": "Quetta"}}], "usage": {"prompt_tokens": 12, "completion_tokens": 3}}
print(reply["usage"]["completion_tokens"])  # aim: the output token count
