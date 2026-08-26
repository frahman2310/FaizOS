# =============================================================================
#  FAIZOS LESSON 1  ·  What an AI feature costs
#  Run me:   uv run python lesson.py
# =============================================================================
#
#  THE PROBLEM
#  -----------
#  You are in an interview. Someone says: "we'd have 100,000 users, each sending
#  about 10 messages a day." Then they look at you, waiting for a dollar figure.
#
#  Engineers who can answer that get hired. This file teaches you to produce it,
#  and teaches you to write Python while you do it.
#
# =============================================================================
#  PART 1 · HOW TO WRITE A LINE OF PYTHON
#  Read this even if it feels too basic. It is the whole grammar you need today.
# =============================================================================
#
#  There are only TWO kinds of line in this entire lesson.
#
#
#  KIND 1 — Give something a name.
#
#       total = 5 + 3
#
#  Read it RIGHT TO LEFT: work out `5 + 3`, then hang the label `total` on the
#  answer. The name goes on the LEFT of the `=`. The work goes on the RIGHT.
#  From that line onwards, the word `total` means 8.
#
#  You can name as many things as you like, one per line:
#
#       price = 10
#       tax   = 2
#       final = price + tax          <- now `final` means 12
#
#
#  KIND 2 — Hand your answer back.
#
#       return final
#
#  `return` means "this is my answer, give it to whoever asked for it."
#  A return line NEVER has an `=` in it. `return final = 12` is broken.
#
#
#  THAT IS THE WHOLE GRAMMAR. Names on the left, work on the right, one answer
#  at the end.
#
#
#  BUILDING A CALCULATION IN STEPS
#  --------------------------------
#  You never have to cram everything onto one line. Break it into small pieces,
#  one per line, then combine them at the end. Here is a shopping bill:
#
#       def shopping_bill(apples, loaves, milk):
#           apple_cost = apples * 0.30        # 4 apples at 30p  -> 1.20
#           bread_cost = loaves * 1.10        # 2 loaves at 1.10 -> 2.20
#           milk_cost  = milk   * 0.90        # 1 milk at 90p    -> 0.90
#           return apple_cost + bread_cost + milk_cost      # -> 4.30
#
#  Three things being paid for, so THREE named lines, then ONE return that adds
#  them together. Each line does one small job.
#
#  This shape — name the pieces, then add them — is what almost every function
#  you write for the rest of your life looks like.
#
#
#  INDENTATION (the thing that trips up everyone on day one)
#  ---------------------------------------------------------
#  Every line inside a function must start with exactly 4 spaces. Python uses
#  those spaces to know which lines belong to the function. Not 2, not 3. Four.
#  If your lines do not line up underneath each other, Python refuses to run.
#
# =============================================================================
#  PART 2 · THE THREE THINGS YOU ARE PAYING FOR
# =============================================================================
#
#  A model does not read letters. It reads TOKENS: chunks of about 4 characters.
#  A page of text is roughly 500 tokens.
#
#  Every call to a model has a bill with up to THREE lines on it:
#
#     1. INPUT  — the tokens you send.        Full price.
#     2. OUTPUT — the tokens it sends back.   About FIVE TIMES the input price.
#     3. CACHED — input it has seen recently. ONE TENTH of the input price.
#
#  Output being dearer is why you were right earlier: reading 2,000 tokens costs
#  $0.006, but writing just 500 costs $0.0075. A quarter of the tokens, more money.
#
#  Cached input is the biggest cost lever in the field. A support bot that resends
#  the same 20,000-token manual with every question pays full price for it 10,000
#  times a day, or a tenth of that. Same product, ten times the bill.
#
#
#  PRICES ARE QUOTED PER MILLION TOKENS
#  -------------------------------------
#  A real price is $0.000003 per token. Unreadable. So everyone quotes "$3 per
#  million" instead, and your arithmetic always divides by a million:
#
#       PER MILLION MEANS THE MILLION GOES ON THE BOTTOM.
#
#  2,000 tokens * $3 = 6,000, divided by a million = $0.006. Correct.
#  Forget the division and your answer is a million times too big.
#
# =============================================================================


# -----------------------------------------------------------------------------
#  PART 3 · MY CODE  (working already. Read it, it is the shape you will copy.)
# -----------------------------------------------------------------------------

PER_MILLION = 1_000_000
# A name for a number, so it is written once and cannot be mistyped later.
# The underscores are invisible to Python: 1_000_000 IS 1000000.


def cost(tokens_in, tokens_out, rate_in, rate_out):
    # TWO things are being paid for here, so TWO named lines, then one return.
    # This is the shopping bill shape from Part 1.

    input_cost = tokens_in * rate_in / PER_MILLION
    # Name on the left. Work on the right. Tokens, times the price of a million,
    # divided by a million to scale it down to what you actually used.

    output_cost = tokens_out * rate_out / PER_MILLION
    # Same shape again, with the output numbers instead.

    return input_cost + output_cost
    # The two names, added. No `=` on a return line.


def daily_cost(users, calls_per_user, tokens_in, tokens_out, rate_in, rate_out):
    calls_per_day = users * calls_per_user
    # 100,000 users each sending 10 messages = 1,000,000 calls a day.

    return calls_per_day * cost(tokens_in, tokens_out, rate_in, rate_out)
    # This CALLS the function above rather than redoing its arithmetic.
    # Writing `cost(...)` runs it and gives you back its answer.


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 1 of 2  (the small one) ▼▼▼
# =============================================================================
#
#  Write the price of cached tokens on their own.
#
#  WHAT IT MUST DO: cached tokens are charged at ONE TENTH of the input rate.
#
#  THE PYTHON YOU NEED:
#    · One tenth of something is `* 0.1`. Multiply, do not divide.
#      Dividing by 0.1 makes a number ten times BIGGER, which is the opposite.
#    · Per million still applies, so `/ PER_MILLION` is still in there.
#    · One line, starting with `return`, no `=` in it.
#
#  SHAPE TO COPY: look at `input_cost` inside `cost` above. Yours is that line
#  with one extra thing multiplied in.
#
#  A worked number so you can check yourself: 1,000,000 cached tokens at a rate
#  of 3.0 should come out as 0.30.
#
# -----------------------------------------------------------------------------

def cache_cost(cached_in, rate_in):
    # Delete the word `pass` and write your line here. Start it with 4 spaces.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    pass

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 2 of 2  (the real one) ▼▼▼
# =============================================================================
#
#  Now the full bill: fresh input, output, AND cached input, all added together.
#
#  THREE things are being paid for. So, following the shopping bill shape:
#  THREE named lines, then ONE return that adds all three names together.
#
#  THE PYTHON YOU NEED:
#    · `cached_in=0` in the brackets below is a DEFAULT. It means someone can
#      call this function without mentioning caching at all, and `cached_in`
#      will quietly be 0. You do not have to do anything to make that work —
#      it already does. But it is why one of the checks calls this with only
#      four numbers instead of five.
#    · You already wrote the cached line in Task 1. You may call `cache_cost(...)`
#      here instead of writing that arithmetic out again, exactly like
#      `daily_cost` calls `cost`.
#    · Four spaces at the start of every line.
#
#  WORKED NUMBERS to check yourself against:
#    1,000,000 fresh input at rate 3.0                     -> 3.00
#    1,000,000 output at rate 15.0                         -> 15.00
#    1,000,000 cached at rate 3.0                          -> 0.30
#    all three together                                    -> 18.30
#
# -----------------------------------------------------------------------------

def cost_with_cache(tokens_in, tokens_out, rate_in, rate_out, cached_in=0):
    # Delete `pass`. Write your three named lines, then your return.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    pass

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▲▲▲  END OF YOUR TURN  ▲▲▲
# =============================================================================


# -----------------------------------------------------------------------------
#  THE CHECKS  (mine. They tell you when you are done.)
# -----------------------------------------------------------------------------

def check(label, got, want):
    ok = got is not None and abs(got - want) < 0.0000001
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        wanted {want}, got {got}")
    return ok


def main():
    print("\nMy code (already working):")
    mine = [
        check("reading 2,000 tokens",           cost(2_000, 0, 3.0, 15.0), 0.006),
        check("writing 500 tokens costs MORE",  cost(0, 500, 3.0, 15.0), 0.0075),
        check("100k users x 10 calls a day",    daily_cost(100_000, 10, 2_000, 0, 3.0, 15.0), 6_000.0),
    ]

    print("\nTask 1 — cache_cost:")
    t1 = [
        check("1M cached tokens at rate 3",     cache_cost(1_000_000, 3.0), 0.30),
        check("nothing cached costs nothing",   cache_cost(0, 3.0), 0.0),
    ]

    print("\nTask 2 — cost_with_cache:")
    t2 = [
        check("fresh input only",               cost_with_cache(1_000_000, 0, 3.0, 15.0), 3.0),
        check("cached only",                    cost_with_cache(0, 0, 3.0, 15.0, cached_in=1_000_000), 0.30),
        check("fresh + cached",                 cost_with_cache(1_000_000, 0, 3.0, 15.0, cached_in=1_000_000), 3.30),
        check("all three together",             cost_with_cache(1_000_000, 1_000_000, 3.0, 15.0, cached_in=1_000_000), 18.30),
    ]

    done = sum(1 for r in mine + t1 + t2 if r)
    total = len(mine) + len(t1) + len(t2)
    print(f"\n{done} of {total} passing.")
    if all(t1) and not all(t2):
        print("Task 1 done. Now Task 2.\n")
    elif done == total:
        print("Both done. Tell me and I'll review it.\n")
    else:
        print("Start with Task 1, it is one line. /faiz-hint for a nudge.\n")


main()
