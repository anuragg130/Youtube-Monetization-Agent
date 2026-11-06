"""Derive growth rates from historical channel metric snapshots."""
import statistics
from typing import List, Sequence, Tuple


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


def percent_growth(counts: Sequence[float]) -> float:
    """Return the overall percentage change from the first to the last value.

    For example ``[800, 1000]`` gives ``25.0``. Useful for summarising how
    quickly subscribers or watch hours grew over a reporting window.

    Raises:
        ValueError: if fewer than two values are given or the first is not positive.
    """
    if len(counts) < 2:
        raise ValueError("need at least two daily values")
    if counts[0] <= 0:
        raise ValueError("first value must be positive")
    return round((counts[-1] - counts[0]) / counts[0] * 100, 2)


def rolling_average(counts: Sequence[float], window: int = 7) -> List[float]:
    """Return the trailing moving average of ``counts`` over ``window`` days.

    Smooths noisy daily totals (e.g. views or new subscribers) so that
    weekly trends are easier to spot. The result has
    ``len(counts) - window + 1`` values.

    Raises:
        ValueError: if ``window`` is not positive or exceeds the series length.
    """
    if window < 1:
        raise ValueError("window must be at least 1")
    if window > len(counts):
        raise ValueError("window must not exceed the number of values")
    return [
        round(statistics.mean(counts[i : i + window]), 2)
        for i in range(len(counts) - window + 1)
    ]


def peak_daily_gain(counts: Sequence[float]) -> Tuple[int, float]:
    """Return ``(day_index, gain)`` for the largest day-over-day increase.

    ``day_index`` refers to the position in ``counts`` where the gain landed,
    so ``[100, 105, 180, 190]`` gives ``(2, 75)``. Useful for spotting the
    upload or shout-out that drove a growth spike. Ties keep the earliest day.

    Raises:
        ValueError: if fewer than two values are given.
    """
    changes = daily_changes(counts)
    best = max(range(len(changes)), key=lambda i: changes[i])
    return best + 1, changes[best]
