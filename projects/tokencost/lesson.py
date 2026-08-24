# =============================================================================
#  FAIZOS LESSON 1  ·  What an AI feature costs
#  Run me:   uv run python lesson.py
# =============================================================================
#
#  THE PROBLEM
#  -----------
#  You are in an interview. Someone says: "we'd have 100,000 users, each sending
#  about 10 messages a day." Then they look at you.
#
#  The expected answer is a dollar figure, out loud, in about fifteen seconds.
#  Engineers who can do this get hired. It is repeatedly named the single thing
#  that separates people who have shipped from people who have only prototyped.
#
#  This file teaches you to produce that number.
#
#
#  CONCEPT 1 — Tokens
#  ------------------
#  A model does not read letters or words. It reads TOKENS: chunks of text,
#  roughly 4 characters each. "Hello world" is about 3 tokens. A page of text is
#  about 500. This whole file is about 1,500.
#
#
#  CONCEPT 2 — You pay twice, at different prices
#  -----------------------------------------------
#  Every call to a model has two separate bills:
#
#      INPUT  = the tokens you send it   (your question, your documents)
#      OUTPUT = the tokens it sends back (its answer)
#
#  Output costs about FIVE TIMES more per token than input. The model has to
#  generate output one token at a time, which is slow and hard; reading input
#  it can do all at once, which is fast and cheap.
#
#  This is why you got the earlier question right. Reading 2,000 tokens costs
#  $0.006, but writing only 500 costs $0.0075. A quarter as many tokens, and it
#  still costs more. Chatty models are expensive models.
#
#
#  CONCEPT 3 — Prices are quoted per MILLION tokens
#  -------------------------------------------------
#  A real price is $0.000003 per token. Nobody can read that without counting
#  zeros, so every provider quotes "$3 per million" instead.
#
#  That means your arithmetic always has a division by a million in it. This is
#  the one place people get it backwards, so say it to yourself once:
#
#      PER MILLION MEANS THE MILLION GOES ON THE BOTTOM.
#
#  Multiply instead and your answer is a million times too big.
#
# =============================================================================


# -----------------------------------------------------------------------------
#  THE CODE  (I wrote this part. Read it, then scroll to YOUR TURN.)
# -----------------------------------------------------------------------------

PER_MILLION = 1_000_000
# A constant. The underscores are invisible to Python: 1_000_000 IS 1000000.
# They exist so your eye can count the zeros without squinting.
# It is named once so you can never typo it as 100_000 somewhere later.


def cost(tokens_in, tokens_out, rate_in, rate_out):
    # This function answers: what did ONE call to the model cost me?
    #
    #   tokens_in   how many tokens I sent
    #   tokens_out  how many tokens came back
    #   rate_in     dollars per MILLION input tokens   (e.g. 3.0)
    #   rate_out    dollars per MILLION output tokens  (e.g. 15.0)

    input_cost = tokens_in * rate_in / PER_MILLION
    # Read it left to right: take the token count, multiply by the price of a
    # million, then divide by a million to scale it down to what you actually used.
    # 2000 tokens * $3 = 6000, / 1,000,000 = $0.006.

    output_cost = tokens_out * rate_out / PER_MILLION
    # Identical shape, different rate. Input and output are worked out separately
    # because they are priced separately.

    return input_cost + output_cost
    # `return` hands the value back to whoever called this function.
    # Notice there is no `=` sign here. `return` already receives the value;
    # writing `return total = x + y` is an error.


def daily_cost(users, calls_per_user, tokens_in, tokens_out, rate_in, rate_out):
    # This function answers: what does the WHOLE PRODUCT cost me per day?

    calls_per_day = users * calls_per_user
    # 100,000 users each sending 10 messages = 1,000,000 calls a day.

    return calls_per_day * cost(tokens_in, tokens_out, rate_in, rate_out)
    # Rather than redo the arithmetic, this CALLS the function above and
    # multiplies its answer. The price of one call is defined in exactly one
    # place, so if it is ever wrong, it is wrong in only one place.


# =============================================================================
#  ▼▼▼  YOUR TURN  ▼▼▼
# =============================================================================
#
#  WHAT YOU ARE ADDING
#  -------------------
#  Providers let you mark part of your prompt as reusable. If you send the same
#  text again within a few minutes, they charge you ONE TENTH of the normal input
#  rate for it, because they skipped the work of reading it.
#
#  This is the biggest cost lever in the entire field. A support bot that resends
#  the same 20,000-token manual with every question pays full price for it 10,000
#  times a day, or a tenth of that. Same product, ten times the bill.
#
#  Your job: teach `cost_with_cache` to handle those cheap cached tokens.
#
#
#  THE PYTHON YOU NEED  (this is the part you are learning)
#  --------------------------------------------------------
#
#  RULE 1 — A DEFAULT ARGUMENT lets an input be optional.
#      def f(a, b=0):
#      means: if the caller does not mention `b`, it is 0.
#      Defaults must come AFTER all the normal arguments, never before.
#
#  RULE 2 — A TENTH is `* 0.1`.
#      Not `/ 0.1`. Dividing by 0.1 makes a number ten times BIGGER.
#      If your answer comes out huge, you divided where you should have multiplied.
#
#  RULE 3 — `return` takes an EXPRESSION, never an assignment.
#      RIGHT:  return a + b
#      WRONG:  return total = a + b
#
#  RULE 4 — You can call a function from inside another function.
#      `cost(...)` already works. You are allowed to use it rather than
#      rewriting the input and output arithmetic by hand.
#
#
#  YOUR RULES FOR THIS FUNCTION
#  -----------------------------
#   1. `cached_in` must DEFAULT to 0, so old callers who never heard of caching
#      still get the right answer.
#   2. Cached tokens are charged at rate_in * 0.1, scaled by PER_MILLION like
#      everything else.
#   3. Fresh input, cached input and output all ADD together.
#
# -----------------------------------------------------------------------------


def cost_with_cache(tokens_in, tokens_out, rate_in, rate_out, cached_in=0):
    # WRITE YOUR CODE BETWEEN THE ARROWS. Delete the `pass` line.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    pass

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▲▲▲  END OF YOUR TURN  ▲▲▲
# =============================================================================


# -----------------------------------------------------------------------------
#  THE CHECKS  (I wrote these. They tell you when you are done.)
# -----------------------------------------------------------------------------

def check(label, got, want):
    close_enough = abs(got - want) < 0.0000001 if got is not None else False
    print(f"  {'PASS' if close_enough else 'FAIL'}  {label}")
    if not close_enough:
        print(f"        expected {want}, got {got}")
    return close_enough


def main():
    print("\nMy code, already working:")
    results = [
        check("one million input tokens at $3",       cost(1_000_000, 0, 3.0, 15.0), 3.0),
        check("one million output tokens at $15",     cost(0, 1_000_000, 3.0, 15.0), 15.0),
        check("reading 2000 tokens",                  cost(2_000, 0, 3.0, 15.0), 0.006),
        check("writing 500 tokens costs MORE",        cost(0, 500, 3.0, 15.0), 0.0075),
        check("100k users x 10 calls x 2k tokens",    daily_cost(100_000, 10, 2_000, 0, 3.0, 15.0), 6_000.0),
    ]

    print("\nYour code:")
    results += [
        check("cached tokens cost a tenth",           cost_with_cache(0, 0, 3.0, 15.0, cached_in=1_000_000), 0.30),
        check("fresh + cached add up",                cost_with_cache(1_000_000, 0, 3.0, 15.0, cached_in=1_000_000), 3.30),
        check("still works with no caching at all",   cost_with_cache(1_000_000, 0, 3.0, 15.0), 3.0),
        check("output still counted",                 cost_with_cache(0, 1_000_000, 3.0, 15.0, cached_in=1_000_000), 15.30),
    ]

    passed = sum(1 for r in results if r)
    print(f"\n{passed} of {len(results)} passing.")
    if passed == len(results):
        print("Done. Tell me and I'll review it.\n")
    else:
        print("Not yet. Stuck? Run /faiz-hint for one hint at a time.\n")


main()
