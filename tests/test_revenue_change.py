import pytest

from ytagent.revenue import revenue_change_percent


def test_growth():
    assert revenue_change_percent(200, 250) == 25.0


def test_decline():
    assert revenue_change_percent(120.0, 90.0) == -25.0


def test_no_change():
    assert revenue_change_percent(50, 50) == 0.0


@pytest.mark.parametrize("previous, current", [(0, 10), (-5, 10), (10, -1)])
def test_rejects_invalid(previous, current):
    with pytest.raises(ValueError):
        revenue_change_percent(previous, current)
