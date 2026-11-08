import pytest

from ytagent.engagement import average_percentage_viewed


def test_average_percentage_viewed():
    assert average_percentage_viewed(240, 600) == 40.0


def test_average_percentage_viewed_caps_at_100():
    assert average_percentage_viewed(75, 60) == 100.0


@pytest.mark.parametrize("duration, length", [(-1, 60), (30, 0), (30, -5)])
def test_average_percentage_viewed_rejects_bad_input(duration, length):
    with pytest.raises(ValueError):
        average_percentage_viewed(duration, length)
