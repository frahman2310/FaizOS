# =============================================================================
#  FAIZOS  ·  DRILL  ·  Names, values, and loops
#  Run me:   uv run --no-project python drill.py
# =============================================================================
#
#  This is not a lesson. There is nothing new to learn here. It is six tiny
#  tasks on the two things that have cost you 11 errors so far:
#
#     api-misuse       7 times   passing the NAME's text, or the whole list,
#                                where a value or one item belonged
#     ordering-pairing 4 times   overwriting a name you still needed
#
#  Every task is one or two lines. Do them in order. Each one isolates exactly
#  one idea, so if a task fails you know precisely which idea it was.
#
# =============================================================================


# -----------------------------------------------------------------------------
#  MY CODE  (all working. These are the tools the tasks use.)
# -----------------------------------------------------------------------------

PRICES = {"apple": 30, "bread": 110, "milk": 90}     # pence
BASKET = ["apple", "bread", "milk"]


def price_of(item):
    # Hand it ONE item name, get back that item's price in pence.
    return PRICES[item]


def with_vat(pence):
    # Hand it a number of pence, get back that number plus 20%.
    return pence * 1.2


# =============================================================================
#  TASK 1  ·  pass the value, not the text of the name
# =============================================================================
#  `thing` is handed to you in the brackets. It holds an item name like "bread".
#  Return that item's price, using price_of.
#
#  THE TRAP: price_of("thing") passes the four letters t-h-i-n-g, and there is
#  no item called "thing" in PRICES.
# -----------------------------------------------------------------------------

def task1_price(thing):
    # vvvvv
    return price_of(thing)
    # ^^^^^


# =============================================================================
#  TASK 2  ·  pass ONE item, not the whole list
# =============================================================================
#  Return the price of the FIRST item in BASKET.
#
#  To reach into a list by position, use square brackets and a number.
#  Positions start at 0, so BASKET[0] is the first item, BASKET[1] the second.
#
#  THE TRAP: price_of(BASKET) hands over all three items at once.
# -----------------------------------------------------------------------------

def task2_first_price():
    # vvvvv
    return price_of(BASKET[0])
    # ^^^^^


# =============================================================================
#  TASK 3  ·  a loop that visits each item
# =============================================================================
#  ONE new thing: the `for` line itself.
#
#  Fill the list `visited` with every item in BASKET, in order.
#  `visited.append(x)` adds x to the end of the list.
#
#  Write a `for` line that walks BASKET, and one indented line under it that
#  appends whichever item you are on. Do not touch the first or last line.
# -----------------------------------------------------------------------------

def task3_visit():
    visited = []
    # vvvvv
    for item in BASKET:
        visited.append(item)
    # ^^^^^
    return visited


# =============================================================================
#  TASK 4  ·  a loop that keeps a running total
# =============================================================================
#  ONE new thing: a total that survives across passes.
#
#  Add up the price of every item in BASKET and return the total in pence.
#
#  The pattern: make a total BEFORE the loop, add to it inside the loop, and
#  return it AFTER the loop.
#     total = total + something      means "the new total is the old one plus this"
# -----------------------------------------------------------------------------

def task4_total():
    total = 0
    # vvvvv
    for item in BASKET:
        total = total + price_of(item)
    # ^^^^^
    return total


# =============================================================================
#  TASK 5  ·  spot the overwrite  (no code, just answer)
# =============================================================================
#  This function is meant to return the NAME of the dearest item. It returns
#  a number instead. Set BUG_LINE to the line number that destroys the name.
#
#      1   def dearest():
#      2       best = None
#      3       for item in BASKET:
#      4           item = price_of(item)
#      5           if best is None or item > best:
#      6               best = item
#      7       return best
#
#  Replace None with 1, 2, 3, 4, 5, 6 or 7.
# -----------------------------------------------------------------------------

BUG_LINE = 4


# =============================================================================
#  TASK 6  ·  fix it
# =============================================================================
#  Same function, written properly, returning the NAME of the dearest item.
#  TWO new things: a second tracker, and the keep-the-best `if`.
#
#  You need two trackers: one for the winning NAME, one for its PRICE.
#  Price each item into a THIRD name so the item name survives.
#  Ask: is the price tracker still empty, OR is this price bigger than it?
#  Return the NAME, outside the loop.
# -----------------------------------------------------------------------------

def task6_dearest():
    # vvvvv
    winning_name = None
    winning_price = None
    for item in BASKET:
        this_price = price_of(item)
        if winning_price is None or this_price > winning_price:
            winning_price = this_price
            winning_name = item
    return winning_name
    # ^^^^^


# =============================================================================


def check(label, got, want):
    ok = got == want
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        print(f"        wanted {want!r}, got {got!r}")
    return ok


def main():
    print()
    r = [
        check("1  price of the item you were handed", task1_price("bread"), 110),
        check("1  works for a different item",        task1_price("milk"), 90),
        check("2  price of the first basket item",    task2_first_price(), 30),
        check("3  visited every item in order",       task3_visit(), ["apple", "bread", "milk"]),
        check("4  running total of the basket",       task4_total(), 230),
        check("5  you spotted the overwrite",         BUG_LINE, 4),
        check("6  the dearest item's NAME",           task6_dearest(), "bread"),
    ]
    print(f"\n{sum(1 for x in r if x)} of {len(r)} passing.")
    if all(r):
        print("\nDrill clear. Both gaps closed. Ready for Lesson 3.\n")
    else:
        print("\nDo them in order. Each task isolates one idea.\n")


main()
