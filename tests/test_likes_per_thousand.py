import pytest

from ytagent.engagement import likes_per_thousand_views


def test_basic_rate():
    assert likes_per_thousand_views(45, 1500) == 30.0


def test_rounds_to_two_decimals():
    assert likes_per_thousand_views(1, 3000) == 0.33


def test_no_views_returns_zero():
    assert likes_per_thousand_views(0, 0) == 0.0


def test_negative_counts_rejected():
    with pytest.raises(ValueError):
        likes_per_thousand_views(-1, 100)
    with pytest.raises(ValueError):
        likes_per_thousand_views(1, -100)
