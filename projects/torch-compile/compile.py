"""torch.compile & CUDA graphs (FaizOS build) — Module 12.

Two separate costs, two separate cures:
  1. HBM trips        -> torch.compile captures a GRAPH and fuses ops (automatic Triton).
                         A GRAPH BREAK (print, .item(), data-dependent if) splits the graph and
                         fusion cannot cross it.
  2. Launch overhead  -> every kernel launch costs the CPU ~5us. CUDA graphs record the whole
                         launch sequence once and replay it as a single unit.

Fill the ONE blank, then run:  python3 compile.py
"""

LAUNCH_US = 5.0                      # CPU microseconds to launch one kernel


def trips_eager(n_ops):
    """Eager mode: every op is its own kernel, reading and writing HBM."""
    return 2 * n_ops


def trips_compiled(n_graphs):
    """Compiled: ops fuse WITHIN a graph, so each graph costs one read plus one write.
    Fusion cannot cross a graph break, so the cost scales with the number of GRAPHS."""
    # Careful: this is about how many graphs there are, not how many ops.
    return 2 * n_graphs                       # each graph: one read + one write


def launch_overhead_us(n_kernels):
    return n_kernels * LAUNCH_US


def launch_overhead_cudagraph_us(n_kernels):
    return LAUNCH_US                 # the whole recorded sequence replays as ONE launch


if __name__ == "__main__":
    N_OPS = 6
    print(f"{N_OPS} elementwise ops:")
    print(f"  eager                       : {trips_eager(N_OPS)} HBM trips")
    for breaks in (0, 1, 2):
        graphs = breaks + 1
        t = trips_compiled(graphs)
        note = "  <- same as eager: compilation bought nothing" if t == trips_eager(N_OPS) else ""
        print(f"  compiled, {breaks} break(s) -> {graphs} graph(s): {t} HBM trips{note}")

    print()
    n_kernels = 1000
    eager_us = launch_overhead_us(n_kernels)
    graph_us = launch_overhead_cudagraph_us(n_kernels)
    print(f"{n_kernels} kernel launches per step:")
    print(f"  plain launches : {eager_us:8.1f} us  ({eager_us/1000:.1f} ms of CPU overhead)")
    print(f"  CUDA graph     : {graph_us:8.1f} us  -> {eager_us/graph_us:.0f}x less launch overhead")

    assert trips_eager(6) == 12
    assert trips_compiled(1) == 2, "one graph: fuse everything -> 1 read + 1 write"
    assert trips_compiled(2) == 4, "one break doubles the traffic"
    assert trips_compiled(3) == 6, "two breaks -> no better than eager's per-op cost pattern"
    assert launch_overhead_us(1000) == 5000.0
    print("\nPASS ✅  compile fuses (watch for graph breaks); CUDA graphs kill launch overhead.")
