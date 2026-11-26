import pytest

from ytagent.revenue import revenue_volatility


def test_steady_income_has_zero_volatility():
    assert revenue_volatility([5.0, 5.0, 5.0]) == 0.0


def test_coefficient_of_variation():
    # mean 10, sample stdev 2 -> 20%
    assert revenue_volatility([8.0, 10.0, 12.0]) == 20.0


def test_short_or_empty_series():
    assert revenue_volatility([]) == 0.0
    assert revenue_volatility([7.5]) == 0.0


def test_all_zero_revenue():
    assert revenue_volatility([0.0, 0.0, 0.0]) == 0.0


def test_negative_revenue_rejected():
    with pytest.raises(ValueError):
        revenue_volatility([1.0, -2.0])
