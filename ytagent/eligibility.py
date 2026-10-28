"""YouTube Partner Program eligibility checks."""

SUBSCRIBER_THRESHOLD = 1000
WATCH_HOURS_THRESHOLD = 4000


def is_eligible(subscribers: int, watch_hours_12m: float) -> bool:
    """Return True if a channel meets the standard YPP thresholds."""
    return subscribers >= SUBSCRIBER_THRESHOLD and watch_hours_12m >= WATCH_HOURS_THRESHOLD
