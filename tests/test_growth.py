import pytest

from ytagent.growth import average_daily_growth, daily_changes, median_daily_growth, percent_growth


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
