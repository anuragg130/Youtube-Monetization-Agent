import pytest

from ytagent.milestones import milestones_between


def test_milestones_between_crosses_several():
    assert milestones_between(50, 12_000) == [100, 500, 1_000, 10_000]


def test_milestones_between_excludes_start():
    assert milestones_between(1_000, 1_500) == []


def test_milestones_between_includes_end():
    assert milestones_between(999, 1_000) == [1_000]


def test_milestones_between_rejects_bad_input():
    with pytest.raises(ValueError):
        milestones_between(500, 100)
    with pytest.raises(ValueError):
        milestones_between(-1, 100)
