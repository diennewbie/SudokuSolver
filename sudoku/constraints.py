from .variable import var
from .encoding import add_exactly_one


def build_constraints(size):

    clauses = []

    next_var = size ** 3 + 1
    block_size = int(size ** 0.5)

# Each cell must contain exactly one value
    for row in range(1, size + 1):

        for col in range(1, size + 1):

            variables = []

            for value in range(1, size + 1):

                variables.append(
                    var(row, col, value, size)
                )

            next_var = add_exactly_one(
                clauses,
                variables,
                next_var
            )

# Each value must appear exactly once in each row
    for row in range(1, size + 1):

        for value in range(1, size + 1):

            variables = []

            for col in range(1, size + 1):

                variables.append(
                    var(row, col, value, size)
                )

            next_var = add_exactly_one(
                clauses,
                variables,
                next_var
            )

# Each value must appear exactly once in each column
    for col in range(1, size + 1):

        for value in range(1, size + 1):

            variables = []

            for row in range(1, size + 1):

                variables.append(
                    var(row, col, value, size)
                )

            next_var = add_exactly_one(
                clauses,
                variables,
                next_var
            )

# Each value must appear exactly once in each block
    for block_row in range(block_size):

        for block_col in range(block_size):

            for value in range(1, size + 1):

                variables = []

                for row in range(
                    block_row * block_size + 1,
                    block_row * block_size + block_size + 1
                ):

                    for col in range(
                        block_col * block_size + 1,
                        block_col * block_size + block_size + 1
                    ):

                        variables.append(
                            var(row, col, value, size)
                        )

                next_var = add_exactly_one(
                    clauses,
                    variables,
                    next_var
                )

    return clauses, next_var