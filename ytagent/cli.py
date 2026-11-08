"""Command-line report of a channel's YouTube Partner Program readiness.

Example::

    python -m ytagent.cli 710 2500 --subs-per-day 22.5 --hours-per-day 40
"""
import argparse
from typing import List, Optional

from ytagent.eligibility import is_eligible
from ytagent.progress import days_to_eligibility, eligibility_gap, progress_percent
from ytagent.revenue import project_monthly_revenue
from ytagent.shorts import is_shorts_eligible, shorts_gap


def build_report(subscribers: int, watch_hours: float, subs_per_day: float = 0.0, hours_per_day: float = 0.0) -> str:
    """Return a short multi-line readiness report for the given metrics."""
    if is_eligible(subscribers, watch_hours):
        return "Eligible for the YouTube Partner Program."
    gap = eligibility_gap(subscribers, watch_hours)
    pct = progress_percent(subscribers, watch_hours)
    lines = [
        "Not yet eligible.",
        f"Subscribers: {pct['subscribers']}% ({gap['subscribers_needed']} needed)",
        f"Watch hours: {pct['watch_hours']}% ({gap['watch_hours_needed']} needed)",
    ]
    if subs_per_day or hours_per_day:
        days = days_to_eligibility(subscribers, watch_hours, subs_per_day, hours_per_day)
        lines.append("Estimated days: never at current rates" if days is None else f"Estimated days: {days}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Check YPP monetization readiness.")
    parser.add_argument("subscribers", type=int)
    parser.add_argument("watch_hours", type=float, help="public watch hours in the last 12 months")
    parser.add_argument("--subs-per-day", type=float, default=0.0)
    parser.add_argument("--hours-per-day", type=float, default=0.0)
    parser.add_argument("--daily-views", type=float, help="average daily views for a revenue projection")
    parser.add_argument("--rpm", type=float, default=2.0, help="revenue per 1,000 monetized views")
    parser.add_argument("--monetized-share", type=float, default=1.0)
    parser.add_argument("--shorts-views", type=int, help="public Shorts views in the last 90 days")
    args = parser.parse_args(argv)
    print(build_report(args.subscribers, args.watch_hours, args.subs_per_day, args.hours_per_day))
    if args.shorts_views is not None:
        if is_shorts_eligible(args.subscribers, args.shorts_views):
            print("Shorts route: eligible")
        else:
            needed = shorts_gap(args.subscribers, args.shorts_views)["shorts_views_needed"]
            print(f"Shorts route: {needed:,} more Shorts views needed")
    if args.daily_views is not None:
        monthly = project_monthly_revenue(args.daily_views, args.rpm, args.monetized_share)
        print(f"Projected 30-day revenue: ${monthly:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
