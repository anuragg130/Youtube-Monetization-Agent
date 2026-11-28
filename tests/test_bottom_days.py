import pandas as pd
import pytest

from ytagent.frame import bottom_days, top_days


def _frame():
    return pd.DataFrame({
        "date": ["2026-11-03", "2026-11-01", "2026-11-02", "2026-11-04", "2026-11-05"],
        "subscribers": [160, 100, 130, 170, 200],
        "watch_hours": [52.0, 40.0, 41.5, 60.0, 61.0],
    })


def test_bottom_days_ranks_smallest_first():
    result = bottom_days(_frame(), n=2)
    assert result["date"].dt.strftime("%Y-%m-%d").tolist() == ["2026-11-04", "2026-11-02"]
    assert result["new_subscribers"].tolist() == [10, 30]


def test_bottom_days_for_watch_hours():
    result = bottom_days(_frame(), "new_watch_hours", n=1)
    assert result["new_watch_hours"].tolist() == [1.0]


def test_covers_same_days_as_top_days():
    df = _frame()
    assert set(bottom_days(df, n=10)["date"]) == set(top_days(df, n=10)["date"])


@pytest.mark.parametrize("kwargs", [{"column": "views"}, {"n": 0}])
def test_rejects_bad_arguments(kwargs):
    with pytest.raises(ValueError):
        bottom_days(_frame(), **kwargs)
