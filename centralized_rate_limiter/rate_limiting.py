import threading
import time
from collections import deque
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class RateLimit:
    """Represents a thread-safe rate limit with a maximum number of calls within a time period."""

    max_calls: int
    period: float  # in seconds
    calls: deque = field(
        default_factory=lambda: deque(maxlen=0)
    )  # Will be initialized in post_init
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self):
        self.calls = deque(maxlen=self.max_calls)

    def add_call(self) -> None:
        """Record a new API call in a thread-safe manner."""
        with self.lock:
            current_time = time.time()
            self.calls.append(current_time)

    def wait_time(self) -> float:
        """Calculate the time to wait before the next call in a thread-safe manner."""
        with self.lock:
            if len(self.calls) < self.max_calls:
                return 0

            oldest_call = self.calls[0]
            current_time = time.time()
            time_passed = current_time - oldest_call

            if time_passed < self.period:
                return self.period - time_passed
            return 0


def create_rate_limited_send(
    period: float, additional_limits: Optional[List[Tuple[int, float]]] = None
) -> Callable:
    """Create a thread-safe rate-limited send method.

    Args:
        period (float): The minimum interval (in seconds) between requests.
        additional_limits (List[Tuple[int, float]], optional): Additional rate limits as
            (max_calls, period) tuples. Example: [(2000, 3600)] for 2000 calls/hour

    Returns:
        Callable: A decorated function that enforces the rate limits.
    """
    # Create primary rate limit
    primary_limit = RateLimit(max_calls=1, period=period)

    # Create additional rate limits if specified
    extra_limits = []
    if additional_limits:
        extra_limits = [
            RateLimit(max_calls, period) for max_calls, period in additional_limits
        ]

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            while True:
                # Check all rate limits and get the maximum wait time
                wait_times = [primary_limit.wait_time()]
                if extra_limits:
                    wait_times.extend(limit.wait_time() for limit in extra_limits)

                max_wait = max(wait_times)
                if max_wait <= 0:
                    break

                time.sleep(max_wait)

            # Record the call in all rate limit trackers
            primary_limit.add_call()
            for limit in extra_limits:
                limit.add_call()

            return func(*args, **kwargs)

        return wrapper

    return decorator


class RateLimitedSession(requests.Session):
    """A thread-safe rate-limited HTTP session that extends requests.Session."""

    def __init__(
        self,
        requests_per_second: int = 10,
        total_retries: int = 5,
        backoff_factor: float = 0.25,
        additional_limits: Optional[List[Tuple[int, float]]] = None,
    ) -> None:
        """Initialize a new rate-limited session.

        Args:
            requests_per_second (int, optional): Maximum number of requests allowed per second.
                Defaults to 10.
            total_retries (int, optional): Maximum number of retry attempts for failed requests.
                Defaults to 5.
            backoff_factor (float, optional): Multiplier used to determine wait time between retries.
                Defaults to 0.25.
            additional_limits (List[Tuple[int, float]], optional): Additional rate limits as
                (max_calls, period) tuples. Example: [(2000, 3600)] for 2000 calls/hour
        """
        super().__init__()

        # Store configuration
        self.requests_per_second = requests_per_second
        self.frequency = 1 / requests_per_second
        self.total_retries = total_retries
        self.backoff_factor = backoff_factor
        self.additional_limits = additional_limits

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
        self.send = create_rate_limited_send(
            self.frequency, additional_limits=additional_limits
        )(self.send)


def get_rate_limiter(
    requests_per_second: int = 10,
    total_retries: int = 5,
    backoff_factor: float = 0.25,
    additional_limits: Optional[List[Tuple[int, float]]] = None,
) -> RateLimitedSession:
    """Create a new thread-safe rate-limited session."""
    return RateLimitedSession(
        requests_per_second=requests_per_second,
        total_retries=total_retries,
        backoff_factor=backoff_factor,
        additional_limits=additional_limits,
    )
