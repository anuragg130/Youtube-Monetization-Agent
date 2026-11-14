import pytest

from ytagent.milestones import milestone_progress, milestones_reached, next_milestone


def test_next_milestone_basic():
    assert next_milestone(0) == 100
    assert next_milestone(999) == 1_000
    assert next_milestone(1_000) == 10_000


def test_next_milestone_past_all():
    assert next_milestone(20_000_000) is None


def test_next_milestone_rejects_negative():
    with pytest.raises(ValueError):
        next_milestone(-1)


def test_milestone_progress():
    assert milestone_progress(750) == (1000, 50.0)
    assert milestone_progress(50) == (100, 50.0)
    assert milestone_progress(10_000_000) == (None, 100.0)


def test_milestones_reached_includes_exact_hits():
    assert milestones_reached(0) == []
    assert milestones_reached(99) == []
    assert milestones_reached(1_000) == [100, 500, 1_000]
    assert milestones_reached(20_000_000)[-1] == 10_000_000


def test_milestones_reached_rejects_negative():
    with pytest.raises(ValueError):
        milestones_reached(-1)
