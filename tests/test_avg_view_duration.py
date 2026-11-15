import pytest

from ytagent.engagement import average_view_duration_minutes, watch_hours_from_views


def test_average_view_duration_minutes():
    assert average_view_duration_minutes(250, 3000) == 5.0
    assert average_view_duration_minutes(0, 0) == 0.0


def test_round_trips_with_watch_hours_from_views():
    hours = watch_hours_from_views(4800, 7.5)
    assert average_view_duration_minutes(hours, 4800) == 7.5


def test_rejects_negative_inputs():
    with pytest.raises(ValueError):
        average_view_duration_minutes(-1, 10)
