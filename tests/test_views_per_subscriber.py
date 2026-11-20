import pytest

from ytagent.engagement import views_per_subscriber


def test_basic_ratio():
    assert views_per_subscriber(5000, 1000) == 5.0


def test_rounds_to_two_decimals():
    assert views_per_subscriber(1, 3) == 0.33


def test_no_subscribers_returns_zero():
    assert views_per_subscriber(250, 0) == 0.0


@pytest.mark.parametrize("views,subs", [(-1, 10), (10, -1)])
def test_negative_counts_rejected(views, subs):
    with pytest.raises(ValueError):
        views_per_subscriber(views, subs)
