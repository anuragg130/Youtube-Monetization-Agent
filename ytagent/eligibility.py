"""YouTube Partner Program eligibility checks."""

SUBSCRIBER_THRESHOLD = 1000
WATCH_HOURS_THRESHOLD = 4000


def is_eligible(subscribers: int, watch_hours_12m: float) -> bool:
    """Return True if a channel meets the standard YPP thresholds.

    Raises:
        ValueError: if either metric is negative.
    """
    if subscribers < 0 or watch_hours_12m < 0:
        raise ValueError("subscribers and watch hours must be non-negative")
    return subscribers >= SUBSCRIBER_THRESHOLD and watch_hours_12m >= WATCH_HOURS_THRESHOLD
