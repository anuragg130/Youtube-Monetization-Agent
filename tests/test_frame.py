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


def test_add_daily_gains_sorted_and_non_mutating():
    from ytagent.frame import add_daily_gains

    df = pd.DataFrame({
        "date": ["2026-11-02", "2026-11-01", "2026-11-03"],
        "subscribers": [710, 700, 735],
        "watch_hours": [2540.0, 2500.0, 2600.0],
    })
    out = add_daily_gains(df)
    assert out["new_subscribers"].tolist() == [0, 10, 25]
    assert out["new_watch_hours"].tolist() == [0.0, 40.0, 60.0]
    assert "new_subscribers" not in df.columns


def test_add_daily_gains_requires_columns():
    from ytagent.frame import add_daily_gains

    with pytest.raises(ValueError, match="subscribers"):
        add_daily_gains(pd.DataFrame({"date": [], "watch_hours": []}))
