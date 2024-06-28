import time
from functools import wraps


def time_tracking(func):
    """Print an elapsed work time of function to console"""
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        time_start = time.monotonic()
        res = func(*args, **kwargs)
        elapsed_time = time.monotonic() - time_start
        print(f"Time tracking of func {func.__name__}: {elapsed_time:0.5f} s")

        return res

    return wrapper_timer


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""
    @wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)

        return wrapper_singleton.instance

    wrapper_singleton.instance = None

    return wrapper_singleton


def count_calls(func):
    """Count calls of function"""
    @wraps(func)
    def wrapper_count_calls(*args, **kwargs):
        wrapper_count_calls.num_calls += 1
        print(f"Number of calls of func {func.__name__!r}: {wrapper_count_calls.num_calls}")

        return func(*args, **kwargs)

    wrapper_count_calls.num_calls = 0

    return wrapper_count_calls
