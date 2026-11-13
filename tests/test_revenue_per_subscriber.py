import pytest

from ytagent.revenue import revenue_per_subscriber


def test_divides_revenue_by_subscribers():
    assert revenue_per_subscriber(250.0, 1000) == 0.25


def test_rounds_to_cents():
    assert revenue_per_subscriber(100.0, 3) == 33.33


def test_zero_subscribers_gives_zero():
    assert revenue_per_subscriber(50.0, 0) == 0.0


@pytest.mark.parametrize("revenue, subscribers", [(-1.0, 10), (10.0, -1)])
def test_rejects_negative_inputs(revenue, subscribers):
    with pytest.raises(ValueError):
        revenue_per_subscriber(revenue, subscribers)
