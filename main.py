import argparse
from statistics import mean

from sudoku.encoding import AMO_METHODS
from sudoku.generator import generate_sampleSudoku
from sudoku.other_solvers import OTHER_SOLVERS
from sudoku.solver import solve
import traceback


# Chạy một solver nhiều lần rồi in một dòng kết quả.
# run_once là hàm nhận vào "stats" và giải Sudoku một lần.
def benchmark(name, run_once, runs):
    results = []
    try:
        for _ in range(runs):
            stats = {}
            if run_once(stats) is None:
                raise RuntimeError("không tìm thấy nghiệm")
            results.append(stats)
    except Exception as e:  # chưa cài thư viện, thiếu license, bài quá lớn...
        print(f"{name:<14}bỏ qua: {type(e).__name__}: {e}")
        return

    # Solver SAT có số biến/mệnh đề, solver khác thì in "-"
    variables = results[0].get("variables", "-")
    clauses = results[0].get("clauses", "-")
    encode = mean(r["encoding_time"] for r in results)
    solve_t = mean(r["solver_time"] for r in results)
    print(f"{name:<14}{variables:>10}{clauses:>12}{encode:>16.6f}{solve_t:>15.6f}")


def main():
    parser = argparse.ArgumentParser(description="Generate a random Sudoku and benchmark solvers.")
    parser.add_argument("size", nargs="?", type=int, help="Sudoku size (perfect square: 4, 9, 16, 25, ...)")
    parser.add_argument("--empty", type=float, default=0.5, help="fraction of empty cells (default 0.5)")
    parser.add_argument("--runs", type=int, default=10, help="runs per solver to average (default 10)")
    parser.add_argument("--seed", type=int, default=None, help="random seed for reproducible puzzles")
    args = parser.parse_args()

    size = args.size if args.size is not None else int(input("Sudoku size (perfect square): "))
    sudoku = generate_sampleSudoku(size, args.empty, args.seed)

    print(f"Benchmark {size}x{size}: {args.runs} run(s) per solver, same puzzle")
    print(f"{'method':<14}{'vars':>10}{'clauses':>12}{'avg encode (s)':>16}{'avg solve (s)':>15}")

    # 4 cách mã hóa SAT
    for method in AMO_METHODS:
        # "lambda stats: ..." là một hàm nhỏ không tên, nhận stats và gọi solve
        benchmark(f"sat-{method}", lambda stats: solve(sudoku, method, stats), args.runs)

    # 4 solver còn lại
    for name, solve_function in OTHER_SOLVERS.items():
        benchmark(name, lambda stats: solve_function(sudoku, stats), args.runs)


if __name__ == "__main__":
    main()