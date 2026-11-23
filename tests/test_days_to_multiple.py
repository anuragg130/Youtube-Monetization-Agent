import pytest

from ytagent.growth import days_to_multiple, doubling_time_days


def test_matches_doubling_time_for_two():
    counts = [1000, 1100, 1210]
    assert days_to_multiple(counts) == doubling_time_days(counts)


def test_tenfold_growth():
    assert days_to_multiple([1000, 1100, 1210], multiple=10) == 24.16


def test_no_growth_returns_none():
    assert days_to_multiple([300, 300], multiple=3) is None


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        days_to_multiple([100, 200], multiple=1)
    with pytest.raises(ValueError):
        days_to_multiple([100])
    with pytest.raises(ValueError):
        days_to_multiple([0, 100])
