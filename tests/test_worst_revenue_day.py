import pytest

from ytagent.revenue import worst_revenue_day


def test_returns_lowest_day():
    assert worst_revenue_day([4.0, 9.25, 3.5]) == (2, 3.5)


def test_ties_go_to_earliest_day():
    assert worst_revenue_day([5.0, 1.5, 1.5]) == (1, 1.5)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        worst_revenue_day([])
    with pytest.raises(ValueError):
        worst_revenue_day([1.0, -2.0])
