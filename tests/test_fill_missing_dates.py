import pandas as pd
import pytest

from ytagent.frame import fill_missing_dates


def test_gaps_are_forward_filled():
    df = pd.DataFrame({
        "date": ["2026-11-04", "2026-11-01", "2026-11-02"],
        "subscribers": [130, 100, 110],
        "watch_hours": [50.0, 40.0, 44.0],
    })
    result = fill_missing_dates(df)
    assert result["date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2026-11-01", "2026-11-02", "2026-11-03", "2026-11-04",
    ]
    assert result["subscribers"].tolist() == [100, 110, 110, 130]
    assert result["watch_hours"].tolist() == [40.0, 44.0, 44.0, 50.0]


def test_duplicate_dates_keep_last_row():
    df = pd.DataFrame({
        "date": ["2026-11-01", "2026-11-01"],
        "subscribers": [100, 105],
        "watch_hours": [40.0, 41.0],
    })
    assert fill_missing_dates(df)["subscribers"].tolist() == [105]


def test_rejects_empty_or_incomplete_frames():
    with pytest.raises(ValueError):
        fill_missing_dates(pd.DataFrame(columns=["date", "subscribers", "watch_hours"]))
    with pytest.raises(ValueError, match="watch_hours"):
        fill_missing_dates(pd.DataFrame({"date": ["2026-11-01"], "subscribers": [1]}))
