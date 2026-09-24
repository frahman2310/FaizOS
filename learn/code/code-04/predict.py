times = [210, 180, 950, 200, 190]      # ms for five calls; the aim is the middle time
times.sort
print("A", times[2])
times.sort()
print("B", times[2])
print("C", times[5])
