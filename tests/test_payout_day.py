import pytest

from ytagent.revenue import payout_day


def test_day_threshold_is_crossed():
    assert payout_day([40, 35, 30]) == 2


def test_exact_threshold_counts():
    assert payout_day([50, 50], threshold=100) == 1


def test_never_reached_returns_none():
    assert payout_day([10, 20, 30]) is None


def test_custom_threshold():
    assert payout_day([5, 5, 5], threshold=10) == 1


def test_rejects_non_positive_threshold():
    with pytest.raises(ValueError):
        payout_day([10], threshold=0)


def test_rejects_negative_amount():
    with pytest.raises(ValueError):
        payout_day([10, -5])
