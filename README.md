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

## Running tests

```bash
pip install pytest
python -m pytest -q
```
