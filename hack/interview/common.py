from collections.abc import Iterable


def is_palindrome_normal(string: str) -> bool:
    """
    Check if a string is a palindrome - reads the same forwards and backwards.
    """
    processed = [char.lower() for char in string if char.isalnum()]

    for i in range(len(processed) // 2):
        if processed[i] != processed[-i - 1]:
            return False

    return True


def is_palindrome_pythonic(string: str) -> bool:
    """
    Check if a string is a palindrome - reads the same forwards and backwards.
    """
    processed = [char.lower() for char in string if char.isalnum()]
    return processed == processed[::-1]


def find_intersection(nums1: list[int], nums2: list[int]) -> Iterable[int]:
    """
    Find the intersection of two lists - elements that are common in both lists.
    """
    return set(nums1) & set(nums2)


def fib_infinite():
    """
    A generator that yields the Fibonacci sequence indefinitely.
    """
    a, b = 0, 1
    while True:
        yield a
        # OR: a, b = b, a + b
        tmp = a
        a = b
        b = tmp + b


def fib_recursive(n: int) -> int:
    """
    Calculate the nth Fibonacci number using a recursive approach.

    WARNING: This approach is not efficient.
    """
    if n == 0:
        return 0

    if n == 1:
        return 1

    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n: int) -> int:
    """
    Calculate the nth Fibonacci number using an iterative approach.
    """
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    return a


def _fib_with_dict_rec(n: int, values: dict[int, int]) -> int:
    if values.get(n) is not None:
        return values[n]

    values[n] = _fib_with_dict_rec(n - 1, values) + _fib_with_dict_rec(n - 2, values)
    return values[n]


def fib_with_dict(n: int) -> int:
    """
    Calculate the nth Fibonacci number using a recursive approach with memoization.
    """
    return _fib_with_dict_rec(n, {0: 0, 1: 1})
