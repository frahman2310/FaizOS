# The check most likely to be asked for: print what reaches cost_of on the buggy line.
import time
from bug import fake_provider, RATES

def cost_of(model, tokens_in, tokens_out):
    print("cost_of got tokens_in =", tokens_in, "and tokens_out =", tokens_out)
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

answer = fake_provider("hi")
print("answer =", answer)
print("cost =", cost_of("haiku", answer["tokens_out"], answer["tokens_in"]))
