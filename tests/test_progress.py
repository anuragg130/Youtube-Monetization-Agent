from ytagent.progress import eligibility_gap, progress_percent


def test_gap_when_short():
    assert eligibility_gap(400, 1000) == {"subscribers_needed": 600, "watch_hours_needed": 3000.0}


def test_gap_zero_when_met():
    assert eligibility_gap(2000, 5000) == {"subscribers_needed": 0, "watch_hours_needed": 0.0}


def test_progress_percent_capped():
    assert progress_percent(500, 8000) == {"subscribers": 50.0, "watch_hours": 100.0}


def test_days_to_eligibility_uses_slowest_gap():
    from ytagent.progress import days_to_eligibility

    # 600 subs at 10/day = 60 days; 3000 hours at 100/day = 30 days
    assert days_to_eligibility(400, 1000, 10, 100) == 60
    assert days_to_eligibility(999, 3999.5, 0.3, 1) == 4


def test_days_to_eligibility_edge_cases():
    import pytest

    from ytagent.progress import days_to_eligibility

    assert days_to_eligibility(1200, 4500, 0, 0) == 0
    assert days_to_eligibility(500, 5000, 0, 10) is None
    with pytest.raises(ValueError):
        days_to_eligibility(500, 1000, -1, 10)
