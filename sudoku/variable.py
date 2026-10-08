# convert Sudoku coordinates to a SAT ID
def var(row, col, value):

    return (row - 1) * 81 + (col - 1) * 9 + value

# convert a SAT ID back to Sudoku coordinates
def decode_var(variable):
    row = (variable - 1) // 81 + 1

    col = ((variable - 1) % 81) // 9 + 1

    value = (variable - 1) % 9 + 1

    return row, col, value