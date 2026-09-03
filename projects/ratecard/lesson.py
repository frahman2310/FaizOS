# =============================================================================
#  FAIZOS  ·  LESSON 2 of 20  ·  The AI Gateway
#  Run me:   uv run --no-project python lesson.py
# =============================================================================
#
#  Everything below was taught in chat. This file is your reference and your
#  build. Scroll to YOUR TURN when you are ready.
#
#  THE QUESTION  (Anthropic / Google, Applied AI onsite)
#  -----------------------------------------------------
#      "You are spending $47,000 a month on a single frontier model. Design an
#       AI Gateway that routes between three providers with auto-fallback, and
#       cut that bill by 40% without users noticing."
#
#  Real routing systems report 30 to 55% savings. 40% is the honest end.
#
#  THE ANSWER, IN STEPS
#  --------------------
#  Step 1: Hold every price in one place.            >> YOU BUILD THIS TODAY
#  Step 2: Price the real workload, not the list.    >> YOU BUILD THIS TODAY
#  Step 3: Route to the cheapest that can cope.      >> YOU BUILD THIS TODAY
#  Step 4: Circuit-break per provider on failure.    >> Lesson 4
#  Step 5: Cache the repeated prefix.                >> built in Lesson 1
#
#  THE POINT
#  ---------
#  A model can be cheap on input and dear on output. Which one wins depends on
#  the SHAPE of your traffic, so you cannot read the answer off the price list.
#  You price your actual workload on each model and compare. That is routing.
#
#  THE PYTHON, IN ONE PLACE
#  ------------------------
#    dict      a lookup table.  prices = {"apple": 0.30}   prices["apple"]
#    list      things in a row.  models = ["haiku", "opus"]
#    for       repeat over each item.  `for m in MODELS:`  COLON, then indent.
#    None      "nothing here yet". Not zero. Zero is a value.
#    is None   asks "is this still empty?"
#    or        true when EITHER side is true.
#
#    [ ] LOOKS UP        RATES["haiku"]
#    ( ) RUNS            cost_for("haiku", 2000, 200)
#
#  KEEP-THE-BEST-SO-FAR, the shape you will write:
#
#      def longest_word(words):
#          best_word   = None
#          best_length = None
#          for word in words:
#              this_length = len(word)
#              if best_length is None or this_length > best_length:
#                  best_word   = word
#                  best_length = this_length
#          return best_word            # OUTSIDE the loop
#
#  Two trackers starting at None, one `if` joining two questions with `or`, and
#  a return outside the loop. Yours is that shape looking for smallest, not
#  biggest, and pricing each option instead of measuring its length.
#
# =============================================================================


# -----------------------------------------------------------------------------
#  MY CODE  (working)
# -----------------------------------------------------------------------------

PER_MILLION = 1_000_000

# Step 1: every price in one place. A dict whose values are themselves dicts.
RATES = {
    "flash":  {"in": 0.50, "out": 30.0},   # cheap to read, expensive to write
    "haiku":  {"in": 1.00, "out": 5.0},
    "sonnet": {"in": 2.00, "out": 10.0},
    "opus":   {"in": 5.00, "out": 25.0},
}

MODELS = ["flash", "haiku", "sonnet", "opus"]


def price_of(model, side):
    # One rate. side is "in" or "out". Two lookups, chained left to right.
    return RATES[model][side]


def cost_for(model, tokens_in, tokens_out):
    # Step 2: what ONE call costs on a given model. Lesson 1's arithmetic,
    # with the rates fetched from the dict rather than handed in.
    rate_in = price_of(model, "in")
    rate_out = price_of(model, "out")
    input_cost = tokens_in * rate_in / PER_MILLION
    output_cost = tokens_out * rate_out / PER_MILLION
    return input_cost + output_cost


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 1 of 2  (one line) ▼▼▼
# =============================================================================
#
#  How many times dearer is one model than another for the SAME work? This is
#  the number that says whether routing is worth building at all.
#
#  YOUR RULES:
#   1. One line, starting with `return`, no `=` in it.
#   2. Use `cost_for(...)` twice, once per model. ROUND brackets: you are
#      running it, not looking something up.
#   3. The two model names arrive in the brackets below. Do not type "opus"
#      or "haiku" into the line; the checks ask about three different pairs.
#   4. `a / b` is a divided by b. The dearer one goes on top.
#
#  CHECK YOURSELF: opus against haiku on 1,000,000 input tokens and no output
#  should give 5.0.
#
# -----------------------------------------------------------------------------

def how_much_dearer(pricey_model, cheap_model, tokens_in, tokens_out):
    # Delete `pass`. Write your one line. Four spaces at the start.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    return cost_for(pricey_model, tokens_in, tokens_out) / cost_for(cheap_model, tokens_in, tokens_out)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 2 of 2  (the loop) ▼▼▼
# =============================================================================
#
#  Step 3: walk every model, price this workload on each, and return the name
#  of the cheapest.
#
#  YOUR RULES:
#   1. Copy the SHAPE of `longest_word` at the top of this file.
#   2. Two trackers, both starting at None. One holds the winning NAME, one
#      holds its cost.
#   3. Loop over MODELS. Colon at the end of the `for` line, four more spaces
#      for everything inside it.
#   4. Inside the loop, price this model with `cost_for(...)`. It needs three
#      things: which model, how many tokens in, how many out. Two of those
#      arrive in the brackets below; the third is the loop variable.
#   5. The `if` asks two questions joined by `or`: is the cost tracker still
#      empty, or is this one cheaper than it. Cheaper is `<`.
#   6. `return` the winning NAME, and put it OUTSIDE the loop, lined up with
#      the two trackers.
#
#  WHY None AND NOT 0: nothing costs less than zero, so a tracker starting at
#  0 rejects every model and returns nothing at all. No error, just an empty
#  answer.
#
#  CHECK YOURSELF: with this rate card, a read-heavy workload and a write-heavy
#  workload do not pick the same model. That is the whole point of the lesson.
#
# -----------------------------------------------------------------------------

def cheapest_model(tokens_in, tokens_out):
    # Delete `pass`. Write the loop. Follow the shape above.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    best_model   = None
    bestmodel_cost = None
    for model in MODELS:
        this_cost = cost_for(model, tokens_in, tokens_out)
        if best_model is None or this_cost < bestmodel_cost:
            best_model   = model
            bestmodel_cost = this_cost
    return best_model

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▲▲▲  END OF YOUR TURN  ▲▲▲
# =============================================================================


def check(label, got, want):
    ok = got == want if isinstance(want, str) else (got is not None and abs(got - want) < 1e-9)
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        wanted {want}, got {got}")
    return ok


def progress_bar():
    import os, sqlite3
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "faizos-core", "data", "faiz.db")
    try:
        con = sqlite3.connect(f"file:{os.path.abspath(p)}?mode=ro", uri=True)
        one = lambda q: con.execute(q).fetchone()[0]
        L = min(one("SELECT COUNT(*) FROM builds WHERE state IN ('done','provisional','unlocked')"), 20)
        pd = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE t.kind IN ('production','ship') AND s.mastery>0")
        pa = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE t.kind IN ('production','ship')")
        md = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE (t.kind='ml' OR t.kind IS NULL) AND s.mastery>0")
        ma = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id WHERE (t.kind='ml' OR t.kind IS NULL)")
        con.close()
    except Exception:
        return
    b = lambda d, t, w=20: "#" * (0 if t == 0 else round(d/t*w)) + "." * (w - (0 if t == 0 else round(d/t*w)))
    pc = lambda a, c: 0 if c == 0 else round(a/c*100)
    print("\n" + "=" * 70)
    print("  WHERE YOU ACTUALLY ARE")
    print("=" * 70)
    print(f"  Lessons     {b(L,20)}  {L}/20     {pc(L,20)}%")
    print(f"  Production  {b(pd,pa)}  {pd}/{pa}     {pc(pd,pa)}%   <- the critical path")
    print(f"  ML (banked) {b(md,ma)}  {md}/{ma}   {pc(md,ma)}%   understood, not yet evidenced")
    print("=" * 70)


def main():
    print("\nMy code (already working):")
    mine = [
        check("sonnet's output rate",     price_of("sonnet", "out"), 10.0),
        check("one RAG call on flash",    cost_for("flash", 20_000, 200), 0.016),
        check("one RAG call on haiku",    cost_for("haiku", 20_000, 200), 0.021),
    ]

    print("\nTask 1 — how_much_dearer:")
    t1 = [
        check("opus vs haiku on input",   how_much_dearer("opus", "haiku", 1_000_000, 0), 5.0),
        check("sonnet vs haiku on input", how_much_dearer("sonnet", "haiku", 1_000_000, 0), 2.0),
        check("opus vs sonnet on output", how_much_dearer("opus", "sonnet", 0, 1_000_000), 2.5),
    ]

    print("\nTask 2 — cheapest_model:")
    t2 = [
        check("read-heavy  (20k in, 200 out)",  cheapest_model(20_000, 200), "flash"),
        check("write-heavy (500 in, 2k out)",   cheapest_model(500, 2_000), "haiku"),
        check("balanced    (1k in, 1k out)",    cheapest_model(1_000, 1_000), "haiku"),
    ]

    done = sum(1 for r in mine + t1 + t2 if r)
    total = len(mine) + len(t1) + len(t2)
    print(f"\n{done} of {total} passing.")

    if done == total:
        print("\n--- THE NUMBER, against the $47,000 question ---")
        spend = 47_000
        # 70% of traffic is read-heavy, 30% write-heavy. Route each to its winner.
        base = 0.7 * cost_for("opus", 20_000, 200) + 0.3 * cost_for("opus", 500, 2_000)
        routed = 0.7 * cost_for(cheapest_model(20_000, 200), 20_000, 200) \
               + 0.3 * cost_for(cheapest_model(500, 2_000), 500, 2_000)
        saved = (base - routed) / base
        print(f"  All traffic on opus         : ${spend:,.0f}/month")
        print(f"  Routed to the cheapest      : ${spend*(1-saved):,.0f}/month")
        print(f"  Saved                       : {saved:.0%}   target was 40%  -> {'MET' if saved >= 0.40 else 'NOT MET'}")
        progress_bar()
        print("\nBoth done. Tell me and I'll review it.\n")
    elif all(t1):
        print("Task 1 done. Now the loop.\n")
    else:
        print("Start with Task 1, it is one line. /faiz-hint for a nudge.\n")


main()
