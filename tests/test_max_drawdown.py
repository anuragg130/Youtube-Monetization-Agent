import pytest

from ytagent.growth import max_drawdown_percent


def test_max_drawdown_percent():
    assert max_drawdown_percent([800, 1000, 950, 900, 1100]) == 10.0
    assert max_drawdown_percent([100, 80, 120, 60]) == 50.0


def test_max_drawdown_percent_no_decline():
    assert max_drawdown_percent([1, 2, 2, 3]) == 0.0
    assert max_drawdown_percent([42]) == 0.0


def test_max_drawdown_percent_rejects_bad_input():
    with pytest.raises(ValueError):
        max_drawdown_percent([])
    with pytest.raises(ValueError):
        max_drawdown_percent([10, 0, 5])
