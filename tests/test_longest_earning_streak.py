import pytest

from ytagent.revenue import longest_earning_streak


def test_zero_day_breaks_streak():
    assert longest_earning_streak([3.0, 0.0, 2.0, 4.5, 1.0]) == 3


def test_custom_threshold():
    assert longest_earning_streak([12.0, 15.0, 9.0, 11.0, 10.0, 10.5], threshold=10.0) == 3


def test_empty_and_all_zero():
    assert longest_earning_streak([]) == 0
    assert longest_earning_streak([0.0, 0.0]) == 0


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        longest_earning_streak([1.0], threshold=-1.0)
    with pytest.raises(ValueError):
        longest_earning_streak([1.0, -2.0])
