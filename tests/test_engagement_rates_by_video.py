import pytest

from ytagent.engagement import engagement_rates_by_video


def test_maps_each_title_to_its_rate():
    videos = [
        {"title": "Intro", "likes": 90, "comments": 10, "views": 1000},
        {"title": "Deep dive", "likes": 20, "comments": 5, "views": 500},
    ]
    assert engagement_rates_by_video(videos) == {"Intro": 10.0, "Deep dive": 5.0}


def test_video_without_views_scores_zero():
    videos = [{"title": "Draft", "likes": 0, "comments": 0, "views": 0}]
    assert engagement_rates_by_video(videos) == {"Draft": 0.0}


def test_rejects_duplicate_titles():
    videos = [
        {"title": "Same", "likes": 1, "comments": 0, "views": 10},
        {"title": "Same", "likes": 2, "comments": 0, "views": 10},
    ]
    with pytest.raises(ValueError):
        engagement_rates_by_video(videos)


def test_missing_key_raises():
    with pytest.raises(KeyError):
        engagement_rates_by_video([{"title": "Oops", "likes": 1, "views": 10}])
