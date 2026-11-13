import pytest

from ytagent.growth import declining_days


def test_flags_days_with_losses():
    assert declining_days([500, 498, 510, 505, 505]) == [1, 3]


def test_flat_days_are_not_declines():
    assert declining_days([100, 100, 100]) == []


def test_steady_growth_has_no_declines():
    assert declining_days([10, 20, 30, 40]) == []


def test_requires_two_values():
    with pytest.raises(ValueError):
        declining_days([42])
