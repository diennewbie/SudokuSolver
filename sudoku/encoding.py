# At Least One 
def add_alo(clauses, variables):

    clauses.append(variables)

# At Most One (Binary Encoding)
def add_amo_binary(clauses, variables, next_var):

    n = len(variables)

    bits = 0

    while (1 << bits) < n:
        bits += 1

    binary_vars = []

    for _ in range(bits):
        binary_vars.append(next_var)
        next_var += 1

    for i in range(n):

        x = variables[i]

        for bit in range(bits):

            bit_value = (i >> bit) & 1

            if bit_value == 1:

                clauses.append([
                    -x,
                    binary_vars[bit]
                ])

            else:

                clauses.append([
                    -x,
                    -binary_vars[bit]
                ])

    return next_var


def add_exactly_one(clauses, variables, next_var):

    add_alo(clauses, variables)

    next_var = add_amo_binary(
        clauses,
        variables,
        next_var
    )

    return next_var