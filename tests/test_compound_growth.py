import pytest

from ytagent.growth import compound_daily_growth_rate


def test_compound_rate_for_steady_ten_percent():
    assert compound_daily_growth_rate([1000, 1100, 1210]) == 10.0


def test_compound_rate_ignores_intermediate_path():
    assert compound_daily_growth_rate([100, 300, 50, 400]) == compound_daily_growth_rate([100, 1, 1, 400])


def test_compound_rate_negative_for_decline():
    assert compound_daily_growth_rate([200, 100]) == -50.0


def test_compound_rate_validates():
    with pytest.raises(ValueError):
        compound_daily_growth_rate([10])
    with pytest.raises(ValueError):
        compound_daily_growth_rate([0, 10])
