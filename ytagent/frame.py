"""pandas helpers for daily channel analytics exports."""
from typing import Dict

import pandas as pd

from ytagent.growth import average_daily_growth

REQUIRED_COLUMNS = ("date", "subscribers", "watch_hours")


def summarize_daily_frame(df: pd.DataFrame) -> Dict[str, float]:
    """Summarise a DataFrame of daily cumulative totals.

    ``df`` needs ``date``, ``subscribers`` and ``watch_hours`` columns; rows
    are sorted by date first so unordered exports work. The returned average
    daily gains can be passed to :func:`ytagent.progress.days_to_eligibility`.

    Raises:
        ValueError: if a required column is missing or there are fewer than two rows.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    if len(df) < 2:
        raise ValueError("need at least two rows")
    ordered = df.assign(date=pd.to_datetime(df["date"])).sort_values("date")
    latest = ordered.iloc[-1]
    return {
        "days": int((ordered["date"].iloc[-1] - ordered["date"].iloc[0]).days),
        "subscribers": int(latest["subscribers"]),
        "watch_hours": float(latest["watch_hours"]),
        "subs_per_day": average_daily_growth(ordered["subscribers"].tolist()),
        "hours_per_day": average_daily_growth(ordered["watch_hours"].tolist()),
    }
