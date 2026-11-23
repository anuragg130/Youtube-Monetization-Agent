"""Derive growth rates from historical channel metric snapshots."""
import math
import statistics
from typing import List, Optional, Sequence, Tuple


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


def longest_decline_streak(counts: Sequence[float]) -> int:
    """Return the longest run of consecutive days where the total dropped.

    The counterpart of :func:`longest_growth_streak`: flat or rising days
    break the run, so ``[500, 498, 495, 495, 490, 489]`` gives ``2``. A long
    streak usually points at sustained churn rather than a one-off purge.

    Raises:
        ValueError: if fewer than two values are given.
    """
    best = current = 0
    for change in daily_changes(counts):
        current = current + 1 if change < 0 else 0
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


def growth_volatility(counts: Sequence[float]) -> float:
    """Return the sample standard deviation of day-over-day gains.

    A low value means steady growth; a high value means a few spikes or
    stalls dominate. Compare it with :func:`average_daily_growth` to judge
    how reliable a :func:`project_value` projection is. Two values (a single
    daily change) give ``0.0``.

    Raises:
        ValueError: if fewer than two values are given.
    """
    changes = daily_changes(counts)
    if len(changes) < 2:
        return 0.0
    return round(statistics.stdev(changes), 2)


def declining_days(counts: Sequence[float]) -> List[int]:
    """Return the indices of days where the total dropped from the day before.

    Indices point at the day the loss landed, matching :func:`peak_daily_gain`,
    so ``[500, 498, 510, 505, 505]`` gives ``[1, 3]``. Useful for spotting
    subscriber churn after a controversial upload or a bulk spam purge.

    Raises:
        ValueError: if fewer than two values are given.
    """
    return [day + 1 for day, change in enumerate(daily_changes(counts)) if change < 0]


def flat_days(counts: Sequence[float]) -> List[int]:
    """Return the indices of days where the total did not change at all.

    The counterpart of :func:`declining_days`: ``[500, 500, 510, 510, 505]``
    gives ``[1, 3]``. A run of flat days often means analytics stopped
    updating or the channel went quiet between uploads.

    Raises:
        ValueError: if fewer than two values are given.
    """
    return [day + 1 for day, change in enumerate(daily_changes(counts)) if change == 0]


def positive_day_share(counts: Sequence[float]) -> float:
    """Return the percentage of day-over-day changes that were gains.

    ``[100, 110, 108, 120, 120]`` has two gains in four changes, giving
    ``50.0``. Complements :func:`declining_days` and :func:`flat_days` with a
    single consistency score that is easy to track week to week.

    Raises:
        ValueError: if fewer than two values are given.
    """
    changes = daily_changes(counts)
    gains = sum(1 for change in changes if change > 0)
    return round(gains / len(changes) * 100, 2)


def best_week(daily_values: Sequence[float], week_length: int = 7) -> Tuple[int, float]:
    """Return ``(week_index, total)`` for the strongest week of daily values.

    Weeks are built with :func:`weekly_totals`, so a trailing partial week
    is considered too. ``week_index`` is zero-based; ties keep the earliest
    week. Handy for finding which upload week drove the most new subscribers.

    Raises:
        ValueError: if ``daily_values`` is empty or ``week_length`` < 1.
    """
    totals = weekly_totals(daily_values, week_length)
    index = max(range(len(totals)), key=lambda i: totals[i])
    return index, totals[index]


def worst_week(daily_values: Sequence[float], week_length: int = 7) -> Tuple[int, float]:
    """Return ``(week_index, total)`` for the weakest week of daily values.

    The counterpart of :func:`best_week`: weeks come from
    :func:`weekly_totals` (a trailing partial week included), the index is
    zero-based and ties keep the earliest week. Note that a short trailing
    week naturally has a lower total, so trim it first if that matters.

    Raises:
        ValueError: if ``daily_values`` is empty or ``week_length`` < 1.
    """
    totals = weekly_totals(daily_values, week_length)
    index = min(range(len(totals)), key=lambda i: totals[i])
    return index, totals[index]


def largest_daily_drop(counts: Sequence[float]) -> Tuple[int, float]:
    """Return ``(day_index, change)`` for the biggest day-over-day decrease.

    The counterpart of :func:`peak_daily_gain`: ``day_index`` points at the
    day the loss landed, so ``[500, 498, 470, 480]`` gives ``(2, -28)``. If
    the total never fell, the smallest change is returned (zero or positive),
    so callers can check ``change < 0``. Ties keep the earliest day.

    Raises:
        ValueError: if fewer than two values are given.
    """
    changes = daily_changes(counts)
    worst = min(range(len(changes)), key=lambda i: changes[i])
    return worst + 1, changes[worst]


def days_since_peak(counts: Sequence[float]) -> int:
    """Return how many days have passed since the series hit its highest value.

    ``0`` means the latest value is the (joint) all-time high, so the channel
    is still at its peak. ``[100, 140, 130, 120]`` gives ``2``. When the peak
    value occurs more than once, the most recent occurrence is used.

    Raises:
        ValueError: if ``counts`` is empty.
    """
    if not counts:
        raise ValueError("counts must not be empty")
    peak = max(counts)
    last_peak = max(i for i, value in enumerate(counts) if value == peak)
    return len(counts) - 1 - last_peak


def max_drawdown_percent(counts: Sequence[float]) -> float:
    """Return the largest peak-to-trough fall in ``counts`` as a percentage.

    Measures the worst setback relative to the running high, e.g. a channel
    that peaked at 1,000 subscribers and later dipped to 900 has a drawdown
    of ``10.0``. ``[800, 1000, 950, 900, 1100]`` gives ``10.0``. A series that
    never falls below a previous high returns ``0.0``.

    Raises:
        ValueError: if ``counts`` is empty or contains a non-positive value.
    """
    if not counts:
        raise ValueError("counts must not be empty")
    if any(value <= 0 for value in counts):
        raise ValueError("all values must be positive")
    running_high = counts[0]
    worst = 0.0
    for value in counts:
        running_high = max(running_high, value)
        worst = max(worst, (running_high - value) / running_high * 100)
    return round(worst, 2)


def growth_acceleration(counts: Sequence[float]) -> float:
    """Return how much the average daily gain changed between halves of ``counts``.

    The daily changes are split into an earlier and a later half (the middle
    change is dropped when the count is odd) and the earlier average is
    subtracted from the later one. A positive result means growth is speeding
    up: ``[100, 110, 120, 140, 160]`` gives ``10.0`` (gains of 10 then 20).

    Raises:
        ValueError: if ``counts`` has fewer than three values.
    """
    if len(counts) < 3:
        raise ValueError("need at least three values to measure acceleration")
    changes = daily_changes(counts)
    half = len(changes) // 2
    earlier = changes[:half]
    later = changes[-half:]
    return round(statistics.mean(later) - statistics.mean(earlier), 2)


def longest_drawdown_days(counts: Sequence[float]) -> int:
    """Return the longest run of consecutive days spent below a previous high.

    Complements :func:`max_drawdown_percent`, which measures how deep the
    worst setback was, by measuring how long the channel stayed under water.
    A day counts as recovered once the value reaches the running high again.
    ``[100, 120, 110, 115, 125, 90]`` gives ``2``; a series that only ever
    rises or stays flat gives ``0``.

    Raises:
        ValueError: if ``counts`` is empty.
    """
    if not counts:
        raise ValueError("counts must not be empty")
    running_high = counts[0]
    current = longest = 0
    for value in counts:
        if value >= running_high:
            running_high = value
            current = 0
        else:
            current += 1
            longest = max(longest, current)
    return longest


def above_average_days(counts: Sequence[float]) -> List[int]:
    """Return indices of daily changes that beat the mean daily gain.

    Index ``i`` refers to the change from ``counts[i]`` to ``counts[i + 1]``,
    matching :func:`declining_days`. Useful for finding which uploads or
    promotions drove unusually strong days.

    Raises:
        ValueError: if fewer than two daily values are given.
    """
    changes = daily_changes(counts)
    mean = statistics.mean(changes)
    return [i for i, change in enumerate(changes) if change > mean]


def below_average_days(counts: Sequence[float]) -> List[int]:
    """Return indices of daily changes that fall short of the mean daily gain.

    The counterpart to :func:`above_average_days`; index ``i`` refers to the
    change from ``counts[i]`` to ``counts[i + 1]``. Useful for spotting
    weak days worth investigating (missed uploads, algorithm dips).

    Raises:
        ValueError: if fewer than two daily values are given.
    """
    changes = daily_changes(counts)
    mean = statistics.mean(changes)
    return [i for i, change in enumerate(changes) if change < mean]


def daily_percent_changes(counts: Sequence[float]) -> List[float]:
    """Return the day-over-day percentage change for each pair of values.

    ``[100, 110, 99]`` gives ``[10.0, -10.0]``. Unlike :func:`daily_changes`,
    the result is comparable across small and large channels.

    Raises:
        ValueError: if fewer than two values are given or any value other
            than the last is not positive.
    """
    if len(counts) < 2:
        raise ValueError("need at least two daily values")
    if any(value <= 0 for value in counts[:-1]):
        raise ValueError("values used as a baseline must be positive")
    return [round((later - earlier) / earlier * 100, 2) for earlier, later in zip(counts, counts[1:])]


def recent_average_growth(counts: Sequence[float], days: int = 7) -> float:
    """Return the mean daily gain over only the last ``days`` changes.

    The whole-history :func:`average_daily_growth` can hide a recent
    slowdown or surge; this looks at the trailing window instead. If fewer
    than ``days`` changes exist, all of them are used.

    Raises:
        ValueError: if ``days`` is not positive or fewer than two values are given.
    """
    if days <= 0:
        raise ValueError("days must be positive")
    changes = daily_changes(counts)
    return round(statistics.mean(changes[-days:]), 2)


def growth_momentum(counts: Sequence[float], days: int = 7) -> float:
    """Compare the average gain of the last ``days`` changes with the ``days`` before.

    Returns the percent change between the two windows' mean daily gains:
    ``25.0`` means the channel is growing a quarter faster than in the
    previous window, a negative value means it has slowed. Extends
    :func:`recent_average_growth` with a built-in point of comparison.

    Raises:
        ValueError: if ``days`` is not positive, there are fewer than
            ``2 * days`` daily changes, or the earlier window's mean is not positive.
    """
    if days <= 0:
        raise ValueError("days must be positive")
    changes = daily_changes(counts)
    if len(changes) < 2 * days:
        raise ValueError("need at least two full windows of daily changes")
    recent = statistics.mean(changes[-days:])
    previous = statistics.mean(changes[-2 * days:-days])
    if previous <= 0:
        raise ValueError("previous window must have a positive average gain")
    return round((recent - previous) / previous * 100, 2)


def doubling_time_days(counts: Sequence[float]) -> Optional[float]:
    """Return how many days the channel takes to double at its compounded pace.

    Uses the same compounded rate as :func:`compound_daily_growth_rate` but
    without rounding, so ``[1000, 1100, 1210]`` (10% a day) gives ``7.27``.
    Returns ``None`` when the series did not grow, since it will never double.

    Raises:
        ValueError: if fewer than two values are given or any value is not positive.
    """
    if len(counts) < 2:
        raise ValueError("need at least two daily values")
    if min(counts) <= 0:
        raise ValueError("all values must be positive")
    if counts[-1] <= counts[0]:
        return None
    daily_factor = (counts[-1] / counts[0]) ** (1 / (len(counts) - 1))
    return round(math.log(2) / math.log(daily_factor), 2)


def days_to_multiple(counts: Sequence[float], multiple: float = 2.0) -> Optional[float]:
    """Return how many days the channel takes to grow by ``multiple`` times.

    Generalises :func:`doubling_time_days` to any target ratio, e.g.
    ``multiple=10`` for "how long until ten times the audience" at the
    compounded pace seen so far. Returns ``None`` when the series did not grow.

    Raises:
        ValueError: if ``multiple`` is not above 1, fewer than two values are
            given, or any value is not positive.
    """
    if multiple <= 1:
        raise ValueError("multiple must be greater than 1")
    if len(counts) < 2:
        raise ValueError("need at least two daily values")
    if min(counts) <= 0:
        raise ValueError("all values must be positive")
    if counts[-1] <= counts[0]:
        return None
    daily_factor = (counts[-1] / counts[0]) ** (1 / (len(counts) - 1))
    return round(math.log(multiple) / math.log(daily_factor), 2)
