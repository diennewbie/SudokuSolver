from math import isqrt
from time import perf_counter

from pysat.solvers import Glucose3

from .constraints import build_constraints
from .variable import var, decode_var

# transfer numbers in Sudoku into CNF
def add_givens(clauses, sudoku, size):

    for row in range(size):

        for col in range(size):

            value = sudoku[row][col]

            if value != 0:

                clauses.append([
                    var(
                        row + 1,
                        col + 1,
                        value,
                        size
                    )
                ])

# solve using Glucose3
def solve(sudoku):

    size = len(sudoku)

    if size == 0:
        raise ValueError("Sudoku is empty.")

    if any(len(row) != size for row in sudoku):
        raise ValueError("Sudoku must be a square matrix.")

    if isqrt(size) ** 2 != size:
        raise ValueError("Sudoku size must be a perfect square.")

    encoding_start = perf_counter()

# build constraints
    clauses, next_var = build_constraints(size)

    add_givens(clauses, sudoku, size)

    encoding_time = perf_counter() - encoding_start

    print("Number of variables:", next_var - 1)
    print("Number of clauses:", len(clauses))
    print(f"Encoding time: {encoding_time:.6f} seconds")

    solver_start = perf_counter()
    solver = Glucose3()

    for clause in clauses:
        solver.add_clause(clause)

    is_satisfiable = solver.solve()
    solver_time = perf_counter() - solver_start

    print(f"Solver time: {solver_time:.6f} seconds")

    if not is_satisfiable:
        solver.delete()
        return None

    model = solver.get_model()
    solver.delete()

    solution = [
        [0 for _ in range(size)]
        for _ in range(size)
    ]

    for literal in model:

        if literal > 0:

            if literal <= size ** 3:

                row, col, value = decode_var(
                    literal,
                    size
                )

                solution[row - 1][col - 1] = value

    return solution
