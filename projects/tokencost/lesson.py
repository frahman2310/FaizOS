# =============================================================================
#  FAIZOS  ·  LESSON 1 of 20  ·  What an AI feature costs
#  Run me:   uv run python lesson.py
# =============================================================================
#
#  Read this file top to bottom. Everything is taught before anything is asked.
#  Your part is at the bottom, clearly marked. Nothing before it is a test.
#
# =============================================================================
#  THE QUESTION
# =============================================================================
#
#  Asked at: Google (L5 AI Engineer, onsite)
#
#      "Design a prompt caching system for 1B daily LLM API calls.
#       Optimise for cost and latency."
#
#  One billion calls a day. That number is the whole question. Without it you
#  could answer anything; with it, most answers are wrong immediately, because
#  at a billion calls a tenth of a cent each is a million dollars a day.
#
#  You cannot design that system until you can price a single call. That is
#  today. Lesson 18 builds the cache itself.
#
#
#  THE ANSWER, IN STEPS
#  --------------------
#  Each step is a DECISION, and each one says what it rules out.
#
#  Step 1: Price one call before you optimise anything.
#      You cannot claim a saving without a baseline. This rules out every
#      answer that starts with "use a cache" — cheaper than what?
#      >> YOU BUILD THIS TODAY.
#
#  Step 2: Price input and output separately.
#      They are charged at different rates, and which one dominates flips
#      depending on the app. This rules out any single "cost per call" figure.
#      >> YOU BUILD THIS TODAY.
#
#  Step 3: Charge repeated input at the cached rate.
#      Providers charge about a tenth for input they have seen recently.
#      At 1B calls this is the single biggest lever there is.
#      >> YOU BUILD THIS TODAY.
#
#  Step 4: Multiply by the traffic to get the real bill.
#      A per-call figure means nothing to Finance. Dollars per day does.
#      >> YOU BUILD THIS TODAY.
#
#  Step 5: Then design the cache itself, keyed on the repeated prefix.
#      >> Lesson 18.
#
# =============================================================================
#  PART 1 · THE CONCEPT
# =============================================================================
#
#  A model does not read letters or words. It reads TOKENS: chunks of text of
#  about 4 characters. "Hello world" is roughly 3 tokens. A page is about 500.
#
#  Every call to a model has a bill with up to THREE lines on it:
#
#      1. INPUT   the tokens you send it       full price
#      2. OUTPUT  the tokens it sends back     about FIVE TIMES the input price
#      3. CACHED  input it has seen recently   ONE TENTH of the input price
#
#  Why output costs more: the model generates output one token at a time, which
#  is slow and serial. Input it can read all at once. You are paying for the
#  hard part.
#
#  A consequence worth holding on to, because it is not obvious:
#
#      reading 2,000 tokens   costs $0.006
#      writing   500 tokens   costs $0.0075
#
#  A quarter as many tokens, and it still costs more. Chatty models are
#  expensive models, and that is why a RAG app and a chatbot need completely
#  different optimisations even on the same model.
#
#
#  PRICES ARE QUOTED PER MILLION TOKENS
#  -------------------------------------
#  The real price of one token is $0.000003. Nobody can read that without
#  counting zeros, so every provider quotes "$3 per million" instead.
#
#  Which means your arithmetic always has a division by a million in it:
#
#      2,000 tokens  x  $3  =  6,000        <- nonsense, that is not dollars
#      6,000  /  1,000,000  =  $0.006       <- correct
#
#      PER MILLION MEANS THE MILLION GOES ON THE BOTTOM.
#
#  Forget the division and your answer is a million times too big. Say the rule
#  to yourself once now; it is the single most common mistake in this material.
#
# =============================================================================
#  PART 2 · THE PYTHON YOU NEED  (taught from zero — no prior knowledge assumed)
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
#       final = price + tax          <- `final` now means 12
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
#  A FUNCTION is a named recipe that takes inputs.
#  ------------------------------------------------
#       def add_tax(price, rate):        <- `def`, a name, inputs in brackets, COLON
#           tax = price * rate           <- indented 4 spaces. This is the body.
#           return price + tax           <- still indented. This is the answer.
#
#  The names in the brackets (`price`, `rate`) are the ONLY names that exist
#  inside that function. Using any other name is an error, and it is the single
#  most common bug for someone starting out.
#
#
#  A DEFAULT ARGUMENT makes an input optional.
#  --------------------------------------------
#       def add_tax(price, rate=0.2):    <- if nobody says `rate`, it is 0.2
#           ...
#
#       add_tax(100)          -> uses rate 0.2
#       add_tax(100, 0.05)    -> uses rate 0.05
#
#  Defaults go AFTER all the normal inputs, never before. This matters today,
#  because caching has to be optional: code written before caching existed must
#  keep working untouched.
#
#
#  INDENTATION
#  ------------
#  Every line inside a function starts with exactly 4 spaces, lined up under
#  each other. Python uses those spaces to know what belongs to the function.
#  Not 2, not 3. Four.
#
# =============================================================================
#  PART 3 · MY CODE, LINE BY LINE
# =============================================================================

PER_MILLION = 1_000_000
#  A name for a number. Written once, so it can never be mistyped as 100_000
#  somewhere later. The underscores are invisible to Python: 1_000_000 IS
#  1000000. They exist purely so your eye can count the zeros.


def cost(tokens_in, tokens_out, rate_in, rate_out):
    #  Step 1 and 2 of the answer, in code: what does ONE call cost?
    #
    #  The four inputs, spelled out:
    #      tokens_in    how many tokens I sent          e.g. 2000
    #      tokens_out   how many came back              e.g. 500
    #      rate_in      $ per MILLION input tokens      e.g. 3.0
    #      rate_out     $ per MILLION output tokens     e.g. 15.0

    input_cost = tokens_in * rate_in / PER_MILLION
    #  A KIND 1 line: name on the left, work on the right.
    #  Read the work left to right: take the token count, multiply by the price
    #  of a million, then divide by a million to scale down to what you used.
    #      2000 * 3.0 = 6000,  then / 1_000_000 = 0.006

    output_cost = tokens_out * rate_out / PER_MILLION
    #  Identical shape, output numbers instead. They are worked out SEPARATELY
    #  because they are priced separately. That is step 2 of the answer.

    return input_cost + output_cost
    #  A KIND 2 line. The two names, added. No `=` on a return line.


def daily_cost(users, calls_per_user, tokens_in, tokens_out, rate_in, rate_out):
    #  Step 4 of the answer: what does the WHOLE PRODUCT cost per day?

    calls_per_day = users * calls_per_user
    #  100,000 users each sending 10 messages = 1,000,000 calls a day.

    return calls_per_day * cost(tokens_in, tokens_out, rate_in, rate_out)
    #  Rather than redo the arithmetic, this CALLS the function above and
    #  multiplies its answer. Writing `cost(...)` with ROUND brackets RUNS it.
    #  The price of one call is now defined in exactly one place, so if it is
    #  ever wrong, it is wrong in only one place.


# =============================================================================
#  PART 4 · A WORKED EXAMPLE OF EXACTLY WHAT YOU ARE ABOUT TO WRITE
# =============================================================================
#
#  You are about to add a THIRD component to a bill that currently has two, and
#  make it optional. Here is that exact shape, fully written out, in a domain
#  that has nothing to do with tokens. Read it, then map it across.
#
#  A shop charges for items and for delivery. Later, they add an optional
#  gift-wrap fee that is HALF the item price.
#
#      def shop_bill(items, delivery, item_price, delivery_price, wrapped=0):
#          item_cost     = items    * item_price
#          delivery_cost = delivery * delivery_price
#          wrap_cost     = wrapped  * item_price * 0.5
#          return item_cost + delivery_cost + wrap_cost
#
#  Four things to notice, because all four apply to your task:
#
#   1. THREE named lines, then ONE return that adds all three. Each line does
#      one small job. This is the shape.
#   2. `wrapped=0` is the DEFAULT. Old code that calls shop_bill(2, 1, 5, 3)
#      still works, and wrap_cost comes out as 0 * anything = 0. Nothing breaks.
#   3. The wrap line REUSES `item_price` and multiplies by 0.5, because the fee
#      is defined in terms of a price that is already there. Yours is the same:
#      the cached rate is defined in terms of the input rate.
#   4. Every name used on the right of an `=` appears in the brackets on the
#      `def` line. Nothing is invented.
#
#  Now map it: items -> fresh input tokens, delivery -> output tokens,
#  wrapped -> cached tokens, and 0.5 -> a tenth.
#
# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 1 of 2  (one line) ▼▼▼
# =============================================================================
#
#  Write the price of cached tokens on their own.
#
#  WHAT IT MUST DO: cached tokens are charged at ONE TENTH of the input rate.
#
#  YOUR RULES:
#   1. One line, starting with `return`, with no `=` in it.
#   2. A tenth is `* 0.1`. Multiply, do not divide. Dividing by 0.1 makes a
#      number ten times BIGGER, which is the opposite of what you want.
#   3. Per million still applies, so `/ PER_MILLION` is in there too.
#   4. The only names you may use are the ones in the brackets below.
#
#  SHAPE TO COPY: the `wrap_cost` line from Part 4, and the `input_cost` line
#  from Part 3. Yours is those two combined, with `return` at the front.
#
#  CHECK YOURSELF: 1,000,000 cached tokens at a rate of 3.0 should give 0.30.
#
# -----------------------------------------------------------------------------

def cache_cost(cached_in, rate_in):
    # Delete `pass` and write your line here. Start it with 4 spaces.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    pass

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 2 of 2  (the real one) ▼▼▼
# =============================================================================
#
#  Now the full bill: fresh input, output, AND cached input, added together.
#  This is step 3 of the interview answer, and it is the line that makes the
#  1B-calls-a-day question answerable.
#
#  THREE things are being paid for. So, exactly like `shop_bill` in Part 4:
#  THREE named lines, then ONE return that adds all three names together.
#
#  YOUR RULES:
#   1. `cached_in=0` in the brackets below is already written for you. It is the
#      DEFAULT from Part 2, and it is why one of the checks calls this with only
#      four numbers. You do not need to do anything to make that work.
#   2. Fresh input, output and cached input all ADD together.
#   3. You may CALL `cache_cost(...)` here rather than writing that arithmetic
#      out again, exactly as `daily_cost` calls `cost`. Round brackets.
#   4. Four spaces at the start of every line.
#
#  CHECK YOURSELF, one number at a time:
#      1,000,000 fresh input at rate 3.0    -> 3.00
#      1,000,000 output at rate 15.0        -> 15.00
#      1,000,000 cached at rate 3.0         -> 0.30
#      all three together                   -> 18.30
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


def check(label, got, want):
    ok = got is not None and abs(got - want) < 1e-9
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        wanted {want}, got {got}")
    return ok


def progress_bar():
    """Read the real FaizOS database. Nothing here is estimated."""
    import os, sqlite3
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "faizos-core", "data", "faiz.db")
    try:
        con = sqlite3.connect(f"file:{os.path.abspath(p)}?mode=ro", uri=True)
        one = lambda q: con.execute(q).fetchone()[0]
        lessons = min(one("SELECT COUNT(*) FROM builds WHERE state IN ('done','provisional','unlocked')"), 20)
        pd = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE t.kind IN ('production','ship') AND s.mastery>0")
        pa = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE t.kind IN ('production','ship')")
        md = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE (t.kind='ml' OR t.kind IS NULL) AND s.mastery>0")
        ma = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE (t.kind='ml' OR t.kind IS NULL)")
        con.close()
    except Exception:
        return
    bar = lambda d, t, w=20: "#" * (0 if t == 0 else round(d / t * w)) + "." * (w - (0 if t == 0 else round(d / t * w)))
    pct = lambda a, b: 0 if b == 0 else round(a / b * 100)
    print("\n" + "=" * 70)
    print("  WHERE YOU ACTUALLY ARE")
    print("=" * 70)
    print(f"  Lessons     {bar(lessons,20)}  {lessons}/20     {pct(lessons,20)}%")
    print(f"  Production  {bar(pd,pa)}  {pd}/{pa}     {pct(pd,pa)}%   <- the critical path")
    print(f"  ML (banked) {bar(md,ma)}  {md}/{ma}   {pct(md,ma)}%   understood, not yet evidenced")
    print("=" * 70)


def main():
    print("\nMy code (already working):")
    mine = [
        check("reading 2,000 tokens",          cost(2_000, 0, 3.0, 15.0), 0.006),
        check("writing 500 costs MORE",        cost(0, 500, 3.0, 15.0), 0.0075),
        check("100k users x 10 calls a day",   daily_cost(100_000, 10, 2_000, 0, 3.0, 15.0), 6_000.0),
    ]

    print("\nTask 1 — cache_cost:")
    t1 = [
        check("1M cached tokens at rate 3",    cache_cost(1_000_000, 3.0), 0.30),
        check("nothing cached costs nothing",  cache_cost(0, 3.0), 0.0),
    ]

    print("\nTask 2 — cost_with_cache:")
    t2 = [
        check("fresh input only",              cost_with_cache(1_000_000, 0, 3.0, 15.0), 3.0),
        check("cached only",                   cost_with_cache(0, 0, 3.0, 15.0, cached_in=1_000_000), 0.30),
        check("fresh + cached",                cost_with_cache(1_000_000, 0, 3.0, 15.0, cached_in=1_000_000), 3.30),
        check("all three together",            cost_with_cache(1_000_000, 1_000_000, 3.0, 15.0, cached_in=1_000_000), 18.30),
    ]

    done = sum(1 for r in mine + t1 + t2 if r)
    total = len(mine) + len(t1) + len(t2)
    print(f"\n{done} of {total} passing.")

    if done == total:
        print("\n--- THE NUMBER, against the 1 BILLION CALLS question ---")
        calls = 1_000_000_000
        no_cache = calls * cost(2_000, 200, 3.0, 15.0)
        with_cache = calls * cost_with_cache(200, 200, 3.0, 15.0, cached_in=1_800)
        print(f"  1B calls, 2,000 in / 200 out, no caching : ${no_cache:>14,.0f} per day")
        print(f"  Same traffic, 90% of input cached        : ${with_cache:>14,.0f} per day")
        print(f"  Saved                                    : ${no_cache-with_cache:>14,.0f} per day"
              f"  ({(no_cache-with_cache)/no_cache:.0%})")
        print("\n  That is the answer to the Google question, and you can now derive it.")
        progress_bar()
        print("\nBoth done. Tell me and I'll review it.\n")
    elif all(t1):
        print("Task 1 done. Now Task 2.\n")
    else:
        print("Start with Task 1. Re-read Part 4 first. /faiz-hint if stuck.\n")


main()
