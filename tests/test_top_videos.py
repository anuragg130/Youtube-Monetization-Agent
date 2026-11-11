import pytest

from ytagent.engagement import top_videos_by_engagement

VIDEOS = [
    {"title": "Intro", "likes": 50, "comments": 10, "views": 1000},
    {"title": "Deep dive", "likes": 90, "comments": 30, "views": 1000},
    {"title": "Q&A", "likes": 20, "comments": 20, "views": 1000},
    {"title": "Teaser", "likes": 0, "comments": 0, "views": 0},
]


def test_returns_highest_engagement_first():
    assert top_videos_by_engagement(VIDEOS, n=2) == [("Deep dive", 12.0), ("Intro", 6.0)]


def test_n_larger_than_list_returns_all():
    result = top_videos_by_engagement(VIDEOS, n=10)
    assert len(result) == 4
    assert result[-1] == ("Teaser", 0.0)


def test_rejects_non_positive_n():
    with pytest.raises(ValueError):
        top_videos_by_engagement(VIDEOS, n=0)


def test_rejects_negative_counts():
    with pytest.raises(ValueError):
        top_videos_by_engagement([{"title": "Bad", "likes": -1, "comments": 0, "views": 10}])
