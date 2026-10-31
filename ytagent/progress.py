"""Track how far a channel is from YouTube Partner Program thresholds."""
import math
from typing import Dict, Optional

from ytagent.eligibility import SUBSCRIBER_THRESHOLD, WATCH_HOURS_THRESHOLD


def eligibility_gap(subscribers: int, watch_hours_12m: float) -> Dict[str, float]:
    """Return the subscribers and watch hours still needed (0 when met)."""
    return {
        "subscribers_needed": max(0, SUBSCRIBER_THRESHOLD - subscribers),
        "watch_hours_needed": max(0.0, WATCH_HOURS_THRESHOLD - watch_hours_12m),
    }


def progress_percent(subscribers: int, watch_hours_12m: float) -> Dict[str, float]:
    """Return percentage progress toward each threshold, capped at 100."""
    return {
        "subscribers": round(min(100.0, subscribers / SUBSCRIBER_THRESHOLD * 100), 1),
        "watch_hours": round(min(100.0, watch_hours_12m / WATCH_HOURS_THRESHOLD * 100), 1),
    }


def days_to_eligibility(
    subscribers: int,
    watch_hours_12m: float,
    subs_per_day: float,
    watch_hours_per_day: float,
) -> Optional[int]:
    """Estimate whole days until both YPP thresholds are met at steady growth.

    Returns 0 if the channel already qualifies, or ``None`` if a remaining gap
    can never close because its daily growth rate is zero.

    Raises:
        ValueError: if either growth rate is negative.
    """
    if subs_per_day < 0 or watch_hours_per_day < 0:
        raise ValueError("daily growth rates must be non-negative")
    gap = eligibility_gap(subscribers, watch_hours_12m)
    days = 0
    for needed, rate in (
        (gap["subscribers_needed"], subs_per_day),
        (gap["watch_hours_needed"], watch_hours_per_day),
    ):
        if needed <= 0:
            continue
        if rate == 0:
            return None
        days = max(days, math.ceil(needed / rate))
    return days
