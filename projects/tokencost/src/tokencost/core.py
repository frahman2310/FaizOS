"""What an LLM feature costs.

Providers quote prices per MILLION tokens, because per-token prices would be numbers
like 0.000003 and nobody can read those. So every rate here is dollars per million,
and every calculation has to scale back down by a million to get real money.
"""

PER_MILLION = 1_000_000


def cost(tokens_in: int, tokens_out: int, rate_in: float, rate_out: float) -> float:
    """Dollars for one API call.

    Input and output are priced separately, and output is usually several times
    dearer, so the two sides are calculated apart and then added.
    """
    input_cost = tokens_in * rate_in / PER_MILLION
    output_cost = tokens_out * rate_out / PER_MILLION
    return input_cost + output_cost


def daily_cost(
    users: int,
    calls_per_user: int,
    tokens_in: int,
    tokens_out: int,
    rate_in: float,
    rate_out: float,
) -> float:
    """Dollars per day for the whole product.

    This is the number that ends a design answer. One call's cost, multiplied by
    how many calls a day the traffic actually produces.
    """
    calls_per_day = users * calls_per_user
    return calls_per_day * cost(tokens_in, tokens_out, rate_in, rate_out)
