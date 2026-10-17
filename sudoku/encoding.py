from itertools import combinations


# At Least One
def add_alo(clauses, variables):

    clauses.append(list(variables))


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
                clauses.append([-x, binary_vars[bit]])
            else:
                clauses.append([-x, -binary_vars[bit]])

    return next_var


# At Most One (Sequential Counter)
def add_amo_sequential(clauses, variables, next_var):

    n = len(variables)

    if n < 2:
        return next_var

    s = list(range(next_var, next_var + n - 1))
    next_var += n - 1
    clauses.append([-variables[0], s[0]])

    for i in range(1, n - 1):

        clauses.append([-variables[i], s[i]])
        clauses.append([-s[i - 1], s[i]])
        clauses.append([-variables[i], -s[i - 1]])

    clauses.append([-variables[n - 1], -s[n - 2]])

    return next_var


# At Most One (Commander Encoding)
def add_amo_commander(clauses, variables, next_var, group_size=3):

    n = len(variables)
    if n <= group_size:
        for a, b in combinations(variables, 2):
            clauses.append([-a, -b])
        return next_var

    commanders = []
    for start in range(0, n, group_size):
        group = variables[start:start + group_size]
        for a, b in combinations(group, 2):
            clauses.append([-a, -b])

        commander = next_var
        next_var += 1
        for x in group:
            clauses.append([-x, commander])

        commanders.append(commander)

    return add_amo_commander(clauses, commanders, next_var, group_size)

# At Most One (Product Encoding)
def add_amo_product(clauses, variables, next_var):
    n = len(variables)
    if n < 2:
        return next_var

    p = 1
    while p * p < n:
        p += 1
    q = p
    row_vars = []
    for _ in range(p):
        row_vars.append(next_var)
        next_var += 1

    col_vars = []
    for _ in range(q):
        col_vars.append(next_var)
        next_var += 1

    for i in range(n):
        x = variables[i]
        clauses.append([-x, row_vars[i // q]])
        clauses.append([-x, col_vars[i % q]])

    next_var = add_amo_sequential(clauses, row_vars, next_var)
    next_var = add_amo_sequential(clauses, col_vars, next_var)

    return next_var

# Map method name -> function
AMO_METHODS = {
    "binary": add_amo_binary,
    "sequential": add_amo_sequential,
    "commander": add_amo_commander,
    "product" : add_amo_product,
}

# Exactly One
def add_exactly_one(clauses, variables, next_var, method="binary"):
    if method not in AMO_METHODS:
        raise ValueError(f"Unknown method '{method}'.")
    add_alo(clauses, variables)

    return AMO_METHODS[method](clauses, variables, next_var)