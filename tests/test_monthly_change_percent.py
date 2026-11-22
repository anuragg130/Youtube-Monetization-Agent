import math

import pandas as pd
import pytest

from ytagent.frame import monthly_change_percent


def _frame():
    return pd.DataFrame(
        {
            "date": ["2026-08-31", "2026-09-30", "2026-10-31", "2026-11-30"],
            "subscribers": [100, 120, 150, 150],
            "watch_hours": [10.0, 12.0, 15.0, 18.0],
        }
    )


def test_subscriber_change_between_months():
    change = monthly_change_percent(_frame())
    assert list(change.index) == ["2026-09", "2026-10", "2026-11"]
    # first month gain (0) is the baseline for September -> NaN
    assert math.isnan(change.iloc[0])
    assert change.iloc[1] == 50.0
    assert change.iloc[2] == -100.0


def test_watch_hours_column():
    change = monthly_change_percent(_frame(), column="new_watch_hours")
    assert change.tolist()[1:] == pytest.approx([50.0, 0.0])


def test_rejects_unknown_column():
    with pytest.raises(ValueError):
        monthly_change_percent(_frame(), column="views")
