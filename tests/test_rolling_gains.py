import pandas as pd
import pytest

from ytagent.frame import add_rolling_gains


def _frame():
    return pd.DataFrame(
        {
            "date": ["2026-11-03", "2026-11-01", "2026-11-02", "2026-11-04"],
            "subscribers": [130, 100, 110, 160],
            "watch_hours": [13.0, 10.0, 11.0, 16.0],
        }
    )


def test_rolling_average_over_window():
    result = add_rolling_gains(_frame(), window=2)
    # daily gains after sorting: 0, 10, 20, 30
    assert result["avg_new_subscribers"].tolist() == pytest.approx([0.0, 5.0, 15.0, 25.0])
    assert result["avg_new_watch_hours"].tolist() == pytest.approx([0.0, 0.5, 1.5, 2.5])


def test_window_of_one_matches_daily_gains():
    result = add_rolling_gains(_frame(), window=1)
    assert result["avg_new_subscribers"].tolist() == result["new_subscribers"].tolist()


def test_rejects_bad_window():
    with pytest.raises(ValueError):
        add_rolling_gains(_frame(), window=0)


def test_requires_columns():
    with pytest.raises(ValueError):
        add_rolling_gains(pd.DataFrame({"date": ["2026-11-01"]}))
