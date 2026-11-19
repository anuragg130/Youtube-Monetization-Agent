import pytest

from ytagent.growth import longest_drawdown_days


def test_longest_drawdown_days():
    assert longest_drawdown_days([100, 120, 110, 115, 125, 90]) == 2
    assert longest_drawdown_days([50, 40, 30, 45, 49, 50, 60]) == 4


def test_longest_drawdown_days_never_below_high():
    assert longest_drawdown_days([1, 2, 2, 3]) == 0
    assert longest_drawdown_days([7]) == 0


def test_longest_drawdown_days_unrecovered_tail():
    assert longest_drawdown_days([10, 9, 8, 7]) == 3


def test_longest_drawdown_days_rejects_empty():
    with pytest.raises(ValueError):
        longest_drawdown_days([])
