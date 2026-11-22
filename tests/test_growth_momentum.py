import pytest

from ytagent.growth import growth_momentum


def test_detects_acceleration():
    # gains: 10, 10 then 15, 15
    assert growth_momentum([100, 110, 120, 135, 150], days=2) == 50.0


def test_detects_slowdown():
    # gains: 20, 20 then 10, 10
    assert growth_momentum([0, 20, 40, 50, 60], days=2) == -50.0


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        growth_momentum([1, 2, 3], days=2)
    with pytest.raises(ValueError):
        growth_momentum([1, 2, 3], days=0)
    with pytest.raises(ValueError):
        growth_momentum([5, 5, 5, 6, 7], days=2)
