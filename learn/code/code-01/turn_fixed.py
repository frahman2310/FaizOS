reply = {"content": [{"type": "text", "text": "Lahore"}], "stop_reason": "end_turn", "usage": {"input_tokens": 8, "output_tokens": 2}}
print(reply["content"][0]["text"])
print("output tokens:", reply["usage"]["output_tokens"])
print(reply["content"][0]["text"])
