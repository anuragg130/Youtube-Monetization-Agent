import pytest

from ytagent.engagement import watch_hours_from_views


def test_watch_hours_from_views():
    assert watch_hours_from_views(12_000, 5) == 1000.0
    assert watch_hours_from_views(100, 4.5) == 7.5
    assert watch_hours_from_views(0, 8) == 0.0


def test_watch_hours_rejects_negative_inputs():
    with pytest.raises(ValueError):
        watch_hours_from_views(-1, 3)
    with pytest.raises(ValueError):
        watch_hours_from_views(10, -0.5)
