import pytest

from ytagent.revenue import estimate_revenue, views_needed_for_revenue


def test_views_needed_for_revenue():
    assert views_needed_for_revenue(500, 2.5) == 200_000
    assert views_needed_for_revenue(0, 3.0) == 0
    assert views_needed_for_revenue(10, 3.0) == 3334


def test_views_needed_round_trips_with_estimate():
    views = views_needed_for_revenue(800.0, 3.2)
    assert estimate_revenue(views, 3.2) == 800.0


def test_views_needed_validation():
    with pytest.raises(ValueError):
        views_needed_for_revenue(-1, 2.0)
    with pytest.raises(ValueError):
        views_needed_for_revenue(100, 0)
