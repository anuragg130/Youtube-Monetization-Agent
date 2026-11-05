"""Estimate ad revenue from view counts and RPM (revenue per mille)."""
import math
from typing import Dict


def estimate_revenue(monetized_views: int, rpm: float) -> float:
    """Return estimated creator revenue for ``monetized_views`` at ``rpm``.

    RPM is the revenue earned per 1,000 views after YouTube's share.

    Raises:
        ValueError: if views or RPM is negative.
    """
    if monetized_views < 0 or rpm < 0:
        raise ValueError("views and rpm must be non-negative")
    return round(monetized_views / 1000 * rpm, 2)


def effective_rpm(revenue: float, views: int) -> float:
    """Return the observed RPM given total ``revenue`` over ``views``.

    Returns 0.0 when there are no views.
    """
    if revenue < 0 or views < 0:
        raise ValueError("revenue and views must be non-negative")
    if views == 0:
        return 0.0
    return round(revenue / views * 1000, 2)


def revenue_range(monetized_views: int, low_rpm: float, high_rpm: float) -> Dict[str, float]:
    """Return low/high revenue estimates for an uncertain RPM band."""
    if low_rpm > high_rpm:
        raise ValueError("low_rpm must not exceed high_rpm")
    return {
        "low": estimate_revenue(monetized_views, low_rpm),
        "high": estimate_revenue(monetized_views, high_rpm),
    }


def views_needed_for_revenue(target_revenue: float, rpm: float) -> int:
    """Return the monetized views needed to earn ``target_revenue`` at ``rpm``.

    The inverse of :func:`estimate_revenue`, rounded up to whole views. For
    example, earning $500 at a $2.50 RPM needs 200,000 monetized views.

    Raises:
        ValueError: if the target is negative or ``rpm`` is not positive.
    """
    if target_revenue < 0:
        raise ValueError("target_revenue must be non-negative")
    if rpm <= 0:
        raise ValueError("rpm must be positive")
    return math.ceil(round(target_revenue / rpm * 1000, 6))
