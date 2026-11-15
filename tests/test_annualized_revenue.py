import pytest

from ytagent.revenue import annualized_revenue


def test_annualized_revenue():
    assert annualized_revenue(250, 30) == 3041.67
    assert annualized_revenue(1000, 365) == 1000.0
    assert annualized_revenue(0, 7) == 0.0


@pytest.mark.parametrize("revenue, days", [(-1, 30), (100, 0)])
def test_annualized_revenue_rejects_bad_input(revenue, days):
    with pytest.raises(ValueError):
        annualized_revenue(revenue, days)
