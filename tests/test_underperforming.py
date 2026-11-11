import pytest

from ytagent.engagement import underperforming_videos

VIDEOS = [
    {"title": "Intro", "likes": 50, "comments": 10, "views": 1000},
    {"title": "Deep dive", "likes": 90, "comments": 30, "views": 1000},
    {"title": "Q&A", "likes": 20, "comments": 0, "views": 1000},
    {"title": "Teaser", "likes": 0, "comments": 0, "views": 0},
]


def test_flags_videos_below_half_channel_rate():
    # Channel rate is 200 / 3000 = 6.67%, so the cutoff is ~3.33%.
    assert underperforming_videos(VIDEOS) == [("Q&A", 2.0)]


def test_higher_threshold_flags_more_videos_lowest_first():
    assert underperforming_videos(VIDEOS, threshold=1.0) == [("Q&A", 2.0), ("Intro", 6.0)]


def test_zero_threshold_flags_nothing():
    assert underperforming_videos(VIDEOS, threshold=0) == []


def test_rejects_negative_threshold():
    with pytest.raises(ValueError):
        underperforming_videos(VIDEOS, threshold=-0.1)
