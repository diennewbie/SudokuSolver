import gurobipy as gp

from math import isqrt
from time import perf_counter
from ortools.sat.python import cp_model
from gurobipy import GRB
from docplex.mp.model import Model
from docplex.cp.model import CpoModel

def get_units(size):
    block_size = isqrt(size)
    units = []
    for i in range(size):
        row = []
        col = []
        for j in range(size):
            row.append((i, j))
            col.append((j, i))
        units.append(row)
        units.append(col)

    for block_row in range(block_size):
        for block_col in range(block_size):
            block = []
            for i in range(block_size):
                for j in range(block_size):
                    block.append((block_row * block_size + i, block_col * block_size + j))
            units.append(block)

    return units

# CP-SAT (IP)
def solve_cpsat(sudoku, stats=None):
    size = len(sudoku)
# build
    start = perf_counter()
    model = cp_model.CpModel()
    x = {}
    for row in range(size):
        for col in range(size):
            for value in range(1, size + 1):
                x[(row, col, value)] = model.new_bool_var(f"x_{row}_{col}_{value}")

# Each cell must contain exactly one value
    for row in range(size):
        for col in range(size):
            cell_vars = []
            for value in range(1, size + 1):
                cell_vars.append(x[(row, col, value)])
            model.add_exactly_one(cell_vars)

# Each Row/Column/Block must contain exactly one value
    for unit in get_units(size):
        for value in range(1, size + 1):
            variables = []
            for (row, col) in unit:
                variables.append(x[(row, col, value)])
            model.add_exactly_one(variables)

    for row in range(size):
        for col in range(size):
            if sudoku[row][col] != 0:
                model.add(x[(row, col, sudoku[row][col])] == 1)

    encoding_time = perf_counter() - start
    start = perf_counter()
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    solver_time = perf_counter() - start
    if stats is not None:
        stats.update(variables = len(x), clauses = 0, encoding_time = encoding_time, solver_time = solver_time)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    solution = [[0] * size for _ in range(size)]
    for row in range(size):
        for col in range(size):
            for value in range(1, size + 1):
                if solver.Value(x[(row, col, value)]) == 1:
                    solution[row][col] = value

    return solution

# Gurobi(ILP)
def solve_gurobi(sudoku, stats = None):
    size = len(sudoku)
    start = perf_counter()
    model = gp.Model("sudoku")
    model.setParam('OutputFlag', 0)
    x = model.addVars(size, size, size, vtype=GRB.BINARY, name = "x")
    for row in range(size):
        for col in range(size):
            sum = 0
            for value in range(size):
                sum += x[row, col, value]
            model.addConstr(sum == 1)

    for unit in get_units(size):
        for value in range(size):
            sum = 0
            for (row, col) in unit:
                sum += x[row, col, value]
            model.addConstr(sum == 1)

    for row in range(size):
        for col in range(size):
            if sudoku[row][col] != 0:
                value = sudoku[row][col] - 1
                model.addConstr(x[row, col, value] == 1)

    encoding_time = perf_counter() - start
    start = perf_counter()
    model.optimize()
    solver_time = perf_counter() - start
    if stats is not None:
        stats.update(variables=model.NumVars, clauses=model.NumConstrs, encoding_time=encoding_time, solver_time=solver_time)

    if model.Status != GRB.OPTIMAL:
        return None

    solution = [[0] * size for _ in range(size)]
    for row in range(size):
        for col in range(size):
            for value in range(size):
                if x[row, col, value].X > 0.5:
                    solution[row][col] = value + 1

    return solution

# CPLEX(ILP) - mip
def solve_cplex_mip(sudoku, stats=None):
    size = len(sudoku)
    start = perf_counter()
    model = Model("sudoku")
    x = model.binary_var_cube(size, size, size, name = "x")

    for row in range(size):
        for col in range(size):
            sum = 0
            for value in range(size):
                sum += x[row, col, value]
            model.add_constraint(sum == 1)

    for unit in get_units(size):
        for value in range(size):
            sum = 0
            for (row, col) in unit:
                sum += x[row, col, value]
            model.add_constraint(sum == 1)

    for row in range(size):
        for col in range(size):
            if sudoku[row][col] != 0:
                model.add_constraint(x[row, col, sudoku[row][col] - 1] == 1)

    encoding_time = perf_counter() - start
    start = perf_counter()
    solution_obj = model.solve(log_output=False)
    solver_time = perf_counter() - start
    if stats is not None:
        stats.update(variables=model.number_of_variables, clauses=model.number_of_constraints, encoding_time=encoding_time, solver_time=solver_time)

    if solution_obj is None:
        return None

    solution = [[0] * size for _ in range(size)]
    for row in range(size):
        for col in range(size):
            for value in range(size):
                if solution_obj.get_value(x[row, col, value]) > 0.5:
                    solution[row][col] = value + 1

    return solution    
        
# CPLEX(ILP) - cp
def solve_cplex_cp(sudoku, stats=None):
    size = len(sudoku)
    start = perf_counter()
    model = CpoModel(name="sudoku")
    cells = {}
    for row in range(size):
        for col in range(size):
            cells[(row, col)] = model.integer_var(1, size, f"cell_{row}_{col}")

    for unit in get_units(size):
        model.add(model.all_diff([cells[(row, col)] for (row, col) in unit]))

    for row in range(size):
        for col in range(size):
            if sudoku[row][col] != 0:
                model.add(cells[(row, col)] == sudoku[row][col])

    encoding_time = perf_counter() - start
    start = perf_counter()
    solution_obj = model.solve(LogVerbosity="Quiet")
    solver_time = perf_counter() - start

    if stats is not None:
        stats.update(variables=size * size, clauses=len(get_units(size)) * 3, encoding_time=encoding_time, solver_time=solver_time)

    if not solution_obj:
        return None

    solution = [[0] * size for _ in range(size)]
    for row in range(size):
        for col in range(size):
            solution[row][col] = solution_obj[cells[(row, col)]]

    return solution

# name solver -> function
OTHER_SOLVERS = {
    "cp-sat": solve_cpsat,
    "gurobi": solve_gurobi,
    "cplex-mip": solve_cplex_mip,
    "cplex-cp": solve_cplex_cp,
}