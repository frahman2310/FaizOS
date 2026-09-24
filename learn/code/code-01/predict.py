RATES = {"haiku": {"in": 1.00, "out": 5.00}}   # dollars per million tokens

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000

print(cost_of("haiku", 1200, 300))
print(cost_of("sonnet", 1200, 300))
