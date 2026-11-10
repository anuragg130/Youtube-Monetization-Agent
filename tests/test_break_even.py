import pytest

from ytagent.revenue import break_even_daily_views, project_monthly_revenue


def test_break_even_example():
    assert break_even_daily_views(300, 3.0, monetized_share=0.5) == 6667


def test_break_even_covers_costs():
    daily = break_even_daily_views(450, 2.5, monetized_share=0.6)
    assert project_monthly_revenue(daily, 2.5, monetized_share=0.6) >= 450


def test_zero_costs_need_no_views():
    assert break_even_daily_views(0, 4.0) == 0


@pytest.mark.parametrize(
    "kwargs",
    [{"monetized_share": 0}, {"monetized_share": 1.5}, {"days": 0}],
)
def test_break_even_rejects_bad_inputs(kwargs):
    with pytest.raises(ValueError):
        break_even_daily_views(100, 3.0, **kwargs)


def test_break_even_rejects_zero_rpm():
    with pytest.raises(ValueError):
        break_even_daily_views(100, 0)
