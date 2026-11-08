import pytest

from ytagent.revenue import estimate_revenue, rpm_from_cpm


def test_rpm_from_cpm_defaults():
    assert rpm_from_cpm(10) == 5.5
    assert rpm_from_cpm(10, monetized_share=0.6) == 3.3
    assert rpm_from_cpm(0) == 0.0


def test_rpm_from_cpm_feeds_estimate_revenue():
    rpm = rpm_from_cpm(8, creator_share=0.5)
    assert estimate_revenue(100_000, rpm) == 400.0


@pytest.mark.parametrize("kwargs", [{"cpm": -1}, {"cpm": 5, "creator_share": 1.2}, {"cpm": 5, "monetized_share": -0.1}])
def test_rpm_from_cpm_rejects_bad_input(kwargs):
    with pytest.raises(ValueError):
        rpm_from_cpm(**kwargs)
