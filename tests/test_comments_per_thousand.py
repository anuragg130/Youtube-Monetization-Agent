import pytest

from ytagent.engagement import comments_per_thousand_views


def test_scales_to_thousand_views():
    assert comments_per_thousand_views(30, 6000) == 5.0


def test_rounds_to_two_places():
    assert comments_per_thousand_views(1, 3000) == 0.33


def test_no_views_gives_zero():
    assert comments_per_thousand_views(0, 0) == 0.0


def test_rejects_negative_counts():
    with pytest.raises(ValueError):
        comments_per_thousand_views(-1, 100)
