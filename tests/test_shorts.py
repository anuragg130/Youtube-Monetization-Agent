import pytest

from ytagent.shorts import is_shorts_eligible, shorts_gap


def test_shorts_eligible_at_thresholds():
    assert is_shorts_eligible(1000, 10_000_000)


def test_shorts_not_eligible_without_views():
    assert not is_shorts_eligible(5000, 9_999_999)


def test_shorts_gap():
    assert shorts_gap(800, 6_500_000) == {"subscribers_needed": 200, "shorts_views_needed": 3_500_000}
    assert shorts_gap(2000, 12_000_000) == {"subscribers_needed": 0, "shorts_views_needed": 0}


def test_shorts_rejects_negative():
    with pytest.raises(ValueError):
        is_shorts_eligible(-1, 0)
    with pytest.raises(ValueError):
        shorts_gap(0, -5)
