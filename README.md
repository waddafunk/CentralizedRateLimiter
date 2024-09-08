# CentralizedRateLimiter
Utility factory building classes to handle rate limiting in a centralized manner. Specify the limit once and make all the requests you need.

Usage:
```python
from rate_limiting import get_rate_limiter

RATE_LIMITER = get_rate_limiter(total_retries=5, backoff_factor=0.25, requests_per_second=10)
url = "your_url"
headers = {"your_header": "Your_value}

# rate_limited_request takes as argument a function that takes as argument a Session class from the request package.
response = RATE_LIMITER.rate_limited_request(
  lambda SESSION: SESSION.get(url, headers=headers)
)
```
