import math
from pathlib import Path

from sudoku.solver import solve


def parse_sudoku_block(lines):
    source_rows = []

    for line_number, line in enumerate(lines, start=1):
        text = line.strip()

        if not text or text.startswith("#"):
            continue

        source_rows.append((line_number, text))

    if not source_rows:
        raise ValueError("Sudoku block is empty.")

    size = len(source_rows)
    rows = []

    for line_number, text in source_rows:
        tokens = text.split()

        # Keep support for compact 4x4/9x9 rows such as "530070000".
        if len(tokens) == 1 and len(tokens[0]) == size and tokens[0].isdigit():
            row = [int(char) for char in tokens[0]]
        else:
            try:
                row = [int(token) for token in tokens]
            except ValueError as error:
                raise ValueError(
                    f"Invalid value at line {line_number}."
                ) from error

        if len(row) != size:
            raise ValueError(
                f"Each row must contain exactly {size} values."
            )

        if any(value < 0 or value > size for value in row):
            raise ValueError(
                f"Values at line {line_number} must be between 0 and {size}."
            )

        rows.append(row)

    if math.isqrt(size) ** 2 != size:
        raise ValueError(
            f"Sudoku size must be a perfect square, but found {size}."
        )

    return rows


def read_sudokus(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    boards = []
    current_block = []

    for line in lines:
        if not line.strip():
            if current_block:
                boards.append(parse_sudoku_block(current_block))
                current_block = []
            continue

        current_block.append(line)

    if current_block:
        boards.append(parse_sudoku_block(current_block))

    if not boards:
        raise ValueError(f"No Sudoku puzzle found in file: {filename}")

    return boards


def read_sudoku(filename):
    return read_sudokus(filename)[0]


def print_sudoku(sudoku):
    size = len(sudoku)
    block_size = math.isqrt(size)
    border = "+" + "+".join(["-" * (2 * block_size + 1) for _ in range(block_size)]) + "+"

    print(border)

    for row in range(size):
        for col in range(size):
            if col % block_size == 0:
                print("|", end=" ")
            print(sudoku[row][col], end=" ")
        print("|")
        if (row + 1) % block_size == 0:
            print(border)


def main():
    puzzle_file = Path("examples/sudokus.txt")
    if not puzzle_file.exists():
        puzzle_file = Path("examples/sudoku.txt")

    puzzles = read_sudokus(str(puzzle_file))

    print(f"Found {len(puzzles)} Sudoku puzzle(s) in {puzzle_file}.")

    for index, sudoku in enumerate(puzzles, start=1):
        print(f"\nPuzzle #{index}:")
        print_sudoku(sudoku)

        print("\nSolving...")
        solution = solve(sudoku)

        if solution is None:
            print("\nNo solution.")
        else:
            print("\nSolved Sudoku:")
            print_sudoku(solution)


if __name__ == "__main__":
    main()
