import pytest

from ytagent.shorts import shorts_progress_percent


def test_shorts_progress_partial():
    assert shorts_progress_percent(250, 2_500_000) == {"subscribers": 25.0, "shorts_views": 25.0}


def test_shorts_progress_caps_at_100():
    assert shorts_progress_percent(5000, 40_000_000) == {"subscribers": 100.0, "shorts_views": 100.0}


def test_shorts_progress_zero():
    assert shorts_progress_percent(0, 0) == {"subscribers": 0.0, "shorts_views": 0.0}


def test_shorts_progress_rejects_negative():
    with pytest.raises(ValueError):
        shorts_progress_percent(10, -1)
