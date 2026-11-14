import pytest

from ytagent.shorts import days_to_shorts_eligibility


def test_slowest_threshold_sets_the_estimate():
    # 500 subs at 50/day -> 10 days; 6M views at 200k/day -> 30 days
    assert days_to_shorts_eligibility(500, 4_000_000, 50, 200_000) == 30


def test_already_eligible_is_zero():
    assert days_to_shorts_eligibility(1_500, 12_000_000, 0, 0) == 0


def test_zero_rate_on_open_gap_is_none():
    assert days_to_shorts_eligibility(900, 10_000_000, 0, 1_000) is None


def test_rejects_negative_rates():
    with pytest.raises(ValueError):
        days_to_shorts_eligibility(100, 0, -1, 10)
