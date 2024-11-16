from functools import wraps
from typing import Any, Callable

import requests
from ratelimit import limits, sleep_and_retry
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_rate_limited_send(period: float) -> Callable:
    """Create a rate-limited send method with the specified period.

    Args:
        period (float): The minimum interval (in seconds) between requests.

    Returns:
        Callable: A decorated function that enforces the rate limit.
    """

    def decorator(func: Callable) -> Callable:
        @sleep_and_retry
        @limits(calls=1, period=period)
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)

        return wrapper

    return decorator


class RateLimitedSession(requests.Session):
    """A rate-limited HTTP session that extends requests.Session with built-in rate limiting and retry logic.

    This class provides a custom implementation of requests.Session that includes:
    - Configurable rate limiting to prevent overwhelming the target server
    - Automatic retry logic for failed requests
    - Exponential backoff strategy for retries
    - Full support for all requests.Session parameters through args and kwargs

    Attributes:
        requests_per_second (int): Maximum number of requests allowed per second.
        frequency (float): The calculated interval between requests (1/requests_per_second).
        total_retries (int): Maximum number of retry attempts for failed requests.
        backoff_factor (float): A multiplier used to determine the time to wait between retries.
            The wait time is calculated as {backoff_factor * (2 ** (retry_number - 1))} seconds.

    Example:
        >>> session = RateLimitedSession(requests_per_second=2, total_retries=3, verify=False)
        >>> response = session.get('https://api.example.com/data')
    """

    def __init__(
        self,
        requests_per_second: int = 10,
        total_retries: int = 5,
        backoff_factor: float = 0.25,
    ) -> None:
        """Initialize a new rate-limited session.

        Args:
            requests_per_second (int, optional): Maximum number of requests allowed per second.
                Defaults to 10.
            total_retries (int, optional): Maximum number of retry attempts for failed requests.
                Defaults to 5.
            backoff_factor (float, optional): Multiplier used to determine wait time between retries.
                Defaults to 0.25.

        Example:
            >>> session = get_rate_limiter(
            ...     requests_per_second=5
            ... )
            >>> response = session.get('https://api.example.com/data')
        """
        super().__init__()

        # Store configuration
        self.requests_per_second = requests_per_second
        self.frequency = 1 / requests_per_second
        self.total_retries = total_retries
        self.backoff_factor = backoff_factor

        # Configure retry strategy
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

        # Create and set the rate-limited send method
        self.send = create_rate_limited_send(self.frequency)(self.send)


def get_rate_limiter(
    requests_per_second: int = 10,
    total_retries: int = 5,
    backoff_factor: float = 0.25,
) -> RateLimitedSession:
    """Create a new rate-limited session with the specified parameters.

    A convenience function to create a new RateLimitedSession instance with custom parameters.
    Supports all parameters from requests.Session through args and kwargs.

    Factory method for backwards compatibility with initial implementation.

    Args:
        requests_per_second (int, optional): Maximum number of requests allowed per second.
            Defaults to 10.
        total_retries (int, optional): Maximum number of retry attempts for failed requests.
            Defaults to 5.
        backoff_factor (float, optional): Multiplier used to determine wait time between retries.
            Defaults to 0.25.

    Returns:
        RateLimitedSession: A configured rate-limited session instance.

    Example:
        >>> session = get_rate_limiter(
        ...     requests_per_second=5
        ... )
        >>> response = session.get('https://api.example.com/data')
    """
    return RateLimitedSession(
        requests_per_second=requests_per_second,
        total_retries=total_retries,
        backoff_factor=backoff_factor,
    )
