# =============================================================================
#  FAIZOS LESSON 2  ·  The AI Gateway
#  Run me:   uv run --no-project python lesson.py
# =============================================================================
#
#  THE QUESTION
#  ------------
#  Asked at: Anthropic / Google (Applied AI onsite)
#
#      "You are spending $47,000 a month on a single frontier model.
#       Design an AI Gateway that routes between three providers with
#       auto-fallback, and cut that bill by 40% without users noticing."
#
#  Notice what makes it answerable: the NUMBER. $47,000 and 40%. Without those
#  it is "design a gateway" and any answer is as good as any other. With them,
#  most designs are eliminated immediately, and the ones left can be argued for.
#
#  That is the whole shape of a systems interview. A constraint with a number,
#  and a sequence of decisions that the constraint forces.
#
#
#  THE STEPS  (this is the answer you should be able to say out loud)
#  ------------------------------------------------------------------
#
#  Step 1: Know the price of every model before you route anything.
#      You cannot choose the cheaper option if you cannot price the options.
#      This rules out any design that hardcodes one provider. You need a
#      lookup table of prices, held in one place, that the router reads.
#      >> You build this today.
#
#  Step 2: Price the actual workload, not the sticker price.
#      Model A can be cheaper per input token and dearer per output token.
#      Which one wins depends entirely on YOUR traffic shape. This rules out
#      choosing by reading the price list.
#      >> You build this today.
#
#  Step 3: Route each request to the cheapest model that can handle it.
#      Run the cheap one first, escalate only on a signal (a failed schema
#      check, a low judge score, a tool error). Because the cheap model is
#      often 5 to 10 times cheaper, you can afford to throw its answer away
#      40% of the time and still win.
#      >> Lesson 8 gives you the escalation signal. Today you build the
#         "which is cheapest" half.
#
#  Step 4: Fall back when a provider fails, without falling over.
#      Circuit breaker per provider and model. Trip on 5xx and overload,
#      never on a rate limit, which means slow down rather than fail over.
#      >> Lesson 4.
#
#  Step 5: Cache the repeated prefix.
#      Providers charge a tenth for input they have seen recently. On a
#      support bot resending the same manual, that alone is most of the 40%.
#      >> You already built this in Lesson 1.
#
#  Real routing systems report 30 to 55% savings, not the 85% the papers
#  claim. Your target of 40% is deliberately at the honest end.
#
# =============================================================================
#  PART 1 · THE PYTHON: THREE NEW THINGS
# =============================================================================
#
#  NEW THING 1 — A DICT is a lookup table.
#  ----------------------------------------
#  A dict holds pairs: a KEY, and the VALUE that key points at. Like a contacts
#  app: you look up "Ammar" and get back a phone number.
#
#       prices = {"apple": 0.30, "bread": 1.10, "milk": 0.90}
#
#  Curly braces { } around the whole thing. Each pair is  key: value.
#  Commas between pairs.
#
#  To get a value out, you use SQUARE brackets:
#
#       prices["bread"]        ->  1.10
#
#  ****  THIS IS THE RULE YOU HAVE BROKEN FIVE TIMES  ****
#
#       SQUARE brackets [ ]  LOOK SOMETHING UP.       prices["bread"]
#       ROUND brackets  ( )  RUN A FUNCTION.          cost_for("haiku", 2000, 0)
#
#  Finding someone in your contacts is not the same as phoning them. Looking a
#  price up is not the same as running a calculation. Different brackets.
#
#
#  NEW THING 2 — A LIST is things in a row.
#  -----------------------------------------
#       models = ["haiku", "sonnet", "opus"]
#
#  SQUARE brackets around the whole thing, commas between items.
#  A dict is looked up by name. A list is just an ordered row of things.
#
#
#  NEW THING 3 — A FOR LOOP does the same work to every item.
#  -----------------------------------------------------------
#       for name in models:
#           print(name)
#
#  Read it as English: "for each name in models, do the indented part."
#  It runs three times, and `name` is "haiku", then "sonnet", then "opus".
#
#  Two things to get right:
#    · the COLON at the end of the `for` line. Forget it and Python stops.
#    · the indented block underneath is what repeats. Four more spaces.
#
#  The word `name` is yours to choose. `for x in models:` works identically.
#  It is just the label for "whichever one we are on right now".
#
#
#  PUTTING THEM TOGETHER — the pattern you will write today
#  ---------------------------------------------------------
#  Walk a list, look each item up in a dict, keep a running answer:
#
#       total = 0                          # start empty
#       for item in shopping_list:         # visit each item
#           total = total + prices[item]   # look it up, add it on
#       return total
#
#  Line by line:
#    · `total = 0` makes a box to accumulate into. It must exist BEFORE the loop.
#    · `prices[item]` looks up whichever item we are on. Square brackets.
#    · `total = total + ...` means "the new total is the old total plus this".
#      The old value is on the right, the new label on the left. Same rule as
#      lesson 1: work on the right, name on the left.
#    · `return total` is OUTSIDE the loop. Return inside a loop stops it dead
#      after one pass.
#
# =============================================================================


# -----------------------------------------------------------------------------
#  PART 2 · MY CODE  (working. Read it, it is the shape you will copy.)
# -----------------------------------------------------------------------------

PER_MILLION = 1_000_000

# Step 1 from the answer above, in code: every price in ONE place.
# A dict of dicts. The outer keys are model names. Each value is ITSELF a dict
# holding that model's two prices, in dollars per million tokens.
RATES = {
    "haiku":  {"in": 1.0, "out": 5.0},
    "sonnet": {"in": 2.0, "out": 10.0},
    "opus":   {"in": 5.0, "out": 25.0},
}

# A plain list. Just the three names, in a row, so we can walk them.
MODELS = ["haiku", "sonnet", "opus"]


def price_of(model, side):
    # Look up one number: a model's price for one side of the bill.
    #   model -> "sonnet"      side -> "in" or "out"
    #
    # TWO lookups, chained. Read it left to right:
    #   RATES["sonnet"]          gives  {"in": 2.0, "out": 10.0}
    #   then ["in"] on THAT      gives  2.0
    return RATES[model][side]


def cost_for(model, tokens_in, tokens_out):
    # Step 2 from the answer: price the ACTUAL workload on a given model.
    # Lesson 1's arithmetic, with the rates fetched from the dict.

    rate_in = price_of(model, "in")
    # ROUND brackets here, because price_of is a function and we are RUNNING it.

    rate_out = price_of(model, "out")

    input_cost = tokens_in * rate_in / PER_MILLION
    output_cost = tokens_out * rate_out / PER_MILLION
    return input_cost + output_cost


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 1 of 2  (one line) ▼▼▼
# =============================================================================
#
#  Write a function that says how much MORE the expensive model costs than the
#  cheap one, for the same piece of work. This is the number that tells you
#  whether routing is even worth building.
#
#  WHAT IT MUST DO: return the cost on `pricey_model` divided by the cost on
#  `cheap_model`. If one is twice the price of the other, this returns 2.0.
#
#  THE PYTHON YOU NEED:
#    · `cost_for(...)` is a FUNCTION. ROUND brackets. You are running it twice,
#      once for each model.
#    · The two model names arrive in the brackets as `pricey_model` and
#      `cheap_model`. They are labels for "whichever two were asked about this
#      time". Typing "opus" directly breaks the check that asks about sonnet.
#    · Division is `/`. The thing on top goes first: `a / b` is a divided by b.
#    · One line, starting with `return`, no `=` in it.
#
#  SHAPE TO COPY: look at `return input_cost + output_cost` in my code above.
#  Yours is that shape, with two function CALLS instead of two names, and a
#  `/` instead of a `+`.
#
#  WORKED NUMBER: opus vs haiku on 1,000,000 input tokens and no output is
#  5.00 / 1.00, so the answer is 5.0.
#
# -----------------------------------------------------------------------------

def how_much_dearer(pricey_model, cheap_model, tokens_in, tokens_out):
    # Delete `pass`. Write your one line. Four spaces at the start.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # Delete `pass`. Write your one line. Four spaces at the start.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    return how_much_dearer ("opus" / "haiku")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 2 of 2  (the loop) ▼▼▼
# =============================================================================
#
#  Step 3 from the answer, in code: find the CHEAPEST model for a given piece
#  of work, and return its name.
#
#  Some models are cheaper on input and dearer on output, so you cannot answer
#  this by reading the price list. You have to price the actual workload on each
#  one and compare. That is the routing decision, and it is worth 30 to 55%.
#
#  THE SHAPE, in the same form as the shopping-list pattern in Part 1:
#
#       best_name = None                 <- nothing chosen yet
#       best_cost = None                 <- no price seen yet
#       for model in MODELS:             <- visit each model. Colon.
#           this_cost = ...              <- what it costs on THIS model
#           if ...:                      <- is it better than the best so far?
#               best_name = model        <- if so, remember it
#               best_cost = this_cost
#       return best_name                 <- OUTSIDE the loop
#
#  A TRACE, so you can see what the loop actually does. cheapest_model(1_000_000, 0):
#
#    before      best_name = None   best_cost = None
#    pass 1      model is "haiku"   costs 1.00   best_cost empty  -> TAKE IT
#    pass 2      model is "sonnet"  costs 2.00   2.00 < 1.00? no  -> skip
#    pass 3      model is "opus"    costs 5.00   5.00 < 1.00? no  -> skip
#    after       return "haiku"
#
#  The middle column IS your two blank lines. "costs" is line 1. "empty, or
#  cheaper?" is line 2.
#
#  THE PYTHON YOU NEED:
#    · `None` means "nothing here yet". It is not zero. Zero is a price; None is
#      the absence of one. If you start best_cost at 0, nothing is ever cheaper
#      than it and your loop picks nobody.
#    · `if` asks a yes/no question and runs the indented block when the answer is
#      yes. It needs a COLON, exactly like `for`.
#    · `is None` is how you ask "is this still empty?"  ->  `if best_cost is None:`
#    · `<` means less than. `a < b` is True when a is smaller.
#    · `or` joins two yes/no questions and is True when EITHER is true.
#      You need it: this model wins if nothing has been picked yet, OR it is
#      cheaper than the best so far.
#    · Everything inside the loop is indented one step further than the `for`.
#      Everything inside the `if` is indented one step further again.
#
#  WORKED NUMBERS to check yourself against:
#    · pure input work, no output      -> haiku wins (it is cheapest on input)
#    · pure output work, no input      -> haiku wins again (cheapest on output)
#    · zero tokens of everything       -> haiku, because it is first and nothing beats it
#
# -----------------------------------------------------------------------------

def cheapest_model(tokens_in, tokens_out):
    # Delete `pass`. Write the loop. Follow the shape above.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
    # Delete `pass`. Write the loop. Follow the shape above.
    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

    best_name = None
    best_cost = None
    for model in MODELS: 
      this_cost = 
      if :
        best_name = model
        best_cost = this_cost
    return best_name

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▲▲▲  END OF YOUR TURN  ▲▲▲
# =============================================================================


# -----------------------------------------------------------------------------
#  THE CHECKS, AND THE NUMBER  (mine)
# -----------------------------------------------------------------------------

def check(label, got, want):
    ok = got == want if isinstance(want, str) else (got is not None and abs(got - want) < 1e-9)
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        wanted {want}, got {got}")
    return ok


def progress_bar():
    """Read the real FaizOS database and print where you actually are.

    Nothing here is estimated. A lesson counts when its build leaves
    'awaiting_student'; a skill counts when its mastery is above zero.
    Uses sqlite3 from the Python standard library, so there is nothing to install.
    """
    import os
    import sqlite3
    db_path = os.path.join(os.path.dirname(__file__), "..", "..", "faizos-core", "data", "faiz.db")
    try:
        con = sqlite3.connect(f"file:{os.path.abspath(db_path)}?mode=ro", uri=True)
    except Exception:
        return  # never let the progress bar break the lesson
    try:
        one = lambda q: con.execute(q).fetchone()[0]
        lessons = min(one("SELECT COUNT(*) FROM builds WHERE state IN ('done','provisional','unlocked')"), 20)
        prod_done = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id "
                        "WHERE t.kind IN ('production','ship') AND s.mastery > 0")
        prod_all = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id "
                       "WHERE t.kind IN ('production','ship')")
        ml_done = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id "
                      "WHERE (t.kind='ml' OR t.kind IS NULL) AND s.mastery > 0")
        ml_all = one("SELECT COUNT(*) FROM skills s LEFT JOIN tracks t ON t.id=s.track_id "
                     "WHERE (t.kind='ml' OR t.kind IS NULL)")
    except Exception:
        con.close()
        return
    con.close()

    def bar(done, total, width=20):
        filled = 0 if total == 0 else round(done / total * width)
        return "#" * filled + "." * (width - filled)

    def pct(a, b):
        return 0 if b == 0 else round(a / b * 100)

    print("\n" + "=" * 68)
    print("  WHERE YOU ACTUALLY ARE")
    print("=" * 68)
    print(f"  Lessons     {bar(lessons,20)}  {lessons}/20     {pct(lessons,20)}%")
    print(f"  Production  {bar(prod_done,prod_all)}  {prod_done}/{prod_all}    {pct(prod_done,prod_all)}%   <- the critical path")
    print(f"  ML (banked) {bar(ml_done,ml_all)}  {ml_done}/{ml_all}    {pct(ml_done,ml_all)}%   understood, not yet evidenced")
    print("=" * 68)


def main():
    print("\nThe question from the top — same model, two workloads:")
    rag_in = 20_000 * price_of("sonnet", "in") / PER_MILLION
    rag_out = 200 * price_of("sonnet", "out") / PER_MILLION
    chat_in = 500 * price_of("sonnet", "in") / PER_MILLION
    chat_out = 1_000 * price_of("sonnet", "out") / PER_MILLION
    print(f"  RAG app  : input ${rag_in:.4f}  output ${rag_out:.4f}   -> output is {rag_out/(rag_in+rag_out):.0%} of the bill")
    print(f"  Chatbot  : input ${chat_in:.4f}  output ${chat_out:.4f}   -> output is {chat_out/(chat_in+chat_out):.0%} of the bill")
    print("  Same model. Which side dominates completely flips, which is why you")
    print("  optimise different things for a RAG app than for a chatbot.")

    print("\nMy code (already working):")
    mine = [
        check("looking up sonnet's input price", price_of("sonnet", "in"), 2.0),
        check("one call on haiku",               cost_for("haiku", 1_000_000, 0), 1.0),
    ]

    print("\nTask 1 — how_much_dearer:")
    t1 = [
        check("opus vs haiku on input",   how_much_dearer("opus", "haiku", 1_000_000, 0), 5.0),
        check("sonnet vs haiku on input", how_much_dearer("sonnet", "haiku", 1_000_000, 0), 2.0),
        check("opus vs sonnet on output", how_much_dearer("opus", "sonnet", 0, 1_000_000), 2.5),
    ]

    print("\nTask 2 — cheapest_model:")
    t2 = [
        check("cheapest for reading", cheapest_model(20_000, 200), "haiku"),
        check("cheapest for writing", cheapest_model(500, 1_000), "haiku"),
        check("cheapest for nothing", cheapest_model(0, 0), "haiku"),
    ]

    done = sum(1 for r in mine + t1 + t2 if r)
    total = len(mine) + len(t1) + len(t2)
    print(f"\n{done} of {total} passing.")

    if done == total:
        # THE NUMBER, measured against the constraint from the top of the file.
        spend = 47_000
        dear = how_much_dearer("opus", "haiku", 20_000, 200)
        saved = (1 - 1 / dear) * 0.60   # route 60% of traffic down to the cheap model
        print("\n--- THE NUMBER, against the $47,000 question ---")
        print(f"  opus costs {dear:.1f}x haiku on a RAG-shaped request.")
        print(f"  Routing 60% of that traffic to haiku saves {saved:.0%}, or ${spend*saved:,.0f}/month.")
        print(f"  Target was 40%. {'MET.' if saved >= 0.40 else 'NOT met on routing alone: add prefix caching from Lesson 1.'}")
        progress_bar()
        print("\nBoth tasks done. Tell me and I'll review it.\n")
    elif all(t1):
        print("Task 1 done. Now the loop.\n")
    else:
        print("Start with Task 1, it is one line. /faiz-hint for a nudge.\n")


main()
