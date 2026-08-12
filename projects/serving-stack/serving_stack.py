"""Serving stacks — prefill vs decode, throughput vs latency (FaizOS build) — Module 14.

A request has two phases with opposite bottlenecks:
  PREFILL - the whole prompt goes through at once -> lots of math per weight read -> COMPUTE-bound
  DECODE  - one token at a time, each reading every weight -> MEMORY-bound

Because decode is memory-bound, one pass over the weights can serve the WHOLE batch: 32 users get
32 tokens for the price of one weight read. That is why batching is the lever in serving.
Fill the ONE blank, then run:  python3 serving_stack.py
"""

WEIGHTS_GB   = 14.0        # a 7B model in fp16
BANDWIDTH_GB = 2000.0      # HBM bytes per second, in GB
PEAK_TFLOPS  = 500.0       # effective compute
N_PARAMS     = 7e9


def decode_step_ms(batch):
    """One decode step reads every weight ONCE, whatever the batch size (memory-bound)."""
    return WEIGHTS_GB / BANDWIDTH_GB * 1000


def decode_throughput(batch):
    """Tokens per second across all users: one token per user per step."""
    # Every user in the batch gets one token out of the same step.
    return batch * 1000 / decode_step_ms(batch)  # one token per user, per step, per second


def prefill_ms(prompt_tokens):
    """Prefill does ~2 FLOPs per parameter per prompt token, and it is compute-bound."""
    flops = 2 * N_PARAMS * prompt_tokens
    return flops / (PEAK_TFLOPS * 1e12) * 1000


def request_latency_ms(prompt_tokens, output_tokens, batch):
    """Time to first token, then one decode step per remaining output token."""
    return prefill_ms(prompt_tokens) + (output_tokens - 1) * decode_step_ms(batch)


if __name__ == "__main__":
    step = decode_step_ms(1)
    print(f"one decode step: {step:.1f} ms   (reads {WEIGHTS_GB:.0f} GB at {BANDWIDTH_GB:.0f} GB/s)\n")

    print(f"  {'batch':>6} {'tokens/s (all users)':>22} {'tokens/s per user':>19}")
    for b in (1, 8, 32, 128):
        total = decode_throughput(b)
        print(f"  {b:>6} {total:>22,.0f} {total / b:>19,.0f}")

    print(f"\nTTFT for a 500-token prompt: {prefill_ms(500):.0f} ms")
    print(f"full request (500 in, 200 out, batch 32): {request_latency_ms(500, 200, 32):.0f} ms")

    assert abs(decode_step_ms(1) - 7.0) < 1e-9, "14 GB / 2000 GB/s = 7 ms"
    assert abs(decode_throughput(1) - 1000 / 7) < 1e-6, "one user: ~143 tokens/s"
    assert abs(decode_throughput(32) / decode_throughput(1) - 32) < 1e-9, "batching scales throughput"
    # per-user speed is unchanged by batching; only total throughput grows
    assert abs(decode_throughput(32) / 32 - decode_throughput(1)) < 1e-6
    print("\nPASS ✅  decode is memory-bound, so batching multiplies throughput at no per-step cost.")
