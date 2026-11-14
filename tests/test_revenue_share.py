import pytest

from ytagent.revenue import revenue_share_by_source


def test_shares_sum_to_hundred_and_sort_largest_first():
    shares = revenue_share_by_source({"memberships": 25.0, "ads": 75.0})
    assert list(shares) == ["ads", "memberships"]
    assert shares == {"ads": 75.0, "memberships": 25.0}


def test_zero_total_gives_zero_shares():
    assert revenue_share_by_source({"ads": 0, "super_chat": 0}) == {"ads": 0.0, "super_chat": 0.0}


def test_rounds_to_two_decimals():
    shares = revenue_share_by_source({"a": 1, "b": 1, "c": 1})
    assert shares["a"] == 33.33


@pytest.mark.parametrize("revenues", [{}, {"ads": -1.0}])
def test_rejects_invalid(revenues):
    with pytest.raises(ValueError):
        revenue_share_by_source(revenues)
