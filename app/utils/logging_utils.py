"""
Logging utilities for consistent performance tracking.
"""

import time
import logging
import inspect
from functools import wraps

# Configure global logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("app.utils.logging")


def log_time(func):
    """
    Decorator to log the execution time of both sync and async functions.
    Automatically detects coroutine functions.
    """
    if inspect.iscoroutinefunction(func):

        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"[ASYNC] {func.__name__} took {elapsed:.2f} ms")
            return result

    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"[SYNC] {func.__name__} took {elapsed:.2f} ms")
            return result

    return wrapper
