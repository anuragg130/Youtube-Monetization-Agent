"""Subscriber milestones that creators commonly track."""
from typing import Optional, Tuple

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
