import pytest

from ytagent.revenue import cumulative_revenue


def test_cumulative_revenue():
    assert cumulative_revenue([10, 12.5, 7.25]) == [10.0, 22.5, 29.75]


def test_empty_series():
    assert cumulative_revenue([]) == []


def test_rejects_negative_amount():
    with pytest.raises(ValueError):
        cumulative_revenue([5, -1])
