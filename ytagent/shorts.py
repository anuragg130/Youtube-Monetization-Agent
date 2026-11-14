"""YPP eligibility via the Shorts path (subscribers + 90-day Shorts views)."""
import math
from typing import Dict, Optional

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


def shorts_progress_percent(subscribers: int, shorts_views_90d: int) -> Dict[str, float]:
    """Return progress toward each Shorts-route threshold as a percentage.

    Mirrors :func:`ytagent.progress.progress_percent` for the Shorts path.
    Each value is capped at 100.0 and rounded to one decimal place.

    Raises:
        ValueError: if either metric is negative.
    """
    if subscribers < 0 or shorts_views_90d < 0:
        raise ValueError("subscribers and shorts views must be non-negative")
    return {
        "subscribers": round(min(100.0, subscribers / SUBSCRIBER_THRESHOLD * 100), 1),
        "shorts_views": round(min(100.0, shorts_views_90d / SHORTS_VIEWS_THRESHOLD * 100), 1),
    }


def days_to_shorts_eligibility(
    subscribers: int,
    shorts_views_90d: int,
    subs_per_day: float,
    shorts_views_per_day: float,
) -> Optional[int]:
    """Estimate whole days until both Shorts-route thresholds are met.

    The Shorts counterpart of :func:`ytagent.progress.days_to_eligibility`.
    Assumes steady daily growth and ignores views ageing out of the 90-day
    window. Returns 0 if already eligible, or ``None`` when a remaining gap
    has a zero growth rate and would never close.

    Raises:
        ValueError: if any metric or growth rate is negative.
    """
    if subs_per_day < 0 or shorts_views_per_day < 0:
        raise ValueError("daily growth rates must be non-negative")
    gap = shorts_gap(subscribers, shorts_views_90d)
    days = 0
    for needed, rate in (
        (gap["subscribers_needed"], subs_per_day),
        (gap["shorts_views_needed"], shorts_views_per_day),
    ):
        if needed <= 0:
            continue
        if rate == 0:
            return None
        days = max(days, math.ceil(needed / rate))
    return days
