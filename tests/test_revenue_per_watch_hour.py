import pytest

from ytagent.revenue import revenue_per_watch_hour


def test_basic_rate():
    assert revenue_per_watch_hour(90, 1200) == 0.08


def test_higher_earning_format():
    assert revenue_per_watch_hour(250, 500) == 0.5


def test_zero_watch_hours_returns_zero():
    assert revenue_per_watch_hour(10, 0) == 0.0


def test_negative_inputs_rejected():
    with pytest.raises(ValueError):
        revenue_per_watch_hour(-5, 100)


def test_half_cent_rounds_up():
    assert revenue_per_watch_hour(1, 200) == 0.01
