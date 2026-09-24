# The check most likely to be asked for: when does the clock start, and what does it measure?
import time
import bug

bug.answers[:] = ["busy", "ok"]
log = []
tries = 0
outside = time.time()
for pause in bug.PAUSES:
    clock = time.time()
    tries = tries + 1
    print("try", tries, ": clock started", round((clock - outside) * 1000, -2), "ms after the user pressed send")
    try:
        text = bug.fake_provider("tax rate")
        print("logged ms:", round((time.time() - clock) * 1000, -2))
        break
    except RuntimeError:
        time.sleep(pause)
