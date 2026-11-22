import pytest

from ytagent.revenue import best_revenue_day


def test_returns_highest_day():
    assert best_revenue_day([4.0, 9.25, 3.5]) == (1, 9.25)


def test_ties_go_to_earliest_day():
    assert best_revenue_day([12.0, 30.5, 30.5]) == (1, 30.5)


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        best_revenue_day([])
    with pytest.raises(ValueError):
        best_revenue_day([1.0, -2.0])
