import requests
from ratelimit import limits, sleep_and_retry
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def get_rate_limiter(total_retries=5, backoff_factor=0.25, requests_per_second=10):
    class RateLimiter:
        def __init__(self) -> None:   
            retry_strategy = Retry(
                total=total_retries,  # Total retries
                status_forcelist=[429, 500, 502, 503, 504],  # Status codes to retry on
                backoff_factor=backoff_factor  # Time between retries
            )
            
    
            # Apply the retry strategy to an HTTPAdapter
            adapter = HTTPAdapter(max_retries=retry_strategy)
    
            # Create a session and mount the adapter
            self.SESSION = requests.Session()
            self.SESSION.mount("http://", adapter)
            self.SESSION.mount("https://", adapter)
    
    
        @sleep_and_retry
        @limits(calls=requests_per_second, period=1)
        def rate_limited_request(self, func):
            return func(self.SESSION)
        
    return RateLimiter()