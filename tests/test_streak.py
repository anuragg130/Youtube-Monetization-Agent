import pytest

from ytagent.growth import longest_growth_streak


def test_longest_growth_streak():
    assert longest_growth_streak([10, 12, 15, 15, 18]) == 2
    assert longest_growth_streak([1, 2, 3, 4, 5]) == 4
    assert longest_growth_streak([5, 4, 3]) == 0
    assert longest_growth_streak([1, 2, 1, 2, 3, 4, 2]) == 3


def test_longest_growth_streak_needs_two_values():
    with pytest.raises(ValueError):
        longest_growth_streak([7])
