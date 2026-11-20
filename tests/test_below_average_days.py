import pytest

from ytagent.growth import above_average_days, below_average_days


def test_finds_weak_days():
    # changes: 10, 2, 12, 4 -> mean 7
    assert below_average_days([100, 110, 112, 124, 128]) == [1, 3]


def test_constant_growth_has_no_below_average_days():
    assert below_average_days([0, 5, 10, 15]) == []


def test_disjoint_from_above_average_days():
    counts = [10, 30, 31, 50, 49, 60]
    assert not set(below_average_days(counts)) & set(above_average_days(counts))


def test_requires_two_values():
    with pytest.raises(ValueError):
        below_average_days([5])
