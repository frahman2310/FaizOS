PRICES = {"small": {"in": 2.00, "out": 10.00}}   # dollars per 1_000_000 tokens

def price(size, n_in, n_out):
    p = PRICES[size]
    return (n_in * p["in"] + n_out * p["out"]) / 1_000_000

reply = {"words": "done", "n_in": 4000, "n_out": 500}
bill = []
bill.append({"size": "small", "dollars": price("small", reply["n_in"], reply["n_in"])})
print(bill)
