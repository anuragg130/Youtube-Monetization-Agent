import pytest

from ytagent.engagement import shares_per_thousand_views


def test_basic_rate():
    assert shares_per_thousand_views(12, 4000) == 3.0


def test_rounds_to_two_decimals():
    assert shares_per_thousand_views(2, 3000) == 0.67


def test_no_views_returns_zero():
    assert shares_per_thousand_views(0, 0) == 0.0


def test_negative_counts_rejected():
    with pytest.raises(ValueError):
        shares_per_thousand_views(-1, 100)
    with pytest.raises(ValueError):
        shares_per_thousand_views(1, -100)
