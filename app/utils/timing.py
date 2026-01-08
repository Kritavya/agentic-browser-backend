"""
Timing Utilities.

Provides timing-related utilities for performance measurement
and timeout handling.

TODO:
- Add async timeout context manager
- Add performance metric collection
"""

import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def timer(name: str = "operation") -> Generator[dict, None, None]:
    """
    Context manager for timing operations.

    Args:
        name: Name of the operation being timed.

    Yields:
        Dictionary with timing info (populated on exit).

    Example:
        with timer("my_operation") as t:
            do_something()
        print(f"Took {t['duration_ms']}ms")
    """
    result = {"name": name, "start": time.time(), "end": None, "duration_ms": None}
    try:
        yield result
    finally:
        result["end"] = time.time()
        result["duration_ms"] = (result["end"] - result["start"]) * 1000


class RateLimiter:
    """
    Simple rate limiter for controlling request frequency.

    TODO:
    - Implement sliding window algorithm
    - Add async support
    """

    def __init__(self, requests_per_second: float = 10.0) -> None:
        """
        Initialize rate limiter.

        Args:
            requests_per_second: Maximum requests per second.
        """
        self.min_interval = 1.0 / requests_per_second
        self._last_request_time = 0.0

    def wait(self) -> float:
        """
        Wait if necessary to respect rate limit.

        Returns:
            Time waited in seconds.
        """
        now = time.time()
        time_since_last = now - self._last_request_time
        wait_time = max(0, self.min_interval - time_since_last)

        if wait_time > 0:
            time.sleep(wait_time)

        self._last_request_time = time.time()
        return wait_time

    def can_proceed(self) -> bool:
        """
        Check if a request can proceed without waiting.

        Returns:
            True if enough time has passed since last request.
        """
        now = time.time()
        return (now - self._last_request_time) >= self.min_interval


def format_duration(ms: float) -> str:
    """
    Format a duration in milliseconds to human-readable string.

    Args:
        ms: Duration in milliseconds.

    Returns:
        Formatted duration string.

    Examples:
        >>> format_duration(500)
        '500ms'
        >>> format_duration(2500)
        '2.5s'
        >>> format_duration(65000)
        '1m 5s'
    """
    if ms < 1000:
        return f"{ms:.0f}ms"
    elif ms < 60000:
        return f"{ms / 1000:.1f}s"
    else:
        minutes = int(ms // 60000)
        seconds = int((ms % 60000) // 1000)
        return f"{minutes}m {seconds}s"
