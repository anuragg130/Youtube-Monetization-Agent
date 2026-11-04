"""Audience engagement metrics derived from per-video statistics."""


def engagement_rate(likes: int, comments: int, views: int) -> float:
    """Return (likes + comments) as a percentage of ``views``.

    Returns 0.0 when there are no views.

    Raises:
        ValueError: if any count is negative.
    """
    if likes < 0 or comments < 0 or views < 0:
        raise ValueError("likes, comments and views must be non-negative")
    if views == 0:
        return 0.0
    return round((likes + comments) / views * 100, 2)


def subscriber_conversion_rate(new_subscribers: int, views: int) -> float:
    """Return new subscribers gained per 1,000 views.

    Useful alongside :func:`ytagent.progress.days_to_eligibility` to judge
    how efficiently views turn into subscribers. Returns 0.0 with no views.
    """
    if new_subscribers < 0 or views < 0:
        raise ValueError("new_subscribers and views must be non-negative")
    if views == 0:
        return 0.0
    return round(new_subscribers / views * 1000, 2)
