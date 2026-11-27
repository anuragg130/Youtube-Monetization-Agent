import pytest

from ytagent.engagement import median_engagement_rate


def test_median_ignores_single_viral_outlier():
    videos = [
        {"title": "A", "likes": 40, "comments": 10, "views": 1000},
        {"title": "B", "likes": 50, "comments": 10, "views": 1000},
        {"title": "Viral", "likes": 90000, "comments": 10000, "views": 200000},
    ]
    assert median_engagement_rate(videos) == 6.0


def test_even_count_averages_middle_rates():
    videos = [
        {"title": "A", "likes": 10, "comments": 0, "views": 100},
        {"title": "B", "likes": 20, "comments": 0, "views": 100},
    ]
    assert median_engagement_rate(videos) == 15.0


def test_skips_videos_without_views():
    videos = [
        {"title": "Draft", "likes": 0, "comments": 0, "views": 0},
        {"title": "Live", "likes": 8, "comments": 2, "views": 100},
    ]
    assert median_engagement_rate(videos) == 10.0


def test_no_viewed_videos_returns_zero():
    assert median_engagement_rate([]) == 0.0


def test_negative_counts_raise():
    with pytest.raises(ValueError):
        median_engagement_rate([{"title": "Bad", "likes": -1, "comments": 0, "views": 10}])
