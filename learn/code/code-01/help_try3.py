reply = {
    "content": [{"type": "text", "text": "Multan"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 11, "output_tokens": 3},
}
print(reply["usage"])
print(reply["usage"]["output_tokens"])
