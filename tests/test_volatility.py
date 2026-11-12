import pytest

from ytagent.growth import growth_volatility


def test_steady_growth_has_zero_volatility():
    assert growth_volatility([100, 110, 120, 130]) == 0.0


def test_spiky_growth_is_volatile():
    # daily changes: 10, 50, 0 -> sample stdev ~26.46
    assert growth_volatility([100, 110, 160, 160]) == pytest.approx(26.46)


def test_single_change_returns_zero():
    assert growth_volatility([5, 9]) == 0.0


def test_requires_two_values():
    with pytest.raises(ValueError):
        growth_volatility([100])
