import pytest

from ytagent.milestones import milestone_days


def test_milestone_days():
    assert milestone_days([90, 120, 480, 510]) == {100: 1, 500: 3}


def test_dip_does_not_retrigger():
    assert milestone_days([90, 110, 95, 130]) == {100: 1}


def test_starting_above_milestone_is_not_counted():
    assert milestone_days([100, 400]) == {}


def test_rejects_empty_series():
    with pytest.raises(ValueError):
        milestone_days([])


def test_rejects_negative_count():
    with pytest.raises(ValueError):
        milestone_days([10, -5])
