import pytest

from ytagent.growth import declining_days, flat_days


def test_flags_days_without_change():
    assert flat_days([500, 500, 510, 510, 505]) == [1, 3]


def test_steady_growth_has_no_flat_days():
    assert flat_days([10, 20, 30]) == []


def test_flat_and_declining_days_do_not_overlap():
    counts = [100, 100, 90, 90, 95]
    assert not set(flat_days(counts)) & set(declining_days(counts))


def test_requires_two_values():
    with pytest.raises(ValueError):
        flat_days([7])
