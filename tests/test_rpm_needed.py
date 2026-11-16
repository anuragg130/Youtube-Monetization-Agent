import pytest

from ytagent.revenue import estimate_revenue, rpm_needed_for_target


def test_basic_rpm():
    assert rpm_needed_for_target(250, 50_000) == 5.0


def test_round_trips_with_estimate_revenue():
    rpm = rpm_needed_for_target(135, 30_000)
    assert rpm == 4.5
    assert estimate_revenue(30_000, rpm) == 135.0


def test_zero_target():
    assert rpm_needed_for_target(0, 1000) == 0.0


def test_invalid_inputs():
    with pytest.raises(ValueError):
        rpm_needed_for_target(-1, 1000)
    with pytest.raises(ValueError):
        rpm_needed_for_target(100, 0)
