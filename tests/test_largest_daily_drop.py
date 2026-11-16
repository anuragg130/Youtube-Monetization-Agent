import pytest

from ytagent.growth import largest_daily_drop


def test_finds_biggest_loss():
    assert largest_daily_drop([500, 498, 470, 480]) == (2, -28)


def test_ties_keep_earliest_day():
    assert largest_daily_drop([100, 90, 95, 85]) == (1, -10)


def test_no_decline_returns_smallest_change():
    assert largest_daily_drop([10, 15, 17, 30]) == (2, 2)


def test_requires_two_values():
    with pytest.raises(ValueError):
        largest_daily_drop([5])
