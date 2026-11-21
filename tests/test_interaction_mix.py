import pytest

from ytagent.engagement import interaction_mix


def test_interaction_mix():
    assert interaction_mix(80, 15, 5) == {"likes": 80.0, "comments": 15.0, "shares": 5.0}


def test_no_interactions():
    assert interaction_mix(0, 0, 0) == {"likes": 0.0, "comments": 0.0, "shares": 0.0}


def test_rejects_negative_count():
    with pytest.raises(ValueError):
        interaction_mix(10, -1, 0)
