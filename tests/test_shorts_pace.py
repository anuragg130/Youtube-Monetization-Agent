import pytest

from ytagent.shorts import SHORTS_VIEWS_THRESHOLD, shorts_pace_ratio


def test_threshold_is_roughly_full_pace():
    assert shorts_pace_ratio(SHORTS_VIEWS_THRESHOLD) == 1.0


def test_half_pace():
    assert shorts_pace_ratio(5_000_000) == 0.5


def test_above_pace_and_zero():
    assert shorts_pace_ratio(20_000_000) == 2.0
    assert shorts_pace_ratio(0) == 0.0


def test_rejects_negative_views():
    with pytest.raises(ValueError):
        shorts_pace_ratio(-1)
