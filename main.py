import argparse
from statistics import mean

from sudoku.encoding import AMO_METHODS
from sudoku.generator import generate_sampleSudoku
from sudoku.solver import solve


def main():
    parser = argparse.ArgumentParser(description="Generate a random Sudoku and benchmark SAT encodings.")
    parser.add_argument("size", nargs="?", type=int, help="Sudoku size (perfect square: 4, 9, 16, 25, ...)")
    parser.add_argument("--empty", type=float, default=0.5, help="fraction of empty cells (default 0.5)")
    parser.add_argument("--runs", type=int, default=10, help="runs per encoding to average (default 10)")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducible puzzles")
    args = parser.parse_args()

    size = args.size if args.size is not None else int(input("Sudoku size (perfect square): "))

    sudoku = generate_sampleSudoku(size, args.empty, args.seed)

    print(f"Benchmark {size}x{size}: {args.runs} run(s) per encoding, same puzzle")
    print(f"{'method':<12}{'vars':>10}{'clauses':>12}{'avg encode (s)':>16}{'avg solve (s)':>15}")

    for method in AMO_METHODS:
        runs = []

        for _ in range(args.runs):
            stats = {}

            if solve(sudoku, method, stats) is None:
                raise RuntimeError(f"No solution found with method '{method}'.")

            runs.append(stats)

        print(
            f"{method:<12}{runs[0]['variables']:>10}{runs[0]['clauses']:>12}"
            f"{mean(r['encoding_time'] for r in runs):>16.6f}"
            f"{mean(r['solver_time'] for r in runs):>15.6f}"
        )


if __name__ == "__main__":
    main()