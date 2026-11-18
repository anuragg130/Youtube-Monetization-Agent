import pytest

from ytagent.growth import growth_acceleration


def test_speeding_up():
    assert growth_acceleration([100, 110, 120, 140, 160]) == 10.0


def test_slowing_down():
    assert growth_acceleration([100, 150, 200, 210, 220]) == -40.0


def test_odd_number_of_changes_drops_middle():
    assert growth_acceleration([0, 1, 100, 102]) == 1.0


def test_steady_growth_is_zero():
    assert growth_acceleration([10, 20, 30, 40]) == 0.0


def test_too_short():
    with pytest.raises(ValueError):
        growth_acceleration([1, 2])
