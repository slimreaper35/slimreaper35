"""
A farmer wants to farm their land with the maximum area where good land is present.

The land is represented as a matrix with 1s and 0s, where 1s mean good land and 0s mean bad land.

The farmer only wants to farm in a square of good land with the maximum area.

Please help the farmer to find the maximum area of the land they can farm in good land.
"""


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


def main() -> None:
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


if __name__ == "__main__":
    main()
