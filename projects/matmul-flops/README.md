# Matmul FLOP + roofline estimator

Built in **ForgeOS**. A tiny tool that estimates how expensive a matrix multiplication is, and
whether it's limited by *doing math* or by *moving data*.

## Background — from zero (read this first)

**Why this exists.** An AI model (like GPT) is, under the hood, mostly a giant pile of **matrix
multiplications**. "Running the model" = doing those multiplications. So if you can estimate the
cost of *one* matrix multiply, you can reason about how fast a model runs, how much GPU memory it
needs, and how much it costs to serve. That's a foundational AI-engineer skill — this is step one.

**Matrix.** A grid of numbers with rows and columns. A "2×3 matrix" has 2 rows and 3 columns. A
model's learned "weights" are big matrices; your data is matrices too.

**Matrix multiplication (matmul).** To multiply matrix `A` (shape `M×K`) by matrix `B` (shape
`K×N`), you get matrix `C` (shape `M×N`). Rule: each cell `C[i][j]` = take **row i of A** and
**column j of B**, multiply them position-by-position, and add up the results.
- `M` = rows of the answer, `N` = columns of the answer, `K` = the shared length you multiply along.
- Worked example: `A=[[1,2],[3,4]]`, `B=[[5,6],[7,8]]` (M=N=K=2). `C[0][0]` = `1*5 + 2*7 = 19`.
  Full answer `C=[[19,22],[43,50]]`.

**Dot product.** The "multiply position-by-position and add" step. `[1,2,3]·[4,5,6] = 4+10+18 = 32`.
A dot product of length `K` costs `K` multiplies + `K` adds ≈ **`2K` operations**.

**FLOP.** "Floating-point operation" = one arithmetic step on decimal numbers (one multiply, or one
add). We count FLOPs because more FLOPs = more work = slower/pricier. A whole matmul has `M*N` output
cells, each costing `2K` → **`2 * M * N * K` FLOPs**. (That's function #1.)

**Bytes & dtype.** Numbers take space in memory. `fp32` = 32-bit float = 4 bytes each; `bf16` =
16-bit "brain float" = 2 bytes each (models use bf16 to be smaller/faster). To do the matmul the GPU
must **read** A and B and **write** C, i.e. move `M*K + K*N + M*N` numbers, each `dtype_bytes` bytes.
(Function #2.)

**GPU, and the two speed limits.** A GPU is the chip that runs AI. It has (1) a max math speed
(FLOPs/second) and (2) a max data-moving speed (bytes/second). Any operation is bottlenecked by
whichever limit it hits first.

**Arithmetic intensity = FLOPs ÷ bytes** — how much math you do per byte you fetch. Analogy: driving
to the store (fetch data) to cook. Cook a feast → the trip was worth it, you're limited by cooking
speed = **compute-bound**. Drive all that way for one apple → limited by the driving = **memory-bound**.
Each GPU has its own FLOP:byte ratio (an NVIDIA **H100** in bf16 ≈ **295 FLOPs per byte**). If your
op's intensity is **above** that → compute-bound; **below** → memory-bound. (Function #3.)

**The punchline (why the two tests below matter).** A big square matmul does tons of math per byte →
compute-bound. A **GEMV** (matrix × *vector*, i.e. `M=1`) does almost no math per byte → memory-bound.
And `M=1` is *exactly* what happens when a language model generates **one token at a time**. That's
why LLM text generation is limited by memory bandwidth, not raw compute — a fact that shapes the whole
inference-hardware industry. You'll have derived it yourself.

## Your job
Fill in the 3 `TODO`s in `flops.py`, then run it. When the acceptance checks pass, you ship.

## Acceptance criteria (verifiable)
- `matmul_flops(2,3,4) == 48` (= `2·M·N·K`), and it holds for a real `1024×4096×4096` layer too
- `matmul_bytes` counts A + B + C in the given dtype
- `roofline_verdict`: a big square matmul is **compute-bound**; a GEMV (`M=1`) is **memory-bound**

## Run
```bash
python3 flops.py
```
