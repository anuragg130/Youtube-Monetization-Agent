import pytest

from ytagent.growth import project_value


def test_project_value_uses_average_growth():
    assert project_value([620, 640, 655, 690, 710], 10) == 935.0


def test_project_value_zero_days_returns_latest():
    assert project_value([100, 90], 0) == 90


def test_project_value_validates():
    with pytest.raises(ValueError):
        project_value([1, 2], -1)
    with pytest.raises(ValueError):
        project_value([5], 3)
