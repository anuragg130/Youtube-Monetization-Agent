import pytest

from ytagent.milestones import days_to_next_milestone


def test_days_to_next_milestone_rounds_up():
    assert days_to_next_milestone(750, 20) == 13


def test_days_to_next_milestone_never_without_growth():
    assert days_to_next_milestone(750, 0) is None
    assert days_to_next_milestone(750, -5) is None


def test_days_to_next_milestone_after_final_milestone():
    assert days_to_next_milestone(20_000_000, 1000) is None


def test_days_to_next_milestone_validates():
    with pytest.raises(ValueError):
        days_to_next_milestone(-1, 10)
