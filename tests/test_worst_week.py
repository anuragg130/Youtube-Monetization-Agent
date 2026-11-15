import pytest

from ytagent.growth import worst_week


def test_picks_lowest_week():
    daily = [3] * 7 + [1] * 7 + [5] * 7
    assert worst_week(daily) == (1, 7)


def test_partial_trailing_week_is_considered():
    assert worst_week([5, 5, 5, 4, 4, 4, 1], week_length=3) == (2, 1)


def test_ties_keep_earliest_week():
    assert worst_week([2, 2, 2, 2], week_length=2) == (0, 4)


def test_rejects_bad_week_length():
    with pytest.raises(ValueError):
        worst_week([1, 2, 3], week_length=0)
