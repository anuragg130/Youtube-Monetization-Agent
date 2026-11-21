import pytest

from ytagent.growth import daily_percent_changes


def test_daily_percent_changes():
    assert daily_percent_changes([100, 110, 99]) == [10.0, -10.0]


def test_last_value_may_be_zero():
    assert daily_percent_changes([50, 0]) == [-100.0]


def test_rejects_short_series():
    with pytest.raises(ValueError):
        daily_percent_changes([100])


def test_rejects_zero_baseline():
    with pytest.raises(ValueError):
        daily_percent_changes([100, 0, 10])
