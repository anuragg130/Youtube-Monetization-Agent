import pytest

from ytagent.growth import longest_decline_streak


def test_longest_decline_streak():
    assert longest_decline_streak([500, 498, 495, 495, 490, 489]) == 2
    assert longest_decline_streak([5, 4, 3, 2]) == 3
    assert longest_decline_streak([1, 2, 3]) == 0


def test_longest_decline_streak_needs_two_values():
    with pytest.raises(ValueError):
        longest_decline_streak([3])
