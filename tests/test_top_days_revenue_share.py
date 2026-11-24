import pytest

from ytagent.revenue import top_days_revenue_share


def test_single_spike_dominates():
    assert top_days_revenue_share([10.0, 10.0, 80.0], n=1) == 80.0


def test_default_top_three():
    assert top_days_revenue_share([1.0, 2.0, 3.0, 4.0]) == 90.0


def test_n_larger_than_days_covers_everything():
    assert top_days_revenue_share([2.5, 7.5], n=5) == 100.0


def test_zero_or_empty_revenue_returns_zero():
    assert top_days_revenue_share([0.0, 0.0]) == 0.0
    assert top_days_revenue_share([]) == 0.0


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        top_days_revenue_share([1.0], n=0)
    with pytest.raises(ValueError):
        top_days_revenue_share([1.0, -1.0])
