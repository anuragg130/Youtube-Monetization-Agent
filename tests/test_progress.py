from ytagent.progress import eligibility_gap, progress_percent


def test_gap_when_short():
    assert eligibility_gap(400, 1000) == {"subscribers_needed": 600, "watch_hours_needed": 3000.0}


def test_gap_zero_when_met():
    assert eligibility_gap(2000, 5000) == {"subscribers_needed": 0, "watch_hours_needed": 0.0}


def test_progress_percent_capped():
    assert progress_percent(500, 8000) == {"subscribers": 50.0, "watch_hours": 100.0}
