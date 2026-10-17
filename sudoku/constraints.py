from .variable import var
from .encoding import add_exactly_one


def build_constraints(size, method="binary"):
    if size < 1 :
        raise ValueError("Size must be a positive integer.")
    block_size = int(size ** 0.5)
    if block_size ** 2 != size:
        raise ValueError("Size must be a perfect square.")
    
    clauses = []
    next_var = size ** 3 + 1

# Each cell must contain exactly one value
    for row in range(1, size + 1):
        for col in range(1, size + 1):
            cell_vars = []
            for value in range(1, size + 1):
                cell_vars.append(var(row, col, value, size))
            next_var = add_exactly_one(clauses, cell_vars, next_var, method)

# Each value must appear exactly once in each row
    for row in range(1, size + 1):
        for value in range(1, size + 1):
            row_vars = []
            for col in range(1, size + 1):
                row_vars.append(var(row, col, value, size))
            next_var = add_exactly_one(clauses, row_vars, next_var, method)

# Each value must appear exactly once in each column
    for col in range(1, size + 1):
        for value in range(1, size + 1):
            col_vars = []
            for row in range(1, size + 1):
                col_vars.append(var(row, col, value, size))
            next_var = add_exactly_one(clauses, col_vars, next_var, method)

# Each value must appear exactly once in each block
    for block_row in range(block_size):
        for block_col in range(block_size):
            row_start =  block_row * block_size + 1
            row_end = row_start + block_size
            col_start = block_col * block_size + 1
            col_end = col_start + block_size
            for value in range(1, size + 1):
                block_vars = []
                for row in range(row_start, row_end):
                    for col in range(col_start, col_end):
                        block_vars.append(var(row, col, value, size))
                next_var = add_exactly_one(clauses, block_vars, next_var, method)

    return clauses, next_var