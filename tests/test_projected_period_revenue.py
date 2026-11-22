import pytest

from ytagent.revenue import projected_period_revenue


def test_extrapolates_current_pace():
    assert projected_period_revenue(320, 21) == 457.14


def test_full_period_returns_earned():
    assert projected_period_revenue(500, 30) == 500.0


def test_custom_period_length():
    assert projected_period_revenue(70, 7, days_in_period=28) == 280.0


@pytest.mark.parametrize("earned, elapsed, period", [(-1, 5, 30), (10, 0, 30), (10, 31, 30)])
def test_rejects_invalid_input(earned, elapsed, period):
    with pytest.raises(ValueError):
        projected_period_revenue(earned, elapsed, period)
