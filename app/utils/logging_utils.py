import time
import logging
import inspect
from functools import wraps

logging.basicConfig(level=logging.INFO)


def log_time(func):
    if inspect.iscoroutinefunction(func):
        # Async endpoint
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            logging.info(f"{func.__name__} took {elapsed_ms:.2f} ms (async)")
            return result

    else:
        # Sync endpoint
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_ms = (time.perf_counter() - start) * 1000
            logging.info(f"{func.__name__} took {elapsed_ms:.2f} ms (sync)")
            return result

    return wrapper
