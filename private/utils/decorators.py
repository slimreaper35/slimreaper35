"""
Decorators are functions that wrap other functions or classes. Decorators use the @ syntax
to modify the behavior of the function or class they decorate.
"""

import functools
import pickle
import timeit


def cached(func):
    """Decorator that caches."""
    cache = {}

    @functools.wraps(func)
    def _cached(*args, **kwargs):
        key = pickle.dumps((args, kwargs))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return _cached


def logged(func):
    """Decorator for logging."""

    @functools.wraps(func)
    def _logged(*args, **kwargs):
        print("logged")  # proper logging
        return func(*args, **kwargs)

    return _logged


registry = dict()


def register_at_call(name):
    """Register the decorated function at call time."""

    def _register(func):
        @functools.wraps(func)
        def __register(*args, **kwargs):
            registry.setdefault(name, []).append(func)
            return func(*args, **kwargs)

        return __register

    return _register


def register_at_def(name):
    """Register the decorated function at definition time."""

    def _register(func):
        registry.setdefault(name, []).append(func)

        return func

    return _register


def check_name_length(max_len=30):
    """Check method name length.

    Raises a `NameError` if one method name of a decorated class is longer than `max_len`.
    """

    def _check_name_length(cls):
        for name, obj in cls.__dict__.items():
            if callable(obj) and len(name) > max_len:
                raise NameError(f"name `{name}` too long, only {max_len} characters are allowed")

        return cls

    return _check_name_length


def measure_time(func):
    """Decorator to measure function run times."""

    @functools.wraps(func)
    def _measure_time(*args, **kwargs):
        start = timeit.default_timer()
        result = func(*args, **kwargs)
        end = timeit.default_timer()
        print(end - start)
        return result

    return _measure_time


def repeat(times=1):
    """Decorator to repeat function calls."""

    def _repeat(func):
        @functools.wraps(func)
        def __repeat(*args, **kwargs):
            assert times >= 1  # easy check
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return __repeat

    return _repeat
