# Key check for Try with me 3: what each option does
reply = {"text": "Karachi", "usage": {"input_tokens": 20, "output_tokens": 50}}
options = {
    "A": lambda: reply["input_tokens"],
    "B": lambda: reply["usage"],
    "C": lambda: reply["usage"]["input_tokens"],
    "D": lambda: reply["usage"]["output_tokens"],
}
for name, get in options.items():
    try:
        print(name, "prints", get())
    except KeyError as err:
        print(name, "crashes: KeyError:", err)
