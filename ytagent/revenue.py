"""Estimate ad revenue from view counts and RPM (revenue per mille)."""
import math
from decimal import ROUND_HALF_UP, Decimal
from typing import Dict, List, Mapping, Optional, Sequence, Tuple


def estimate_revenue(monetized_views: int, rpm: float) -> float:
    """Return estimated creator revenue for ``monetized_views`` at ``rpm``.

    RPM is the revenue earned per 1,000 views after YouTube's share.

    Raises:
        ValueError: if views or RPM is negative.
    """
    if monetized_views < 0 or rpm < 0:
        raise ValueError("views and rpm must be non-negative")
    return round(monetized_views / 1000 * rpm, 2)


def rpm_needed_for_target(target_revenue: float, monetized_views: int) -> float:
    """Return the RPM required to earn ``target_revenue`` from ``monetized_views``.

    The inverse of :func:`estimate_revenue` for a fixed view count: earning
    $250 from 50,000 monetized views needs an RPM of ``5.0``. Compare the
    result with your channel's :func:`effective_rpm` to see whether a revenue
    goal is realistic without more views.

    Raises:
        ValueError: if the target is negative or views are not positive.
    """
    if target_revenue < 0:
        raise ValueError("target_revenue must be non-negative")
    if monetized_views <= 0:
        raise ValueError("monetized_views must be positive")
    return round(target_revenue / monetized_views * 1000, 2)


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


def project_monthly_revenue(daily_views: float, rpm: float, monetized_share: float = 1.0, days: int = 30) -> float:
    """Project revenue over ``days`` from an average daily view count.

    ``monetized_share`` is the fraction of views that carry ads (0-1), since
    not every playback is monetized. For example 2,000 daily views at a $3 RPM
    with 60% monetized views gives ``108.0`` over 30 days.

    Raises:
        ValueError: if inputs are negative, ``days`` < 1, or the share exceeds 1.
    """
    if daily_views < 0:
        raise ValueError("daily_views must be non-negative")
    if not 0 <= monetized_share <= 1:
        raise ValueError("monetized_share must be between 0 and 1")
    if days < 1:
        raise ValueError("days must be at least 1")
    return estimate_revenue(round(daily_views * monetized_share * days), rpm)


def rpm_from_cpm(cpm: float, creator_share: float = 0.55, monetized_share: float = 1.0) -> float:
    """Estimate RPM from an advertiser CPM.

    CPM is what advertisers pay per 1,000 ad impressions; RPM is what the
    creator earns per 1,000 views. YouTube's standard long-form split gives
    creators 55% of ad revenue, and only ``monetized_share`` of views show
    ads. For example a $10 CPM with 60% monetized views gives an RPM of 3.3.

    Raises:
        ValueError: if ``cpm`` is negative or a share is outside ``[0, 1]``.
    """
    if cpm < 0:
        raise ValueError("cpm must be non-negative")
    if not 0 <= creator_share <= 1 or not 0 <= monetized_share <= 1:
        raise ValueError("shares must be between 0 and 1")
    return round(cpm * creator_share * monetized_share, 2)


def break_even_daily_views(monthly_costs: float, rpm: float, monetized_share: float = 1.0, days: int = 30) -> int:
    """Return the average daily views needed to cover ``monthly_costs``.

    The inverse of :func:`project_monthly_revenue`: useful for checking
    whether editing, gear or software spend is covered by ad revenue. For
    example $300 of monthly costs at a $3 RPM with 50% monetized views needs
    6,667 views a day over 30 days.

    Raises:
        ValueError: if costs are negative, ``rpm`` is not positive,
            ``monetized_share`` is not in ``(0, 1]`` or ``days`` < 1.
    """
    if not 0 < monetized_share <= 1:
        raise ValueError("monetized_share must be greater than 0 and at most 1")
    if days < 1:
        raise ValueError("days must be at least 1")
    monetized_needed = views_needed_for_revenue(monthly_costs, rpm)
    return math.ceil(round(monetized_needed / monetized_share / days, 6))


def revenue_per_subscriber(revenue: float, subscribers: int) -> float:
    """Return average ``revenue`` earned per subscriber, rounded to cents.

    A rough measure of how valuable each subscriber is, useful when weighing
    a subscriber milestone against :func:`estimate_revenue`. Returns 0.0
    when the channel has no subscribers.

    Raises:
        ValueError: if revenue or subscribers is negative.
    """
    if revenue < 0 or subscribers < 0:
        raise ValueError("revenue and subscribers must be non-negative")
    if subscribers == 0:
        return 0.0
    return round(revenue / subscribers, 2)


def revenue_change_percent(previous: float, current: float) -> float:
    """Return the percentage change in revenue between two periods.

    ``revenue_change_percent(200, 250)`` gives ``25.0``; a drop gives a
    negative value. Useful for month-over-month earnings reports alongside
    :func:`project_monthly_revenue`.

    Raises:
        ValueError: if ``previous`` is not positive or ``current`` is negative.
    """
    if previous <= 0:
        raise ValueError("previous revenue must be positive")
    if current < 0:
        raise ValueError("current revenue must be non-negative")
    return round((current - previous) / previous * 100, 2)


def revenue_share_by_source(revenues: Mapping[str, float]) -> Dict[str, float]:
    """Return each revenue source's share of the total as a percentage.

    ``revenues`` maps a source name (e.g. ``"ads"``, ``"memberships"``,
    ``"super_chat"``) to its earnings. Shares are rounded to two decimals and
    returned largest first. An all-zero total gives 0.0 for every source.

    Raises:
        ValueError: if ``revenues`` is empty or any amount is negative.
    """
    if not revenues:
        raise ValueError("revenues must not be empty")
    if any(amount < 0 for amount in revenues.values()):
        raise ValueError("revenue amounts must be non-negative")
    total = sum(revenues.values())
    shares = {
        source: round(amount / total * 100, 2) if total else 0.0
        for source, amount in revenues.items()
    }
    return dict(sorted(shares.items(), key=lambda item: (-item[1], item[0])))


def revenue_per_watch_hour(revenue: float, watch_hours: float) -> float:
    """Return earnings per hour of watch time, rounded to cents.

    Long videos can have a modest RPM yet earn well per hour watched, so
    this complements :func:`effective_rpm` when comparing formats. For
    example $90 over 1,200 watch hours gives ``0.08``. Returns 0.0 when
    there is no watch time.

    Raises:
        ValueError: if revenue or watch hours is negative.
    """
    if revenue < 0 or watch_hours < 0:
        raise ValueError("revenue and watch_hours must be non-negative")
    if watch_hours == 0:
        return 0.0
    rate = Decimal(str(revenue)) / Decimal(str(watch_hours))
    return float(rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def annualized_revenue(revenue: float, days: int) -> float:
    """Scale earnings from a ``days``-long period up to a 365-day estimate.

    Lets reports covering different window lengths be compared on the same
    footing: $250 earned over 30 days annualizes to ``3041.67``.

    Raises:
        ValueError: if ``revenue`` is negative or ``days`` < 1.
    """
    if revenue < 0:
        raise ValueError("revenue must be non-negative")
    if days < 1:
        raise ValueError("days must be at least 1")
    return round(revenue / days * 365, 2)


def daily_revenue_needed(target_revenue: float, earned_so_far: float, days_remaining: int) -> float:
    """Return the average daily revenue required to hit ``target_revenue``.

    Useful mid-month: with a $500 goal, $320 already earned and 9 days left,
    the channel needs ``20.0`` per day. Returns ``0.0`` once the target has
    already been reached.

    Raises:
        ValueError: if any amount is negative or ``days_remaining`` < 1.
    """
    if target_revenue < 0 or earned_so_far < 0:
        raise ValueError("revenue amounts must be non-negative")
    if days_remaining < 1:
        raise ValueError("days_remaining must be at least 1")
    shortfall = max(target_revenue - earned_so_far, 0.0)
    return round(shortfall / days_remaining, 2)


def cumulative_revenue(daily_revenues: Sequence[float]) -> List[float]:
    """Return the running total of ``daily_revenues``.

    Handy for plotting month-to-date earnings: ``[10, 12.5, 7.25]`` gives
    ``[10.0, 22.5, 29.75]``. An empty sequence yields an empty list.

    Raises:
        ValueError: if any daily amount is negative.
    """
    totals: List[float] = []
    running = 0.0
    for amount in daily_revenues:
        if amount < 0:
            raise ValueError("daily revenues must be non-negative")
        running += amount
        totals.append(round(running, 2))
    return totals


def payout_day(daily_revenues: Sequence[float], threshold: float = 100.0) -> Optional[int]:
    """Return the 0-based day on which earnings first reach ``threshold``.

    AdSense only pays out once the balance hits a minimum (US$100 by
    default), so this tells a new channel which day of an export crossed
    it. Built on :func:`cumulative_revenue`: ``[40, 35, 30]`` reaches 100
    on day ``2``. Returns ``None`` if the threshold is never reached.

    Raises:
        ValueError: if ``threshold`` is not positive or any amount is negative.
    """
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    for day, total in enumerate(cumulative_revenue(daily_revenues)):
        if total >= threshold:
            return day
    return None


def rpm_by_video(videos: Sequence[Mapping[str, float]]) -> Dict[str, float]:
    """Return each video's observed RPM plus the view-weighted channel RPM.

    Each mapping needs ``title``, ``revenue`` and ``views`` keys. Per-video
    values come from :func:`effective_rpm`; the extra ``"__overall__"`` entry
    divides total revenue by total views, so heavily viewed videos count
    more than a simple average of the per-video RPMs would.

    Raises:
        ValueError: if ``videos`` is empty, a key is missing, a title repeats,
            or any revenue or view count is negative.
    """
    if not videos:
        raise ValueError("videos must not be empty")
    rpms: Dict[str, float] = {}
    total_revenue = 0.0
    total_views = 0
    for video in videos:
        try:
            title, revenue, views = video["title"], video["revenue"], int(video["views"])
        except KeyError as exc:
            raise ValueError(f"video is missing {exc.args[0]!r}") from None
        if title in rpms:
            raise ValueError(f"duplicate video title {title!r}")
        rpms[str(title)] = effective_rpm(revenue, views)
        total_revenue += revenue
        total_views += views
    rpms["__overall__"] = effective_rpm(total_revenue, total_views)
    return rpms


def projected_period_revenue(earned_so_far: float, days_elapsed: int, days_in_period: int = 30) -> float:
    """Extrapolate end-of-period revenue from the pace so far.

    Assumes the remaining days earn at the same average rate as the elapsed
    ones: $320 after 21 of 30 days projects ``457.14``. Compare the result
    with a goal, or use :func:`daily_revenue_needed` to see the required pace.

    Raises:
        ValueError: if ``earned_so_far`` is negative, ``days_elapsed`` < 1,
            or ``days_elapsed`` exceeds ``days_in_period``.
    """
    if earned_so_far < 0:
        raise ValueError("earned_so_far must be non-negative")
    if days_elapsed < 1:
        raise ValueError("days_elapsed must be at least 1")
    if days_elapsed > days_in_period:
        raise ValueError("days_elapsed cannot exceed days_in_period")
    return round(earned_so_far / days_elapsed * days_in_period, 2)


def best_revenue_day(daily_revenues: Sequence[float]) -> Tuple[int, float]:
    """Return the 0-based index and amount of the highest-earning day.

    Ties go to the earliest day, so ``[12.0, 30.5, 30.5]`` gives
    ``(1, 30.5)``. Pair it with :func:`cumulative_revenue` to see how much a
    single viral day contributed to the period total.

    Raises:
        ValueError: if ``daily_revenues`` is empty or any amount is negative.
    """
    if not daily_revenues:
        raise ValueError("daily_revenues must not be empty")
    if any(amount < 0 for amount in daily_revenues):
        raise ValueError("daily revenues must be non-negative")
    best = max(range(len(daily_revenues)), key=lambda day: (daily_revenues[day], -day))
    return best, float(daily_revenues[best])


def worst_revenue_day(daily_revenues: Sequence[float]) -> Tuple[int, float]:
    """Return the 0-based index and amount of the lowest-earning day.

    The counterpart to :func:`best_revenue_day`; ties go to the earliest day,
    so ``[5.0, 1.5, 1.5]`` gives ``(1, 1.5)``.

    Raises:
        ValueError: if ``daily_revenues`` is empty or any amount is negative.
    """
    if not daily_revenues:
        raise ValueError("daily_revenues must not be empty")
    if any(amount < 0 for amount in daily_revenues):
        raise ValueError("daily revenues must be non-negative")
    worst = min(range(len(daily_revenues)), key=lambda day: (daily_revenues[day], day))
    return worst, float(daily_revenues[worst])


def top_days_revenue_share(daily_revenues: Sequence[float], n: int = 3) -> float:
    """Return the percentage of total revenue earned on the ``n`` best days.

    A high share means earnings hinge on a few spikes rather than steady
    income: ``[10.0, 10.0, 80.0]`` with ``n=1`` gives ``80.0``. Returns 0.0
    when total revenue is zero. ``n`` larger than the number of days simply
    covers every day.

    Raises:
        ValueError: if ``n`` is below 1 or any amount is negative.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if any(amount < 0 for amount in daily_revenues):
        raise ValueError("daily revenues must be non-negative")
    total = sum(daily_revenues)
    if total == 0:
        return 0.0
    top = sum(sorted(daily_revenues, reverse=True)[:n])
    return round(top / total * 100, 2)


def longest_earning_streak(daily_revenues: Sequence[float], threshold: float = 0.01) -> int:
    """Return the longest run of consecutive days earning at least ``threshold``.

    Measures how consistently a channel earns rather than how much: with the
    default one-cent threshold, ``[3.0, 0.0, 2.0, 4.5, 1.0]`` gives ``3``.
    Raise ``threshold`` to ask, for example, how many days in a row the
    channel cleared $10. An empty sequence gives ``0``.

    Raises:
        ValueError: if ``threshold`` is negative or any amount is negative.
    """
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    longest = current = 0
    for amount in daily_revenues:
        if amount < 0:
            raise ValueError("daily revenues must be non-negative")
        current = current + 1 if amount >= threshold else 0
        longest = max(longest, current)
    return longest


def trailing_revenue_totals(daily_revenues: Sequence[float], window: int = 28) -> List[float]:
    """Return the revenue earned over each trailing ``window``-day period.

    Mirrors the "last 28 days" figure YouTube Studio reports, but for every
    day in the series, so you can see how that headline number moved over
    time. The result has one value per full window, in day order:
    ``[1.0, 2.0, 3.0, 4.0]`` with ``window=2`` gives ``[3.0, 5.0, 7.0]``.
    A series shorter than ``window`` gives an empty list.

    Raises:
        ValueError: if ``window`` is below 1 or any amount is negative.
    """
    if window < 1:
        raise ValueError("window must be at least 1")
    if any(amount < 0 for amount in daily_revenues):
        raise ValueError("daily revenues must be non-negative")
    values = [float(amount) for amount in daily_revenues]
    if len(values) < window:
        return []
    totals = [sum(values[:window])]
    for day in range(window, len(values)):
        totals.append(totals[-1] + values[day] - values[day - window])
    return [round(total, 2) for total in totals]
