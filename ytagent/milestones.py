"""Subscriber milestones that creators commonly track."""
import math
from typing import Dict, List, Optional, Sequence, Tuple

MILESTONES = (100, 500, 1_000, 10_000, 100_000, 1_000_000, 10_000_000)


def next_milestone(subscribers: int) -> Optional[int]:
    """Return the next subscriber milestone above ``subscribers``.

    Returns ``None`` once every milestone in :data:`MILESTONES` is passed.

    Raises:
        ValueError: if ``subscribers`` is negative.
    """
    if subscribers < 0:
        raise ValueError("subscribers must be non-negative")
    for milestone in MILESTONES:
        if subscribers < milestone:
            return milestone
    return None


def milestone_progress(subscribers: int) -> Tuple[Optional[int], float]:
    """Return ``(next_milestone, percent)`` progress from the previous milestone.

    For example 750 subscribers sits between 500 and 1,000, giving
    ``(1000, 50.0)``. Past the final milestone the result is ``(None, 100.0)``.
    """
    target = next_milestone(subscribers)
    if target is None:
        return None, 100.0
    index = MILESTONES.index(target)
    previous = MILESTONES[index - 1] if index else 0
    return target, round((subscribers - previous) / (target - previous) * 100, 1)


def days_to_next_milestone(subscribers: int, subs_per_day: float) -> Optional[int]:
    """Estimate whole days until :func:`next_milestone` at a steady daily gain.

    For example 750 subscribers growing by 20 a day reach 1,000 in 13 days.
    Returns ``None`` when there is no further milestone or ``subs_per_day``
    is not positive, since the milestone would never be reached.

    Raises:
        ValueError: if ``subscribers`` is negative.
    """
    target = next_milestone(subscribers)
    if target is None or subs_per_day <= 0:
        return None
    return math.ceil((target - subscribers) / subs_per_day)


def milestones_reached(subscribers: int) -> List[int]:
    """Return every milestone in :data:`MILESTONES` already reached, ascending.

    A milestone counts as reached once ``subscribers`` equals it, so exactly
    1,000 subscribers includes ``1000``. Complements :func:`next_milestone`,
    which looks at the one still ahead.

    Raises:
        ValueError: if ``subscribers`` is negative.
    """
    if subscribers < 0:
        raise ValueError("subscribers must be non-negative")
    return [milestone for milestone in MILESTONES if subscribers >= milestone]


def milestones_between(start: int, end: int) -> List[int]:
    """Return the milestones crossed while growing from ``start`` to ``end``.

    A milestone counts when ``start < milestone <= end``, so a channel that
    was already at 1,000 subscribers does not "cross" 1,000 again. Handy for
    a weekly recap of what the channel unlocked.

    Raises:
        ValueError: if either count is negative or ``end`` is below ``start``.
    """
    if start < 0 or end < 0:
        raise ValueError("subscriber counts must be non-negative")
    if end < start:
        raise ValueError("end must not be below start")
    return [milestone for milestone in MILESTONES if start < milestone <= end]


def milestone_days(daily_subscribers: Sequence[int]) -> Dict[int, int]:
    """Map each milestone to the first day index on which it was reached.

    Only milestones crossed during the series count (see
    :func:`milestones_between`), so ``[90, 120, 480, 510]`` gives
    ``{100: 1, 500: 3}``. Subscriber dips followed by a recovery do not
    re-trigger a milestone. Useful for annotating growth charts.

    Raises:
        ValueError: if the series is empty or contains a negative count.
    """
    if not daily_subscribers:
        raise ValueError("daily_subscribers must not be empty")
    if any(count < 0 for count in daily_subscribers):
        raise ValueError("subscriber counts must be non-negative")
    reached: Dict[int, int] = {}
    high = daily_subscribers[0]
    for day, count in enumerate(daily_subscribers[1:], start=1):
        if count > high:
            for milestone in milestones_between(high, count):
                reached[milestone] = day
            high = count
    return reached
