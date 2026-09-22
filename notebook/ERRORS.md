# Error taxonomy

Open categories weight the next rules card. Generated from the database; do not edit by hand.

## Open

| category | occurrences | last seen | the rule it breaks |
|---|---|---|---|
| api-misuse | 7 | 2026-09-03 | Square brackets look up, round brackets call. Variable names come from the code, never from the sentence describing it. |
| inverse-relationship | 5 | 2026-09-22 | A rate is one over a duration. If an improvement should make the number bigger, the time goes on the bottom. exp undoes ln. |
| ordering-pairing | 5 | 2026-09-22 | Pair each value with its own source. Lowest reward takes the most negative advantage; the query uses its own position. |
| expression-vs-statement | 3 | 2026-08-14 | return and append already receive the value. Write only the expression, no equals sign, no units. |
| off-by-one | 3 | 2026-08-14 | Ask which half of a paired operation consumes rather than adds before counting. Verify powers of two by doubling. |
| missing-call-brackets | 2 | 2026-08-14 | A name refers to the function. Round brackets with its input actually run it. |
| shape-mismatch | 1 | 2026-08-14 | How many numbers you store and what shape they produce are different questions. Inner dimensions cancel. |
| silent-truncation | 1 | 2026-08-14 | Keep the fraction. Rounding away the decimal can hide the size of the result. |

### Detail

**api-misuse** (7): cost_for(MODELS, ...) — passed the whole list where one model belonged, three attempts running. Also cost_for("pricey_model") — passed the quoted parameter NAME instead of the value it holds.

**inverse-relationship** (5): Best-of-five reporting: could not say it biases the reported rate upward

**ordering-pairing** (5): Complement count: 40 PASS, judge agreed on 36, answered 6 disagreed instead of 4

**expression-vs-statement** (3): An assignment or English written where a bare expression belongs. Cases: residual = seq[i] + attn[i] inside a comprehension; return 2 trips; rm_score = drift * -beta inside a return.

**off-by-one** (3): An implicit gained or released term missed, and small count slips. Cases: speculative decoding answered accepted instead of accepted + 1; GPipe peak doubled because backward was counted as storing rather than freeing; 8192/1024 answered as 7.

**missing-call-brackets** (2): Bare function name where a call was needed. Cases: "all gather pieces" for all_gather(pieces); decode_step_ms without brackets where a value was needed.

**shape-mismatch** (1): Stored count confused with produced shape. Case: LoRA B@A said to produce 8000 when it stores 2dr numbers but produces a d by d grid; the matmul inner-cancel rule needed re-deriving.

**silent-truncation** (1): A fractional part dropped from an answer. Case: 50/4 reported as 12x rather than 12.5x.

## Resolved

None yet. A category resolves after three clean builds in a row.
