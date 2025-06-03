"""
A farmer wants to farm their land with the maximum area where good land is present.

The land is represented as a matrix with 1s and 0s, where 1s mean good land and 0s mean bad land.

The farmer only wants to farm in a square of good land with the maximum area.

Please help the farmer to find the maximum area of the land they can farm in good land.
"""

import math


class Matrix:
    rows: int
    cols: int
    grid: list[list[int]]

    def __init__(self, grid: list[list[int]]) -> None:
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.grid = grid


def largest_square(m: Matrix) -> int:
    largest = 0

    for i in range(m.rows):
        for j in range(m.cols):
            largest = max(largest, _largest_square_rec(m, i, j))

    return largest


def _largest_square_rec(m: Matrix, row: int, col: int) -> int:
    if row >= m.rows or col >= m.cols:
        return 0

    if m.grid[row][col] == 0:
        return 0

    largest_square_right = _largest_square_rec(m, row, col + 1)
    largest_square_diagonal = _largest_square_rec(m, row + 1, col + 1)
    largest_square_bottom = _largest_square_rec(m, row + 1, col)

    return 1 + min(largest_square_right, largest_square_diagonal, largest_square_bottom)


def largest_square_alternative(m: Matrix) -> int:
    largest = 0
    dp = [[0] * m.cols for _ in range(m.rows)]

    for i in range(m.rows):
        for j in range(m.cols):
            if m.grid[i][j] == 0:
                continue

            left = right = diag = 0

            if i > 0:
                left = dp[i - 1][j]
            if j > 0:
                right = dp[i][j - 1]
            if i > 0 and j > 0:
                diag = dp[i - 1][j - 1]

            dp[i][j] = min(left, right, diag) + 1
            largest = max(largest, dp[i][j])

    return largest


def test_largest_square() -> None:
    example = [
        [0, 1, 1, 0, 1],
        [1, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    m = Matrix(grid=example)
    assert largest_square(m) == largest_square_alternative(m) == 3


def cosine_similarity(
    a_keys: list[int],
    a_values: list[float],
    b_keys: list[int],
    b_values: list[float],
) -> float:
    """
    Calculate the cosine similarity between two vectors represented by their keys and values.

    But what is the cosine similarity ?

    Cosine similarity is a measure of similarity between two non-zero vectors in an inner product space.
    It is defined as the cosine of the angle between them, which can be computed using the dot product
    of the vectors divided by the product of their magnitudes.

    The formula for cosine similarity is:
    cosine_similarity(A, B) = (A . B) / (||A|| * ||B||)

    where:
    - A . B is the dot product of vectors A and B.
    - ||A|| is the magnitude (length) of vector A.
    - ||B|| is the magnitude (length) of vector B.

    The function takes two lists of keys and their corresponding values, computes the dot product,
    and calculates the magnitudes of both vectors to return the cosine similarity.
    """
    a_map = {a_keys[i]: a_values[i] for i in range(len(a_keys))}
    b_map = {b_keys[i]: b_values[i] for i in range(len(b_keys))}

    dot_product = 0.0

    ptr_a = 0
    ptr_b = 0

    while ptr_a < len(a_keys) and ptr_b < len(b_keys):
        key_a = a_keys[ptr_a]
        key_b = b_keys[ptr_b]

        if key_a == key_b:
            dot_product += a_map[key_a] * b_map[key_b]
            ptr_a += 1
            ptr_b += 1
        elif key_a < key_b:
            ptr_a += 1
        else:
            ptr_b += 1

    magnitude_a_squared = 0.0
    for value in a_values:
        magnitude_a_squared += value * value

    magnitude_b_squared = 0.0
    for value in b_values:
        magnitude_b_squared += value * value

    magnitude_a = math.sqrt(magnitude_a_squared)
    magnitude_b = math.sqrt(magnitude_b_squared)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def test_cosine_similarity() -> None:
    a_keys = [2, 4, 5, 8]
    a_values = [7.0, 5.0, 12.0, 1.0]
    b_keys = [3, 4, 7]
    b_values = [3.0, 5.0, 2.0]

    # Manual calculation for verification:
    # Dot product (A . B): only common key is 4
    # (5 * 5) = 25.0
    expected_dot_product = 25.0
    # Magnitude A (||A||)
    expected_magnitude_a = math.sqrt(7**2 + 5**2 + 12**2 + 1**2)
    # Magnitude B (||B||)
    expected_magnitude_b = math.sqrt(3**2 + 5**2 + 2**2)

    expected_cosine_similarity = expected_dot_product / (
        expected_magnitude_a * expected_magnitude_b
    )
    result = cosine_similarity(a_keys, a_values, b_keys, b_values)

    tolerance = 1e-9
    assert abs(result - expected_cosine_similarity) < tolerance


test_largest_square()
test_cosine_similarity()
print("OK")
