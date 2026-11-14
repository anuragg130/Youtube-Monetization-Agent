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
```

## Running tests

```bash
pip install -r requirements.txt
python -m pytest -q
```
