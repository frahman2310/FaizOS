reply = {"choices": [{"message": {"role": "assistant", "content": "Quetta"}}], "usage": {"prompt_tokens": 12, "completion_tokens": 3}}
print(reply["choices"][0]["message"]["content"])
print(reply["usage"]["prompt_tokens"])
