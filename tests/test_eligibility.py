from ytagent.eligibility import is_eligible


def test_eligible():
    assert is_eligible(1500, 4200)


def test_not_eligible():
    assert not is_eligible(900, 5000)


def test_exact_thresholds_are_eligible():
    assert is_eligible(1000, 4000)


def test_negative_metrics_rejected():
    import pytest

    with pytest.raises(ValueError):
        is_eligible(-1, 4000)
    with pytest.raises(ValueError):
        is_eligible(1000, -0.5)
