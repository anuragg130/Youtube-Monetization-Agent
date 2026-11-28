import pytest

from ytagent.revenue import earning_day_share


def test_half_of_days_earned():
    assert earning_day_share([0.0, 2.0, 0.0, 3.0]) == 50.0


def test_all_and_no_earning_days():
    assert earning_day_share([1.0, 0.5, 2.0]) == 100.0
    assert earning_day_share([0.0, 0.0]) == 0.0


def test_rounds_to_one_decimal():
    assert earning_day_share([1.0, 0.0, 0.0]) == 33.3


def test_empty_series_gives_zero():
    assert earning_day_share([]) == 0.0


def test_rejects_negative_amount():
    with pytest.raises(ValueError):
        earning_day_share([1.0, -2.0])
