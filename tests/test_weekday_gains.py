import pandas as pd
import pytest

from ytagent.frame import average_gain_by_weekday


def _frame():
    # 2026-11-01 is a Sunday; the next Sunday follows a week later.
    return pd.DataFrame(
        {
            "date": ["2026-11-01", "2026-11-02", "2026-11-03", "2026-11-08", "2026-11-09"],
            "subscribers": [100, 110, 115, 145, 165],
            "watch_hours": [10.0, 11.0, 12.0, 14.0, 15.0],
        }
    )


def test_weekday_means_in_calendar_order():
    result = average_gain_by_weekday(_frame())
    assert list(result.index) == ["Monday", "Tuesday", "Sunday"]
    assert result["Monday"] == pytest.approx(15.0)
    assert result["Tuesday"] == pytest.approx(5.0)
    assert result["Sunday"] == pytest.approx(30.0)


def test_weekday_watch_hours_column():
    result = average_gain_by_weekday(_frame(), column="new_watch_hours")
    assert result["Monday"] == pytest.approx(1.0)


def test_weekday_rejects_unknown_column():
    with pytest.raises(ValueError):
        average_gain_by_weekday(_frame(), column="views")


def test_weekday_needs_two_rows():
    with pytest.raises(ValueError):
        average_gain_by_weekday(_frame().iloc[:1])
