import pytest

from ytagent.growth import doubling_time_days


def test_ten_percent_daily_growth():
    assert doubling_time_days([1000, 1100, 1210]) == 7.27


def test_flat_or_shrinking_never_doubles():
    assert doubling_time_days([500, 500]) is None
    assert doubling_time_days([500, 450, 400]) is None


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        doubling_time_days([100])
    with pytest.raises(ValueError):
        doubling_time_days([0, 100])
