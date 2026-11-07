import pytest

from ytagent.growth import (
    average_daily_growth,
    daily_changes,
    median_daily_growth,
    peak_daily_gain,
    percent_growth,
    rolling_average,
)


def test_daily_changes():
    assert daily_changes([100, 110, 105, 130]) == [10, -5, 25]


def test_average_and_median_growth():
    counts = [100, 102, 104, 106, 206]
    assert average_daily_growth(counts) == 26.5
    assert median_daily_growth(counts) == 2.0


def test_requires_two_values():
    with pytest.raises(ValueError):
        average_daily_growth([100])


def test_percent_growth():
    assert percent_growth([800, 900, 1000]) == 25.0
    assert percent_growth([200, 150]) == -25.0
    with pytest.raises(ValueError):
        percent_growth([100])
    with pytest.raises(ValueError):
        percent_growth([0, 10])


def test_rolling_average():
    assert rolling_average([10, 20, 30, 40], window=2) == [15, 25, 35]
    assert rolling_average([5, 5, 5], window=3) == [5]
    assert rolling_average([1, 2], window=1) == [1, 2]


def test_rolling_average_invalid_window():
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], window=0)
    with pytest.raises(ValueError):
        rolling_average([1, 2, 3], window=4)


def test_peak_daily_gain():
    assert peak_daily_gain([100, 105, 180, 190]) == (2, 75)
    assert peak_daily_gain([50, 40, 30]) == (1, -10)
    assert peak_daily_gain([0, 10, 0, 10]) == (1, 10)
    with pytest.raises(ValueError):
        peak_daily_gain([100])


def test_weekly_totals_includes_partial_week():
    from ytagent.growth import weekly_totals

    assert weekly_totals([1] * 10) == [7, 3]
    assert weekly_totals([5, 5, 5, 5], week_length=2) == [10, 10]


def test_weekly_totals_rejects_bad_input():
    import pytest
    from ytagent.growth import weekly_totals

    with pytest.raises(ValueError):
        weekly_totals([])
    with pytest.raises(ValueError):
        weekly_totals([1, 2], week_length=0)
