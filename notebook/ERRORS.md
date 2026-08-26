# Error taxonomy

Open categories weight the next rules card. Generated from the database; do not edit by hand.

## Open

| category | occurrences | last seen | the rule it breaks |
|---|---|---|---|
| api-misuse | 5 | 2026-08-26 | Square brackets look up, round brackets call. Variable names come from the code, never from the sentence describing it. |
| expression-vs-statement | 3 | 2026-08-14 | return and append already receive the value. Write only the expression, no equals sign, no units. |
| inverse-relationship | 3 | 2026-08-14 | A rate is one over a duration. If an improvement should make the number bigger, the time goes on the bottom. exp undoes ln. |
| off-by-one | 3 | 2026-08-14 | Ask which half of a paired operation consumes rather than adds before counting. Verify powers of two by doubling. |
| missing-call-brackets | 2 | 2026-08-14 | A name refers to the function. Round brackets with its input actually run it. |
| ordering-pairing | 2 | 2026-08-14 | Pair each value with its own source. Lowest reward takes the most negative advantage; the query uses its own position. |
| shape-mismatch | 1 | 2026-08-14 | How many numbers you store and what shape they produce are different questions. Inner dimensions cancel. |
| silent-truncation | 1 | 2026-08-14 | Keep the fraction. Rounding away the decimal can hide the size of the result. |

### Detail

**api-misuse** (5): tokens_in used inside cache_cost(cached_in, rate_in). NameError. Name taken from the topic being discussed rather than the parameter list.

**expression-vs-statement** (3): An assignment or English written where a bare expression belongs. Cases: residual = seq[i] + attn[i] inside a comprehension; return 2 trips; rm_score = drift * -beta inside a return.

**inverse-relationship** (3): Duration and rate inverted, and exp/ln not treated as inverses. Cases: Amdahl speedup written as new_time * original; tokens per second answered with the step duration; exp(0.693) answered as 0.693.

**off-by-one** (3): An implicit gained or released term missed, and small count slips. Cases: speculative decoding answered accepted instead of accepted + 1; GPipe peak doubled because backward was counted as storing rather than freeing; 8192/1024 answered as 7.

**missing-call-brackets** (2): Bare function name where a call was needed. Cases: "all gather pieces" for all_gather(pieces); decode_step_ms without brackets where a value was needed.

**ordering-pairing** (2): The right set of values paired with the wrong sources. Cases: advantages listed 2, 0, -2 for rewards 5, 7, 9 (reversed); RoPE query rotated by j instead of its own position i.

**shape-mismatch** (1): Stored count confused with produced shape. Case: LoRA B@A said to produce 8000 when it stores 2dr numbers but produces a d by d grid; the matmul inner-cancel rule needed re-deriving.

**silent-truncation** (1): A fractional part dropped from an answer. Case: 50/4 reported as 12x rather than 12.5x.

## Resolved

None yet. A category resolves after three clean builds in a row.
