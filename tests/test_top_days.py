import pandas as pd
import pytest

from ytagent.frame import top_days


def _frame():
    return pd.DataFrame({
        "date": ["2026-11-03", "2026-11-01", "2026-11-02", "2026-11-04", "2026-11-05"],
        "subscribers": [160, 100, 130, 170, 200],
        "watch_hours": [52.0, 40.0, 41.5, 60.0, 61.0],
    })


def test_top_days_ranks_and_breaks_ties_by_date():
    result = top_days(_frame(), n=3)
    assert result["date"].dt.strftime("%Y-%m-%d").tolist() == ["2026-11-02", "2026-11-03", "2026-11-05"]
    assert result["new_subscribers"].tolist() == [30, 30, 30]


def test_top_days_for_watch_hours():
    result = top_days(_frame(), "new_watch_hours", n=1)
    assert result["new_watch_hours"].tolist() == [10.5]


def test_n_larger_than_series():
    assert len(top_days(_frame(), n=10)) == 4


@pytest.mark.parametrize("kwargs", [{"column": "views"}, {"n": 0}])
def test_rejects_bad_arguments(kwargs):
    with pytest.raises(ValueError):
        top_days(_frame(), **kwargs)
