import pytest

from ytagent.growth import above_average_days


def test_finds_strong_days():
    # changes: 10, 50, 0, 20 -> mean 20
    assert above_average_days([100, 110, 160, 160, 180]) == [1]


def test_constant_growth_has_no_standouts():
    assert above_average_days([0, 5, 10, 15]) == []


def test_handles_declines():
    # changes: -10, 5, -1 -> mean -2
    assert above_average_days([50, 40, 45, 44]) == [1, 2]


def test_requires_two_values():
    with pytest.raises(ValueError):
        above_average_days([10])
