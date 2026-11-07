import pandas as pd
import pytest

from ytagent.frame import summarize_daily_frame


def test_summarize_sorts_by_date():
    df = pd.DataFrame({
        "date": ["2026-11-03", "2026-11-01", "2026-11-02"],
        "subscribers": [720, 700, 710],
        "watch_hours": [2580.0, 2500.0, 2540.0],
    })
    summary = summarize_daily_frame(df)
    assert summary == {
        "days": 2,
        "subscribers": 720,
        "watch_hours": 2580.0,
        "subs_per_day": 10.0,
        "hours_per_day": 40.0,
    }


def test_summarize_requires_columns():
    with pytest.raises(ValueError, match="watch_hours"):
        summarize_daily_frame(pd.DataFrame({"date": ["2026-11-01"] * 2, "subscribers": [1, 2]}))


def test_summarize_requires_two_rows():
    df = pd.DataFrame({"date": ["2026-11-01"], "subscribers": [1], "watch_hours": [1.0]})
    with pytest.raises(ValueError):
        summarize_daily_frame(df)
