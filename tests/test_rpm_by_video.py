import pytest

from ytagent.revenue import rpm_by_video


def test_per_video_and_weighted_overall():
    result = rpm_by_video([
        {"title": "tutorial", "revenue": 90.0, "views": 30_000},
        {"title": "vlog", "revenue": 10.0, "views": 10_000},
    ])
    assert result == {"tutorial": 3.0, "vlog": 1.0, "__overall__": 2.5}


def test_zero_view_video_has_zero_rpm():
    assert rpm_by_video([{"title": "new", "revenue": 0.0, "views": 0}]) == {"new": 0.0, "__overall__": 0.0}


@pytest.mark.parametrize("videos", [
    [],
    [{"title": "a", "revenue": 1.0}],
    [{"title": "a", "revenue": 1.0, "views": 10}, {"title": "a", "revenue": 2.0, "views": 10}],
    [{"title": "a", "revenue": -1.0, "views": 10}],
])
def test_rejects_invalid_input(videos):
    with pytest.raises(ValueError):
        rpm_by_video(videos)
