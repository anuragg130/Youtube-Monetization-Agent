import pandas as pd
import pytest

from ytagent.frame import days_meeting_target

DF = pd.DataFrame(
    {
        "date": ["2026-01-03", "2026-01-01", "2026-01-02", "2026-01-04"],
        "subscribers": [130, 100, 110, 155],
        "watch_hours": [16.0, 10.0, 12.5, 21.0],
    }
)


def test_returns_days_at_or_above_target():
    hits = days_meeting_target(DF, 20)
    assert hits["date"].dt.strftime("%Y-%m-%d").tolist() == ["2026-01-03", "2026-01-04"]
    assert hits["new_subscribers"].tolist() == [20, 25]


def test_watch_hours_column():
    hits = days_meeting_target(DF, 4.0, column="new_watch_hours")
    assert len(hits) == 1


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        days_meeting_target(DF, -1)
    with pytest.raises(ValueError):
        days_meeting_target(DF, 1, column="views")
