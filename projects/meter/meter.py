# =============================================================================
#  FAIZOS  ·  LESSON 3  ·  meter
#  A complete, working, measured LLM call: timed, priced, retried, capped,
#  and fused. You read this file. You do not write it.
#  Run me:   uv run --no-project python meter.py      (takes about 30 seconds)
# =============================================================================

import random
import time

# ---------------------------------------------------------------- the knobs

# Dollars per MILLION tokens. Anthropic list prices, September 2026.
RATES = {
    "haiku":  {"in": 1.00, "out": 5.00},     # Claude Haiku 4.5
    "sonnet": {"in": 2.00, "out": 10.00},    # Claude Sonnet 5
}

# How often the pretend provider misbehaves. main() changes these later.
KNOBS = {"fail": 0.08, "hang": 0.04}

TIMEOUT = 1.0                 # seconds we are willing to wait for one attempt
BACKOFF = [0.5, 1.0, 0.0]     # seconds to wait after attempt 1, 2, 3 fails
TRIP_AT = 3                   # dead calls in a row before the breaker opens
COOL_OFF = 5.0                # seconds the breaker stays open

# The breaker's memory. One dict, two stickers inside it.
breaker = {"dead_in_a_row": 0, "open_until": 0.0}


# ---------------------------------------------------------------- the provider

def provider(prompt, model, timeout):
    """Pretends to be Anthropic's API. Sometimes broken, sometimes slow."""
    roll = random.random()
    if roll < KNOBS["fail"]:
        raise RuntimeError("529 overloaded")
    if roll < KNOBS["fail"] + KNOBS["hang"]:
        takes = 2.0                            # the tail: a call that drags
    else:
        takes = random.uniform(0.05, 0.25)     # a normal call
    if takes > timeout:
        time.sleep(timeout)                    # we waited this long...
        raise TimeoutError("gave up after " + str(timeout) + "s")
    time.sleep(takes)
    return {"text": "reply to: " + prompt, "tokens_in": 1200, "tokens_out": 300}


# ---------------------------------------------------------------- the meter

def cost_of(model, tokens_in, tokens_out):
    rate = RATES[model]
    return (tokens_in * rate["in"] + tokens_out * rate["out"]) / 1_000_000


def breaker_record(ok, now):
    """Tell the breaker how the last call went."""
    if ok:
        breaker["dead_in_a_row"] = 0
    else:
        breaker["dead_in_a_row"] = breaker["dead_in_a_row"] + 1
        if breaker["dead_in_a_row"] >= TRIP_AT:
            breaker["open_until"] = now + COOL_OFF
            breaker["dead_in_a_row"] = 0


def call(prompt, model, log):
    """One call. Always writes exactly one record into log."""
    start = time.time()

    if start < breaker["open_until"]:
        log.append({"model": model, "ok": False, "why": "breaker open",
                    "ms": 0.0, "attempts": 0, "cost": 0.0})
        return None

    attempts = 0
    why = ""
    for wait in BACKOFF:
        attempts = attempts + 1
        try:
            answer = provider(prompt, model, TIMEOUT)
            ms = (time.time() - start) * 1000
            log.append({"model": model, "ok": True, "why": "",
                        "ms": ms, "attempts": attempts,
                        "cost": cost_of(model, answer["tokens_in"], answer["tokens_out"])})
            breaker_record(True, time.time())
            return answer["text"]
        except (RuntimeError, TimeoutError) as err:
            why = str(err)
            time.sleep(wait)

    ms = (time.time() - start) * 1000
    log.append({"model": model, "ok": False, "why": why,
                "ms": ms, "attempts": attempts, "cost": 0.0})
    breaker_record(False, time.time())
    return None


def percentile(numbers, fraction):
    line = sorted(numbers)
    spot = int(len(line) * fraction) - 1
    return line[spot]


def report(title, log):
    oks = []
    for row in log:
        if row["ok"]:
            oks.append(row)

    times = []
    for row in oks:
        times.append(row["ms"])

    spend = 0.0
    for row in log:
        spend = spend + row["cost"]

    retried = 0
    for row in oks:
        if row["attempts"] > 1:
            retried = retried + 1

    skipped = 0
    for row in log:
        if row["why"] == "breaker open":
            skipped = skipped + 1

    print()
    print("  " + title)
    print(f"  calls              {len(log)}")
    print(f"  succeeded          {len(oks)}  ({len(oks) / len(log) * 100:.0f}%)")
    print(f"  succeeded on retry {retried}")
    print(f"  skipped by breaker {skipped}")
    print(f"  spend              ${spend:.4f}")
    if len(times) == 0:
        print("  no successful calls, nothing to time")
        return
    print(f"  cost per success   ${spend / len(oks):.5f}")
    print(f"  p50 latency        {percentile(times, 0.50):.0f} ms")
    print(f"  p95 latency        {percentile(times, 0.95):.0f} ms")
    print(f"  slowest success    {max(times):.0f} ms")


def main():
    random.seed(3)

    log = []
    for i in range(100):
        call("summarise this invoice", "haiku", log)
    report("SCENE 1 · a normal day, 100 calls", log)

    KNOBS["fail"] = 1.0                      # the provider goes down
    log = []
    for i in range(20):
        call("summarise this invoice", "haiku", log)
    report("SCENE 2 · the provider is down, 20 calls", log)


main()
