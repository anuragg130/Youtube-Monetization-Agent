import pandas as pd
import pytest

from ytagent.frame import weekly_gains


def test_weekly_gains_groups_by_week_ending_sunday():
    df = pd.DataFrame(
        {
            "date": ["2026-11-03", "2026-11-01", "2026-11-02", "2026-11-04"],
            "subscribers": [130, 100, 110, 150],
            "watch_hours": [12.0, 10.0, 11.0, 15.0],
        }
    )
    weekly = weekly_gains(df)
    assert list(weekly.index.strftime("%Y-%m-%d")) == ["2026-11-01", "2026-11-08"]
    assert weekly["new_subscribers"].tolist() == [0, 50]
    assert weekly["new_watch_hours"].tolist() == [0.0, 5.0]


def test_weekly_gains_requires_columns():
    with pytest.raises(ValueError):
        weekly_gains(pd.DataFrame({"date": ["2026-11-01"]}))
