# convert Sudoku coordinates to a SAT ID
def var(row, col, value, size):

    return (row - 1) * size * size + (col - 1) * size + value

# convert a SAT ID back to Sudoku coordinates
def decode_var(variable, size):
    row = (variable - 1) // (size * size) + 1

    col = ((variable - 1) % (size * size)) // size + 1

    value = (variable - 1) % size + 1

    return row, col, value