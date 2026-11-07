"""YPP eligibility via the Shorts path (subscribers + 90-day Shorts views)."""
from typing import Dict

from ytagent.eligibility import SUBSCRIBER_THRESHOLD

SHORTS_VIEWS_THRESHOLD = 10_000_000


def is_shorts_eligible(subscribers: int, shorts_views_90d: int) -> bool:
    """Return True if a channel qualifies through the Shorts route.

    The Shorts route needs the same 1,000 subscribers as the long-form route
    plus 10 million valid public Shorts views in the last 90 days.

    Raises:
        ValueError: if either metric is negative.
    """
    if subscribers < 0 or shorts_views_90d < 0:
        raise ValueError("subscribers and shorts views must be non-negative")
    return subscribers >= SUBSCRIBER_THRESHOLD and shorts_views_90d >= SHORTS_VIEWS_THRESHOLD


def shorts_gap(subscribers: int, shorts_views_90d: int) -> Dict[str, int]:
    """Return subscribers and Shorts views still needed (0 once met)."""
    if subscribers < 0 or shorts_views_90d < 0:
        raise ValueError("subscribers and shorts views must be non-negative")
    return {
        "subscribers_needed": max(0, SUBSCRIBER_THRESHOLD - subscribers),
        "shorts_views_needed": max(0, SHORTS_VIEWS_THRESHOLD - shorts_views_90d),
    }
