reply = {
    "content": [{"type": "text", "text": "Gilgit"}],
    "stop_reason": "end_turn",
    "usage": {"input_tokens": 12, "output_tokens": 2},
}
print(reply["content"])
print(reply["content"][0])
print(reply["content"][0]["text"])
