import requests
from ratelimit import limits, sleep_and_retry
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


class RateLimitedSessionProto(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.requests_per_second = None
        self.frequency = None
        self.total_retries = None
        self.backoff_factor = None


def get_rate_limiter(
    requests_per_second: int = 10, total_retries: int = 5, backoff_factor: float = 0.25,
) -> RateLimitedSessionProto:
    """Create a new rate-limited session with the specified parameters."""

    class RateLimitedSession(RateLimitedSessionProto):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Configure retry strategy to handle retries at the adapter level
            retry_strategy = Retry(
                total=total_retries,
                backoff_factor=backoff_factor,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=[
                    "GET",
                    "POST",
                    "PUT",
                    "DELETE",
                    "HEAD",
                    "OPTIONS",
                    "TRACE",
                    "PATCH",
                ],
                raise_on_status=False,
            )

            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.mount("http://", adapter)
            self.mount("https://", adapter)

            self.requests_per_second = requests_per_second
            self.frequency = 1 / requests_per_second
            self.total_retries = total_retries
            self.backoff_factor = backoff_factor

        @sleep_and_retry
        @limits(calls=1, period=1 / requests_per_second)
        def send(self, request, **kwargs):
            """Override send to handle retries at a lower level"""
            return super().send(request, **kwargs)

    return RateLimitedSession
