import pytest

from ytagent.engagement import share_to_like_ratio


def test_basic_ratio():
    assert share_to_like_ratio(25, 500) == 5.0


def test_rounds_to_two_decimals():
    assert share_to_like_ratio(1, 3) == 33.33


def test_no_likes_returns_zero():
    assert share_to_like_ratio(10, 0) == 0.0


def test_negative_counts_rejected():
    with pytest.raises(ValueError):
        share_to_like_ratio(-1, 10)
    with pytest.raises(ValueError):
        share_to_like_ratio(1, -10)
