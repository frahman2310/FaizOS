def fetch(prompt, records):
    # goal: get one reply, trying again after a failure, and write one record
    tries = 0
    for outcome in ["timeout", "ok"]:
        tries = tries + 1
        if outcome == "ok":
            records.append({"done": True, "tries": tries})
            return "rate: " + prompt
    return None

records = []
print(fetch("USD to PKR", records))
print(records)
