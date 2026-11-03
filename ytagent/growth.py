"""Derive growth rates from historical channel metric snapshots."""
import statistics
from typing import List, Sequence


def daily_changes(counts: Sequence[float]) -> List[float]:
    """Return day-over-day differences for a series of daily totals."""
    if len(counts) < 2:
        raise ValueError("need at least two daily values")
    return [later - earlier for earlier, later in zip(counts, counts[1:])]


def average_daily_growth(counts: Sequence[float]) -> float:
    """Return the mean daily gain across ``counts`` (may be negative).

    The result can be fed into :func:`ytagent.progress.days_to_eligibility`.
    """
    return round(statistics.mean(daily_changes(counts)), 2)


def median_daily_growth(counts: Sequence[float]) -> float:
    """Return the median daily gain, which is robust to one-off viral spikes."""
    return round(statistics.median(daily_changes(counts)), 2)
