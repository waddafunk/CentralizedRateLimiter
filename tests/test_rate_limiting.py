import threading
import time

import pytest
import responses
from urllib3.util.retry import Retry

from centralized_rate_limiter import RateLimitedSession, get_rate_limiter


@pytest.fixture
def session() -> RateLimitedSession:
    return get_rate_limiter(requests_per_second=10, total_retries=3, backoff_factor=0.1)


@responses.activate
def test_rate_limiting(session: RateLimitedSession):
    """Test that requests are rate limited according to the specified rate."""
    # Setup mock endpoint
    responses.add(
        responses.GET,
        "https://api.example.com/test",
        json={"status": "success"},
        status=200,
    )

    # Make multiple requests and measure time
    num_seconds_range = 4

    for seconds in range(num_seconds_range):
        start_time = time.time()

        for _ in range(seconds * session.requests_per_second + 1):
            response = session.get("https://api.example.com/test")
            assert response.status_code == 200

        elapsed_time = time.time() - start_time
        assert elapsed_time >= seconds


@responses.activate
def test_retry_behavior(session: RateLimitedSession):
    """Test that the session correctly retries on specified status codes."""
    # Setup mock endpoint that fails twice then succeeds
    responses.add(responses.GET, "https://api.example.com/test", status=503)
    responses.add(responses.GET, "https://api.example.com/test", status=503)
    responses.add(
        responses.GET,
        "https://api.example.com/test",
        json={"status": "success"},
        status=200,
    )

    # Request should eventually succeed after retries
    response = session.get("https://api.example.com/test")
    assert response.status_code == 200
    assert len(responses.calls) == 3  # Verify it took 3 attempts


@responses.activate
def test_different_http_methods(session: RateLimitedSession):
    """Test that rate limiting works for different HTTP methods."""
    # Setup mock endpoints for different methods
    responses.add(
        responses.GET,
        "https://api.example.com/test",
        json={"method": "get"},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://api.example.com/test",
        json={"method": "post"},
        status=200,
    )
    responses.add(
        responses.PUT,
        "https://api.example.com/test",
        json={"method": "put"},
        status=200,
    )

    # Test different HTTP methods
    start_time = time.time()

    for _ in range(11):
        response = session.get("https://api.example.com/test")
        assert response.status_code == 200

        response = session.post("https://api.example.com/test")
        assert response.status_code == 200

        response = session.put("https://api.example.com/test")
        assert response.status_code == 200

    elapsed_time = time.time() - start_time
    assert elapsed_time >= 3


@responses.activate
def test_max_retries_exceeded(session: RateLimitedSession):
    """Test that the session gives up after maximum retries."""
    # Setup mock endpoint to always return 503
    responses.add(responses.GET, "https://api.example.com/test", status=503)

    # Request should return 503 after all retries are exhausted
    response = session.get("https://api.example.com/test")
    assert response.status_code == 503
    assert len(responses.calls) == 4  # Initial request + 3 retries


def test_custom_parameters():
    """Test that custom rate limiting parameters are respected."""
    custom_session = get_rate_limiter(
        requests_per_second=2, total_retries=1, backoff_factor=0.5
    )

    assert isinstance(custom_session.adapters["http://"].max_retries, Retry)
    assert custom_session.adapters["http://"].max_retries.total == 1
    assert custom_session.adapters["http://"].max_retries.backoff_factor == 0.5


@responses.activate
def test_concurrent_requests(session: RateLimitedSession):
    """Test that concurrent requests are properly rate limited."""
    responses.add(
        responses.GET,
        "https://api.example.com/test",
        json={"status": "success"},
        status=200,
    )

    # Make concurrent requests
    threads = []
    start_time = time.time()

    for _ in range(20):  # Try to make 20 concurrent requests
        thread = threading.Thread(
            target=lambda: session.get("https://api.example.com/test")
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    elapsed_time = time.time() - start_time
    expected_minimum_time = (
        20 / session.requests_per_second
    ) - 0.1  # Allow small margin

    assert elapsed_time >= expected_minimum_time
    assert len(responses.calls) == 20


@responses.activate
def test_too_many_requests_retry(session: RateLimitedSession):
    """Test retry behavior specifically for 429 (Too Many Requests) status code."""
    # Setup mock endpoint that returns 429 twice then succeeds
    responses.add(responses.GET, "https://api.example.com/test", status=429)
    responses.add(responses.GET, "https://api.example.com/test", status=429)
    responses.add(
        responses.GET,
        "https://api.example.com/test",
        json={"status": "success"},
        status=200,
    )

    response = session.get("https://api.example.com/test")

    # Verify the response was eventually successful
    assert response.status_code == 200
    assert len(responses.calls) == 3

    # Verify retry configuration
    adapter = session.adapters["https://"]
    retry = adapter.max_retries

    # Verify retry settings
    assert retry.total == session.total_retries
    assert retry.backoff_factor == session.backoff_factor
    assert 429 in retry.status_forcelist  # Verify 429 is in retry status codes
