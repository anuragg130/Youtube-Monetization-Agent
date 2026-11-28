import pytest

from ytagent.revenue import median_daily_revenue


def test_median_resists_spike():
    assert median_daily_revenue([1.0, 1.5, 2.0, 40.0]) == 1.75


def test_odd_length_picks_middle_day():
    assert median_daily_revenue([3.0, 1.0, 2.0]) == 2.0


def test_skip_zero_days():
    days = [0.0, 0.0, 0.0, 4.0, 6.0]
    assert median_daily_revenue(days) == 0.0
    assert median_daily_revenue(days, skip_zero_days=True) == 5.0


def test_empty_series_gives_zero():
    assert median_daily_revenue([]) == 0.0
    assert median_daily_revenue([0.0], skip_zero_days=True) == 0.0


def test_rejects_negative_amount():
    with pytest.raises(ValueError):
        median_daily_revenue([1.0, -0.5])
