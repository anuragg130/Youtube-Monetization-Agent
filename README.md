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

## Running tests

```bash
pip install pytest
python -m pytest -q
```
