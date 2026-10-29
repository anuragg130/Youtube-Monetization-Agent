"""Track how far a channel is from YouTube Partner Program thresholds."""
from typing import Dict

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
