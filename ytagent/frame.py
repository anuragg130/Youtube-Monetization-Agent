"""pandas helpers for daily channel analytics exports."""
from typing import Dict, Optional

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


def add_daily_gains(df: pd.DataFrame) -> pd.DataFrame:
    """Return a date-sorted copy of ``df`` with per-day gain columns.

    Adds ``new_subscribers`` and ``new_watch_hours`` from the day-over-day
    difference of the cumulative totals. The first row has no prior day, so
    its gains are 0. The input DataFrame is not modified.

    Raises:
        ValueError: if a required column is missing.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    ordered = df.assign(date=pd.to_datetime(df["date"])).sort_values("date").reset_index(drop=True)
    ordered["new_subscribers"] = ordered["subscribers"].diff().fillna(0).astype(int)
    ordered["new_watch_hours"] = ordered["watch_hours"].diff().fillna(0.0)
    return ordered


def filter_date_range(df: pd.DataFrame, start: Optional[str] = None, end: Optional[str] = None) -> pd.DataFrame:
    """Return the rows of ``df`` whose ``date`` falls within ``[start, end]``.

    Either bound may be omitted. Dates are parsed with :func:`pandas.to_datetime`
    and the result is sorted by date, ready for :func:`summarize_daily_frame`
    when only a recent window (e.g. the last 28 days) is of interest.

    Raises:
        ValueError: if the ``date`` column is missing or ``start`` is after ``end``.
    """
    if "date" not in df.columns:
        raise ValueError("missing columns: date")
    low = pd.to_datetime(start) if start is not None else None
    high = pd.to_datetime(end) if end is not None else None
    if low is not None and high is not None and low > high:
        raise ValueError("start must not be after end")
    ordered = df.assign(date=pd.to_datetime(df["date"])).sort_values("date")
    mask = pd.Series(True, index=ordered.index)
    if low is not None:
        mask &= ordered["date"] >= low
    if high is not None:
        mask &= ordered["date"] <= high
    return ordered[mask].reset_index(drop=True)


def weekly_gains(df: pd.DataFrame) -> pd.DataFrame:
    """Return new subscribers and watch hours gained per calendar week.

    Builds on :func:`add_daily_gains` and resamples by week ending Sunday,
    so the result is indexed by ``week_ending`` with ``new_subscribers`` and
    ``new_watch_hours`` columns. Handy for weekly creator reports.

    Raises:
        ValueError: if a required column is missing.
    """
    gains = add_daily_gains(df).set_index("date")
    weekly = gains[["new_subscribers", "new_watch_hours"]].resample("W-SUN").sum()
    weekly.index.name = "week_ending"
    return weekly


def best_day(df: pd.DataFrame, column: str = "new_subscribers") -> Dict[str, object]:
    """Return the date with the largest daily gain in ``column``.

    Gains come from :func:`add_daily_gains`, so ``column`` must be
    ``new_subscribers`` or ``new_watch_hours``. Ties go to the earliest date.
    The result is ``{"date": "YYYY-MM-DD", "gain": value}``.

    Raises:
        ValueError: if ``column`` is unsupported, a required column is
            missing, or there are fewer than two rows.
    """
    if column not in ("new_subscribers", "new_watch_hours"):
        raise ValueError("column must be 'new_subscribers' or 'new_watch_hours'")
    if len(df) < 2:
        raise ValueError("need at least two rows")
    gains = add_daily_gains(df).iloc[1:]
    row = gains.loc[gains[column].idxmax()]
    return {"date": row["date"].strftime("%Y-%m-%d"), "gain": row[column].item()}


def monthly_gains(df: pd.DataFrame) -> pd.DataFrame:
    """Return new subscribers and watch hours gained per calendar month.

    The monthly counterpart of :func:`weekly_gains`: gains come from
    :func:`add_daily_gains` and are summed per month, giving a DataFrame
    indexed by ``month`` (``"YYYY-MM"`` strings) with ``new_subscribers`` and
    ``new_watch_hours`` columns. Months with no rows are omitted.

    Raises:
        ValueError: if a required column is missing.
    """
    gains = add_daily_gains(df)
    month = gains["date"].dt.strftime("%Y-%m").rename("month")
    return gains.groupby(month)[["new_subscribers", "new_watch_hours"]].sum()
