"""The tests define done. Run them with: uv run pytest

Note the import on the next line. It says `from tokencost import ...`, not
`from src.tokencost import ...` and not `from core import ...`. That import only
succeeds if your package is genuinely INSTALLED into the environment. If you skip
pyproject.toml, or get the layout wrong, this file fails at line 1 and nothing else
runs. The import is the packaging test.
"""

import pytest

from tokencost import cost, daily_cost


class TestCost:
    """One API call, in dollars. Rates are USD per MILLION tokens."""

    def test_one_million_input_tokens_costs_the_input_rate(self):
        assert cost(tokens_in=1_000_000, tokens_out=0, rate_in=3.0, rate_out=15.0) == 3.0

    def test_one_million_output_tokens_costs_the_output_rate(self):
        assert cost(tokens_in=0, tokens_out=1_000_000, rate_in=3.0, rate_out=15.0) == 15.0

    def test_both_sides_add(self):
        assert cost(tokens_in=1_000_000, tokens_out=1_000_000, rate_in=3.0, rate_out=15.0) == 18.0

    def test_a_realistic_small_call(self):
        # 2k in, 500 out at Sonnet-ish rates. This is the number you would quote in a design review.
        assert cost(tokens_in=2_000, tokens_out=500, rate_in=3.0, rate_out=15.0) == pytest.approx(0.0135)

    def test_nothing_costs_nothing(self):
        assert cost(tokens_in=0, tokens_out=0, rate_in=3.0, rate_out=15.0) == 0.0

    def test_rates_are_per_million_not_per_token(self):
        # If this fails with a number a million times too big, you multiplied where you should
        # have divided. Check which way round the scaling goes.
        assert cost(tokens_in=1, tokens_out=0, rate_in=3.0, rate_out=15.0) == pytest.approx(0.000003)

    @pytest.mark.parametrize(
        ("tokens_in", "tokens_out", "expected"),
        [
            (1_000_000, 0, 3.0),
            (500_000, 500_000, 9.0),
            (0, 2_000_000, 30.0),
        ],
    )
    def test_a_table_of_cases(self, tokens_in, tokens_out, expected):
        assert cost(tokens_in, tokens_out, 3.0, 15.0) == pytest.approx(expected)


class TestDailyCost:
    """The whole product, per day. This is the number that ends a design answer."""

    def test_the_interview_scenario(self):
        # 100k users, 10 calls each, 2k tokens in and 0 out, at $3/M.
        # 100_000 * 10 * 2_000 = 2e9 tokens in. At $3 per million that is $6,000/day.
        assert daily_cost(
            users=100_000, calls_per_user=10, tokens_in=2_000, tokens_out=0,
            rate_in=3.0, rate_out=15.0,
        ) == pytest.approx(6_000.0)

    def test_output_tokens_dominate_when_they_are_priced_higher(self):
        assert daily_cost(
            users=1_000, calls_per_user=1, tokens_in=1_000, tokens_out=1_000,
            rate_in=3.0, rate_out=15.0,
        ) == pytest.approx(18.0)

    def test_no_users_no_bill(self):
        assert daily_cost(
            users=0, calls_per_user=10, tokens_in=2_000, tokens_out=500,
            rate_in=3.0, rate_out=15.0,
        ) == 0.0
