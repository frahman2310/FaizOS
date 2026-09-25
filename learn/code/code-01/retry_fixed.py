reply = {"content": [{"type": "text", "text": "Rawalpindi"}], "stop_reason": "max_tokens", "usage": {"input_tokens": 16, "output_tokens": 30}}
print(reply["usage"]["input_tokens"])
print(reply["usage"]["output_tokens"])
print(reply["content"][0]["text"])
