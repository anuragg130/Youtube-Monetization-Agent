import pytest

from ytagent.growth import average_daily_growth, recent_average_growth


def test_uses_only_trailing_changes():
    counts = [100, 110, 120, 125, 128]
    assert recent_average_growth(counts, days=2) == 4.0


def test_short_history_uses_all_changes():
    counts = [100, 104, 110]
    assert recent_average_growth(counts, days=30) == average_daily_growth(counts)


def test_rejects_bad_arguments():
    with pytest.raises(ValueError):
        recent_average_growth([1, 2], days=0)
    with pytest.raises(ValueError):
        recent_average_growth([1])
