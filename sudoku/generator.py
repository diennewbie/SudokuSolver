import random
from math import isqrt

def validate_size(size):
    if not isinstance(size, int) or size < 1:
        raise ValueError("Sudoku size must be a positive integer.")

    if isqrt(size) ** 2 != size:
        raise ValueError(
            f"Sudoku size must be a perfect square (4, 9, 16, 25, ...), but got {size}."
        )

def generate_validSudoku(size, rng):
    base = isqrt(size)
    grid = []
    for r in range(size):
        row = []
        for c in range(size):
            value = (base * (r % base) + r // base + c) % size
            row.append(value)
        grid.append(row)

    def shuffled_order():
        groups = rng.sample(range(base), base)
        order = []
        for g in groups:
            positions = rng.sample(range(base), base)
            for i in positions:
                index = g * base + i
                order.append(index)
        return order

    rows = shuffled_order()
    cols = shuffled_order()

    new_grid = []

    for r in rows:
        new_row = []
        for c in cols:
            value = grid[r][c]
            new_row.append(value)
        new_grid.append(new_row)
    grid = new_grid

    numbers = list(range(1, size + 1))
    new_numbers = rng.sample(numbers, size)
    result = []
    for r in range(size):
        new_row = []
        for c in range(size):
            old_value = grid[r][c]
            new_value = new_numbers[old_value]
            new_row.append(new_value)
        result.append(new_row)
    return result

def generate_sampleSudoku(size, empty_ratio = 0.5, seed = None):
    validate_size(size)
    if not 0 <= empty_ratio < 1:
        raise ValueError("empty_ratio must be in the range [0, 1).")
    rng = random.Random(seed)
    puzzle = generate_validSudoku(size, rng)
    cells = []
    for r in range(size):
        for c in range(size):
            cells.append((r, c))

    num_empty = round(size * size * empty_ratio)
    cells_to_empty = rng.sample(cells, num_empty)

    for r, c in cells_to_empty:
        puzzle[r][c] = 0

    return puzzle
