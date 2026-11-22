import pandas as pd
import pytest

from ytagent.frame import target_hit_rate

DF = pd.DataFrame(
    {
        "date": ["2026-01-03", "2026-01-01", "2026-01-02", "2026-01-04"],
        "subscribers": [130, 100, 110, 155],
        "watch_hours": [16.0, 10.0, 12.5, 21.0],
    }
)


def test_share_of_days_hitting_target():
    assert target_hit_rate(DF, 20) == 66.67


def test_zero_target_always_hit():
    assert target_hit_rate(DF, 0) == 100.0


def test_rejects_short_frame():
    with pytest.raises(ValueError):
        target_hit_rate(DF.head(1), 5)
