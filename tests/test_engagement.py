import pytest

from ytagent.engagement import channel_engagement_rate, engagement_rate, subscriber_conversion_rate


def test_engagement_rate():
    assert engagement_rate(likes=450, comments=50, views=10_000) == 5.0
    assert engagement_rate(10, 0, 0) == 0.0


def test_subscriber_conversion_rate():
    assert subscriber_conversion_rate(25, 5_000) == 5.0
    assert subscriber_conversion_rate(3, 0) == 0.0


def test_rejects_negative_counts():
    with pytest.raises(ValueError):
        engagement_rate(-1, 0, 100)
    with pytest.raises(ValueError):
        subscriber_conversion_rate(1, -100)


def test_channel_engagement_rate_weights_by_views():
    videos = [
        {"likes": 90, "comments": 10, "views": 1000},
        {"likes": 1, "comments": 0, "views": 1},
    ]
    assert channel_engagement_rate(videos) == 10.09
    assert channel_engagement_rate([]) == 0.0


def test_channel_engagement_rate_validates_input():
    with pytest.raises(KeyError):
        channel_engagement_rate([{"likes": 1, "views": 10}])
    with pytest.raises(ValueError):
        channel_engagement_rate([{"likes": -1, "comments": 0, "views": 10}])
