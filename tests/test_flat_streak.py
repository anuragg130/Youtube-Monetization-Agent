import pytest

from ytagent.growth import flat_days, longest_flat_streak


def test_longest_flat_streak():
    assert longest_flat_streak([500, 500, 500, 510, 510, 505]) == 2


def test_no_flat_days():
    assert longest_flat_streak([1, 2, 3, 2]) == 0


def test_streak_never_exceeds_flat_day_count():
    counts = [10, 10, 11, 11, 11, 11, 12]
    assert longest_flat_streak(counts) == 3
    assert longest_flat_streak(counts) <= len(flat_days(counts))


def test_requires_two_values():
    with pytest.raises(ValueError):
        longest_flat_streak([100])
