reply = {"content": [{"type": "text", "text": "Lahore"}], "stop_reason": "end_turn", "usage": {"input_tokens": 8, "output_tokens": 2}}
print(reply["stop_reason"])  # aim: why the model stopped
