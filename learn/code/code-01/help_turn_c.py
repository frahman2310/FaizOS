reply = {"content": [{"type": "text", "text": "Peshawar"}], "stop_reason": "end_turn", "usage": {"input_tokens": 10, "output_tokens": 5}}
print(reply["stop_reason"])  # aim: why the model stopped
