import pytest

from ytagent.revenue import effective_rpm, estimate_revenue, revenue_range


def test_estimate_revenue():
    assert estimate_revenue(250_000, 3.2) == 800.0
    assert estimate_revenue(0, 5.0) == 0.0


def test_effective_rpm():
    assert effective_rpm(800.0, 250_000) == 3.2
    assert effective_rpm(10.0, 0) == 0.0


def test_revenue_range_and_validation():
    assert revenue_range(100_000, 1.5, 4.0) == {"low": 150.0, "high": 400.0}
    with pytest.raises(ValueError):
        revenue_range(100_000, 5.0, 1.0)
    with pytest.raises(ValueError):
        estimate_revenue(-1, 2.0)


def test_project_monthly_revenue():
    from ytagent.revenue import project_monthly_revenue

    assert project_monthly_revenue(2000, 3.0, monetized_share=0.6) == 108.0
    assert project_monthly_revenue(1000, 2.0, days=7) == 14.0


def test_project_monthly_revenue_rejects_bad_share():
    import pytest
    from ytagent.revenue import project_monthly_revenue

    with pytest.raises(ValueError):
        project_monthly_revenue(1000, 2.0, monetized_share=1.5)
    with pytest.raises(ValueError):
        project_monthly_revenue(1000, 2.0, days=0)
