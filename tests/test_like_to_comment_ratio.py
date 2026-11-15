import pytest

from ytagent.engagement import like_to_comment_ratio


def test_basic_ratio():
    assert like_to_comment_ratio(120, 30) == 4.0


def test_rounds_to_two_decimals():
    assert like_to_comment_ratio(10, 3) == 3.33


def test_no_comments_returns_zero():
    assert like_to_comment_ratio(50, 0) == 0.0


def test_negative_counts_rejected():
    with pytest.raises(ValueError):
        like_to_comment_ratio(-1, 5)
