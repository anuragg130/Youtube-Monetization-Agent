# YouTube Monetization Agent

Python toolkit for analysing YouTube channel metrics and estimating monetization readiness.

## Usage

```python
from ytagent.eligibility import is_eligible
from ytagent.growth import average_daily_growth, percent_growth
from ytagent.progress import days_to_eligibility, eligibility_gap
from ytagent.revenue import revenue_range

subs_history = [620, 640, 655, 690, 710]
print(is_eligible(710, 2500))                   # False
print(eligibility_gap(710, 2500))               # {'subscribers_needed': 290, 'watch_hours_needed': 1500}
print(percent_growth(subs_history))             # 14.52
rate = average_daily_growth(subs_history)       # 22.5
print(days_to_eligibility(710, 2500, rate, 40)) # 38
print(revenue_range(50_000, 1.5, 4.0))          # {'low': 75.0, 'high': 200.0}
```

### Smoothing and engagement

```python
from ytagent.engagement import channel_engagement_rate
from ytagent.growth import peak_daily_gain, rolling_average

subs_history = [620, 640, 655, 690, 710]
print(rolling_average(subs_history, window=3))  # [638.33, 661.67, 685]
print(peak_daily_gain(subs_history))            # (3, 35) -> biggest jump landed on day 3

videos = [
    {"likes": 120, "comments": 30, "views": 4000},
    {"likes": 45, "comments": 5, "views": 1000},
]
print(channel_engagement_rate(videos))          # 4.0 (% of views, weighted by views)
```

### Forecasting and weekly roll-ups

```python
from ytagent.growth import weekly_totals
from ytagent.revenue import project_monthly_revenue

new_subs = [12, 15, 9, 20, 18, 25, 30, 22, 19, 24]
print(weekly_totals(new_subs))                                # [129, 65] (last week is partial)
print(project_monthly_revenue(2000, 3.0, monetized_share=0.6))  # 108.0
```

### Milestones and analytics exports

```python
import pandas as pd
from ytagent.frame import summarize_daily_frame
from ytagent.milestones import milestone_progress

print(milestone_progress(710))  # (1000, 42.0) -> 42% of the way from 500 to 1,000

df = pd.DataFrame({
    "date": ["2026-11-01", "2026-11-02", "2026-11-03"],
    "subscribers": [690, 700, 710],
    "watch_hours": [2420.0, 2460.0, 2500.0],
})
print(summarize_daily_frame(df))
# {'days': 2, 'subscribers': 710, 'watch_hours': 2500.0, 'subs_per_day': 10, 'hours_per_day': 40.0}
```

### Shorts route and daily gains

```python
from ytagent.frame import add_daily_gains, best_day
from ytagent.shorts import is_shorts_eligible, shorts_gap, shorts_progress_percent

print(is_shorts_eligible(1200, 8_000_000))  # False
print(shorts_gap(1200, 8_000_000))          # {'subscribers_needed': 0, 'shorts_views_needed': 2000000}
print(shorts_progress_percent(1200, 8_000_000))  # {'subscribers': 100.0, 'shorts_views': 80.0}
print(add_daily_gains(df)[["date", "new_subscribers", "new_watch_hours"]])
print(best_day(df))                    # e.g. {'date': '2026-11-02', 'gain': 30}
print(best_day(df, "new_watch_hours"))  # biggest single-day watch-hour gain
```

### Income mix, smoothed gains and milestones passed

```python
from ytagent.frame import add_rolling_gains
from ytagent.milestones import milestones_reached
from ytagent.revenue import revenue_share_by_source

print(revenue_share_by_source({"ads": 300.0, "memberships": 75.0, "super_chat": 25.0}))
# {'ads': 75.0, 'memberships': 18.75, 'super_chat': 6.25}
print(add_rolling_gains(df, window=7)[["date", "avg_new_subscribers"]])  # 7-day trailing mean
print(milestones_reached(1_200))  # [100, 500, 1000]
```

### Weakest day and Shorts-route timing

```python
from ytagent.frame import worst_day
from ytagent.shorts import days_to_shorts_eligibility

print(worst_day(df))  # e.g. {'date': '2026-11-03', 'gain': -5} - a day the channel lost subs
print(days_to_shorts_eligibility(500, 4_000_000, subs_per_day=50, shorts_views_per_day=200_000))  # 30
```

### Milestones crossed and best upload days

`milestones_between` lists the milestones a channel passed during a period
(the starting count is excluded), and `average_gain_by_weekday` averages the
daily subscriber gains of an analytics export by day of the week:

```python
import pandas as pd
from ytagent.frame import average_gain_by_weekday
from ytagent.milestones import milestones_between

print(milestones_between(450, 1_200))  # [500, 1000]

df = pd.read_csv("daily_totals.csv")  # date, subscribers, watch_hours
print(average_gain_by_weekday(df).idxmax())  # e.g. 'Saturday'
```

### Churn, consistency and annualized earnings

`longest_decline_streak` and `positive_day_share` summarise how steady
daily growth is, `average_view_duration_minutes` recovers minutes watched
per view from watch hours, and `annualized_revenue` scales a period's
earnings to a full year:

```python
from ytagent.engagement import average_view_duration_minutes
from ytagent.growth import longest_decline_streak, positive_day_share
from ytagent.revenue import annualized_revenue

print(longest_decline_streak([500, 498, 495, 495, 490, 489]))  # 2
print(positive_day_share([100, 110, 108, 120, 120]))  # 50.0
print(average_view_duration_minutes(250, 3000))  # 5.0
print(annualized_revenue(250, 30))  # 3041.67
```

### Relative growth, interaction mix and milestone dates

Percent changes compare fairly across channel sizes, the interaction mix
shows whether viewers discuss and share or only like, and `milestone_days`
pinpoints when each milestone was first hit:

```python
from ytagent.engagement import interaction_mix
from ytagent.growth import daily_percent_changes
from ytagent.milestones import milestone_days

print(daily_percent_changes([100, 110, 99]))  # [10.0, -10.0]
print(interaction_mix(80, 15, 5))  # {'likes': 80.0, 'comments': 15.0, 'shares': 5.0}
print(milestone_days([90, 120, 480, 510]))  # {100: 1, 500: 3}
```

With a daily export, `ytagent.frame.top_days(df, n=3)` ranks the strongest
gain days for a quick "what worked" review.

### Revenue tracking

```python
from ytagent.revenue import cumulative_revenue, payout_day, rpm_by_video

print(cumulative_revenue([40, 35, 30]))  # [40.0, 75.0, 105.0]
print(payout_day([40, 35, 30]))  # 2 (day the $100 AdSense threshold is reached)
print(rpm_by_video([
    {"title": "tutorial", "revenue": 90.0, "views": 30_000},
    {"title": "vlog", "revenue": 10.0, "views": 10_000},
]))  # {'tutorial': 3.0, 'vlog': 1.0, '__overall__': 2.5}
```

If an export skips days, run it through `ytagent.frame.fill_missing_dates(df)`
first so daily-gain helpers see one row per calendar day.

### Pace checks

`recent_average_growth` looks only at the last few daily changes,
`projected_period_revenue` extrapolates month-end earnings from the pace so
far, and `monthly_change_percent` compares each month's gains with the last:

```python
from ytagent.growth import recent_average_growth
from ytagent.revenue import projected_period_revenue

print(recent_average_growth([100, 110, 120, 125, 128], days=2))  # 4
print(projected_period_revenue(320, days_elapsed=21))  # 457.14
```

## Command line

```bash
python -m ytagent.cli 710 2500 --subs-per-day 22.5 --hours-per-day 40
# Not yet eligible.
# Subscribers: 71.0% (290 needed)
# Watch hours: 62.5% (1500.0 needed)
# Estimated days: 38

python -m ytagent.cli 1500 4200 --daily-views 2000 --rpm 3 --monetized-share 0.6
# Eligible for the YouTube Partner Program.
# Projected 30-day revenue: $108.00

python -m ytagent.cli 1200 100 --shorts-views 8000000 --shorts-views-per-day 100000
# ...
# Shorts route: 2,000,000 more Shorts views needed
# Shorts route ETA: 20 days

python -m ytagent.cli 1500 4200 --revenue-target 500 --earned 320 --days-left 9
# Eligible for the YouTube Partner Program.
# Revenue target: $20.00/day needed over 9 days
```

## Running tests

```bash
pip install -r requirements.txt
python -m pytest -q
```
