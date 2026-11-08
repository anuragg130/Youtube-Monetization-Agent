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


def weekly_totals(daily_values: Sequence[float], week_length: int = 7) -> List[float]:
    """Sum daily values (e.g. new subscribers or views) into consecutive weeks.

    A trailing partial week is included as its own total, so 10 days of data
    produce two values: days 1-7 and days 8-10.

    Raises:
        ValueError: if ``daily_values`` is empty or ``week_length`` < 1.
    """
    if not daily_values:
        raise ValueError("daily_values must not be empty")
    if week_length < 1:
        raise ValueError("week_length must be at least 1")
    return [
        round(sum(daily_values[i : i + week_length]), 2)
        for i in range(0, len(daily_values), week_length)
    ]


def longest_growth_streak(counts: Sequence[float]) -> int:
    """Return the longest run of consecutive days with a positive gain.

    Flat or declining days break the streak, so ``[10, 12, 15, 15, 18]``
    gives ``2``. A quick consistency signal to pair with
    :func:`average_daily_growth`, which can hide stalls behind one big day.

    Raises:
        ValueError: if fewer than two values are given.
    """
    best = current = 0
    for change in daily_changes(counts):
        current = current + 1 if change > 0 else 0
        best = max(best, current)
    return best


def project_value(counts: Sequence[float], days_ahead: int) -> float:
    """Linearly project a cumulative total ``days_ahead`` days past the last value.

    Uses :func:`average_daily_growth` as the slope, so ``[620, 640, 655, 690, 710]``
    projected 10 days ahead gives ``935.0``. Handy for "where will we be next
    month?" estimates of subscribers or watch hours.

    Raises:
        ValueError: if fewer than two values are given or ``days_ahead`` is negative.
    """
    if days_ahead < 0:
        raise ValueError("days_ahead must be non-negative")
    return round(counts[-1] + average_daily_growth(counts) * days_ahead, 2)


def compound_daily_growth_rate(counts: Sequence[float]) -> float:
    """Return the average compounded daily growth rate as a percentage.

    Unlike :func:`percent_growth`, this spreads the overall change evenly
    across each day, so ``[1000, 1100, 1210]`` gives ``10.0``. It is the
    daily equivalent of CAGR and is useful for comparing windows of
    different lengths.

    Raises:
        ValueError: if fewer than two values are given or any value is not positive.
    """
    if len(counts) < 2:
        raise ValueError("need at least two daily values")
    if min(counts) <= 0:
        raise ValueError("all values must be positive")
    days = len(counts) - 1
    return round(((counts[-1] / counts[0]) ** (1 / days) - 1) * 100, 2)
