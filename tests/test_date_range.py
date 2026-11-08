import pandas as pd
import pytest

from ytagent.frame import filter_date_range

DF = pd.DataFrame({
    "date": ["2026-11-03", "2026-11-01", "2026-11-02", "2026-11-04"],
    "subscribers": [710, 690, 700, 725],
    "watch_hours": [2500.0, 2420.0, 2460.0, 2550.0],
})


def test_filter_date_range_inclusive_and_sorted():
    out = filter_date_range(DF, "2026-11-02", "2026-11-03")
    assert out["subscribers"].tolist() == [700, 710]


def test_filter_date_range_open_ended():
    assert len(filter_date_range(DF, start="2026-11-03")) == 2
    assert len(filter_date_range(DF, end="2026-11-01")) == 1
    assert len(filter_date_range(DF)) == 4


def test_filter_date_range_validates():
    with pytest.raises(ValueError):
        filter_date_range(DF, "2026-11-04", "2026-11-01")
    with pytest.raises(ValueError):
        filter_date_range(DF.drop(columns="date"))
