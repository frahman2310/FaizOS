times = [210, 180, 950, 200, 190]      # milliseconds for five calls

times.sort
middle = times[len(times) // 2]        # the middle one: the p50
print(middle)
