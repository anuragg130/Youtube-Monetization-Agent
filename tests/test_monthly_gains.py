import pandas as pd
import pytest

from ytagent.frame import monthly_gains


def test_monthly_gains_sums_daily_gains_per_month():
    df = pd.DataFrame(
        {
            "date": ["2026-10-31", "2026-10-30", "2026-11-01", "2026-11-02"],
            "subscribers": [120, 100, 150, 160],
            "watch_hours": [12.0, 10.0, 14.5, 15.0],
        }
    )
    monthly = monthly_gains(df)
    assert list(monthly.index) == ["2026-10", "2026-11"]
    assert monthly["new_subscribers"].tolist() == [20, 40]
    assert monthly["new_watch_hours"].tolist() == pytest.approx([2.0, 3.0])


def test_monthly_gains_requires_columns():
    with pytest.raises(ValueError):
        monthly_gains(pd.DataFrame({"date": ["2026-11-01"], "subscribers": [1]}))
