import pytest

from ytagent.revenue import daily_revenue_needed


def test_daily_revenue_needed():
    assert daily_revenue_needed(500, 320, 9) == 20.0
    assert daily_revenue_needed(100, 0, 3) == 33.33


def test_target_already_met():
    assert daily_revenue_needed(500, 650, 5) == 0.0


@pytest.mark.parametrize("target, earned, days", [(-1, 0, 5), (100, -5, 5), (100, 0, 0)])
def test_rejects_bad_input(target, earned, days):
    with pytest.raises(ValueError):
        daily_revenue_needed(target, earned, days)
