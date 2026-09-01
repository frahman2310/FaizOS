# =============================================================================
#  FAIZOS LESSON 2  ·  Rate cards: picking the cheapest model
#  Run me:   uv run python lesson.py
# =============================================================================
#
#  THE PROBLEM
#  -----------
#  You have three models to choose from. The expensive one is five times the price
#  of the cheap one. Obvious answer: use the cheap one.
#
#  Except the cheap one is worse, so you only want it where it can cope. Which
#  means you need to know, for YOUR traffic, what each one would actually cost.
#  Not the sticker price. The bill.
#
#  Teams that get this right cut their model spend by 30 to 55 percent. That is
#  the single most quotable number you can put in an interview, and by the end of
#  this file you will have written the code that produces it.
#
#
#  WHAT YOU ALREADY KNOW (from lesson 1)
#  --------------------------------------
#      cost = tokens * rate / PER_MILLION
#
#      Input is charged at one rate. Output is charged at about FIVE TIMES that.
#      Prices are quoted per million, so the million always divides.
#
#  That is all carried forward. This lesson adds the ability to hold MANY prices
#  at once and compare them.
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
#       ROUND brackets  ( )  RUN A FUNCTION.          cost(2000, 0, 3.0, 15.0)
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
#  PART 2 · A QUESTION BEFORE YOU READ MY CODE
# =============================================================================
#
#  Two apps, same model, both charged more for output than input:
#
#      A RAG app   sends 20,000 tokens (a pile of documents), gets back 200.
#      A chatbot   sends    500 tokens (one question),        gets back 1,000.
#
#  In WHICH of those two does the OUTPUT dominate the bill?
#
#  Have an answer in your head before you scroll. The checks at the bottom
#  print both numbers, so the file will tell you if you were right.
#
# =============================================================================


# -----------------------------------------------------------------------------
#  PART 3 · MY CODE  (working. Read it, it is the shape you will copy.)
# -----------------------------------------------------------------------------

PER_MILLION = 1_000_000

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
    # What one call to this model costs. Lesson 1's arithmetic, with the rates
    # fetched from the dict instead of handed in as numbers.

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
#  cheap one, for the same piece of work.
#
#  WHAT IT MUST DO: return the cost on `pricey_model` divided by the cost on
#  `cheap_model`. If one is twice the price of the other, this returns 2.0.
#
#  THE PYTHON YOU NEED:
#    · `cost_for(...)` is a FUNCTION. ROUND brackets. You are running it twice,
#      once for each model.
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

    return how_much_dearer ("opus" / "haiku")

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


# =============================================================================
#  ▼▼▼  YOUR TURN — TASK 2 of 2  (the loop) ▼▼▼
# =============================================================================
#
#  Find the CHEAPEST model for a given piece of work, and return its name.
#
#  Some models are cheaper on input and dearer on output, so you cannot answer
#  this by reading the price list. You have to price the actual workload on each
#  one and compare. That is model routing, and it is worth 30 to 55 percent.
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
#  THE CHECKS  (mine)
# -----------------------------------------------------------------------------

def check(label, got, want):
    ok = got == want if isinstance(want, str) else (got is not None and abs(got - want) < 1e-9)
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        wanted {want}, got {got}")
    return ok


def main():
    print("\nThe question from Part 2 — same model, two workloads:")
    rag_in = 20_000 * price_of("sonnet", "in") / PER_MILLION
    rag_out = 200 * price_of("sonnet", "out") / PER_MILLION
    chat_in = 500 * price_of("sonnet", "in") / PER_MILLION
    chat_out = 1_000 * price_of("sonnet", "out") / PER_MILLION
    print(f"  RAG app  : input ${rag_in:.4f}  output ${rag_out:.4f}   -> output is {rag_out / (rag_in + rag_out):.0%} of the bill")
    print(f"  Chatbot  : input ${chat_in:.4f}  output ${chat_out:.4f}   -> output is {chat_out / (chat_in + chat_out):.0%} of the bill")
    print("  Same model, and which side dominates completely flips. That is why")
    print("  you optimise different things for a RAG app than for a chatbot.")

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
        check("cheapest for reading",      cheapest_model(20_000, 200), "haiku"),
        check("cheapest for writing",      cheapest_model(500, 1_000), "haiku"),
        check("cheapest for nothing",      cheapest_model(0, 0), "haiku"),
    ]

    done = sum(1 for r in mine + t1 + t2 if r)
    total = len(mine) + len(t1) + len(t2)
    print(f"\n{done} of {total} passing.")
    if all(t1) and not all(t2):
        print("Task 1 done. Now the loop.\n")
    elif done == total:
        print("Both done. Tell me and I'll review it.\n")
    else:
        print("Start with Task 1, it is one line. /faiz-hint for a nudge.\n")


main()
