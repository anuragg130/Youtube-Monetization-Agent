import pytest

from ytagent.growth import best_week


def test_picks_highest_week():
    daily = [1] * 7 + [5] * 7 + [2] * 7
    assert best_week(daily) == (1, 35)


def test_partial_trailing_week_can_win():
    assert best_week([1, 1, 1, 10, 10], week_length=3) == (1, 20)


def test_ties_keep_earliest_week():
    assert best_week([2, 2, 2, 2], week_length=2) == (0, 4)


def test_rejects_empty_input():
    with pytest.raises(ValueError):
        best_week([])
