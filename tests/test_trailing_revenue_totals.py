import pytest

from ytagent.revenue import trailing_revenue_totals


def test_sliding_sums():
    assert trailing_revenue_totals([1.0, 2.0, 3.0, 4.0], window=2) == [3.0, 5.0, 7.0]


def test_window_equal_to_length_gives_single_total():
    assert trailing_revenue_totals([1.5, 2.5, 3.0], window=3) == [7.0]


def test_short_series_gives_empty_list():
    assert trailing_revenue_totals([5.0] * 10) == []


def test_default_window_is_28_days():
    assert trailing_revenue_totals([1.0] * 30) == [28.0, 28.0, 28.0]


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        trailing_revenue_totals([1.0], window=0)
    with pytest.raises(ValueError):
        trailing_revenue_totals([1.0, -1.0], window=1)
