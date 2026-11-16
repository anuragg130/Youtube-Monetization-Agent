import pytest

from ytagent.growth import days_since_peak


def test_counts_days_after_peak():
    assert days_since_peak([100, 140, 130, 120]) == 2


def test_latest_value_is_peak():
    assert days_since_peak([10, 20, 30]) == 0


def test_repeated_peak_uses_most_recent():
    assert days_since_peak([50, 80, 60, 80, 70]) == 1


def test_single_value():
    assert days_since_peak([42]) == 0


def test_empty_rejected():
    with pytest.raises(ValueError):
        days_since_peak([])
