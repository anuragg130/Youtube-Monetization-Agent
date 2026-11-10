import pandas as pd
import pytest

from ytagent.frame import best_day


def _frame():
    return pd.DataFrame({
        "date": ["2026-11-03", "2026-11-01", "2026-11-02", "2026-11-04"],
        "subscribers": [160, 100, 130, 170],
        "watch_hours": [52.0, 40.0, 41.5, 60.0],
    })


def test_best_day_for_subscribers():
    assert best_day(_frame()) == {"date": "2026-11-02", "gain": 30}


def test_best_day_for_watch_hours():
    assert best_day(_frame(), "new_watch_hours") == {"date": "2026-11-03", "gain": 10.5}


def test_best_day_validation():
    with pytest.raises(ValueError):
        best_day(_frame(), "views")
    with pytest.raises(ValueError):
        best_day(_frame().head(1))
