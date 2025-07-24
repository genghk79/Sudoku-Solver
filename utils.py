import numpy as np

# In here are the functions needed to set up and manipulate the board and define the rules

# Create and return a blank Sudoku board
def create_blank_puzzle():
    A = np.ones((9, 9, 11))
    for row in range(9):
        for col in range(9):
            A[row, col, 0] = 3 * (row // 3) + (col // 3 + 1)
            A[row, col, 10] = 0
    return np.uint8(A)


# Empty an existing Sudoku board
def reset(A):
    for row in range(9):
        for col in range(9):
            for poss in range(1, 10):
                A[row, col, poss] = 1
            A[row, col, 10] = 0


# Firm up an entry in a cell; used to set up board as well as to enter numbers
def set_cell(A, row, col, num):
    for poss in range(1, 10):
        A[row, col, poss] = 0
    A[row, col, 10] = num
    clear_poss(A)

def load_puzzle(fname):
    board = np.zeros((9, 9))
    with open(fname) as f:
        for row in range(9):
            line = f.readline().split(',')
            board[row] = line
    return board

def save_puzzle(fname, board):
    with open(fname, 'w') as f:
        for row in range(9):
            for col in range(9):
                f.write(str(int(board[row,col])))
                if col<8:
                    f.write(',')
            if row<8:
                f.write('\n')


# Enter a 9x9 array of numbers as list, consisting 9 lists of 9 numbers.
# Use 0 to denote a blank cell. i.e. this creates a blank puzzle:
# new_puzzle = set_puzzle([[0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0],
#                          [0,0,0,0,0,0,0,0,0]])
# Checks the entry for conflicts, does a 1st-cut sweep to eliminate possibilities,
# and displays the board as set up.
def set_puzzle(A_in):
    A_in = np.array(A_in)
    if A_in.shape != (9, 9):
        print("Error! Input must be formated as a 9-by-9 list of numbers.")
        return -1
    A_in = A_in.astype(int)
    A = create_blank_puzzle()
    for row in range(9):
        for col in range(9):
            if 0 > A_in[row, col] or A_in[row, col] > 9:
                print("Error! Numbers must be between 0 and 9. Use 0 to indicate a blank.")
                return -1
            elif A_in[row, col] > 0:
                set_cell(A, row, col, A_in[row, col])
    print("Puzzle set:")
    if check4errors(A):
        print("This board is not legal, or has no solution")
    show_puzzle(A)
    return A


# Scan each row, column and square to eliminate possibilities based on current entries
def clear_poss(A):
    for row in range(9):
        for col in range(9):
            if A[row, col, 10] != 0:
                clear_row_poss(A, row, A[row, col, 10])
                clear_col_poss(A, col, A[row, col, 10])
                clear_sqr_poss(A, row, col, A[row, col, 10])


def clear_row_poss(A, row, num):
    for col in range(9):
        A[row, col, num] = 0


def clear_col_poss(A, col, num):
    for row in range(9):
        A[row, col, num] = 0


def clear_sqr_poss(A, row, col, num):
    sqr = A[row, col, 0]
    for row in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
        for col in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
            A[row, col, num] = 0


# Check entries in each row, column, square and look for repeats. Return 1 if there are, 0 if not.
def check4errors(A):
    for row in range(9):
        fixed = A[row, :, 10]
        fixed = fixed[fixed > 0]
        if np.any(np.unique_counts(fixed).counts > 1):
            print(f"Error in row {row}!")
            return 1
    for col in range(9):
        fixed = A[:, col, 10]
        fixed = fixed[fixed > 0]
        if np.any(np.unique_counts(fixed).counts > 1):
            print(f"Error in column {col}!")
            return 1
    for sqr in range(1, 10):
        fixed = A[3 * ((sqr - 1) // 3):3 * ((sqr - 1) // 3) + 3, 3 * ((sqr - 1) % 3):3 * ((sqr - 1) % 3) + 3, 10]
        fixed = fixed[fixed > 0]
        if np.any(np.unique_counts(fixed).counts > 1):
            print(f"Error in square {sqr}!")
            return 1
    for row in range(9):
        for col in range(9):
            if sum(A[row, col, 1:11]) == 0:
                print(f"No possible number in cell ({row}, {col})!")
                return 1
    return 0


# If all numbers are fixed/have been entered, return True
def puzzle_complete(A):
    if np.isin(0, A[:, :, 10]):
        return False
    else:
        return True


def show_puzzle(A):
    for row in range(9):
        for col in range(9):
            if A[row, col, 10] > 0:
                print(f"{A[row, col, 10]}", end=' ')
            else:
                print(".", end=' ')
            if col == 2 or col == 5:
                print("|", end=' ')
            elif col == 8:
                print("")
        if row == 2 or row == 5:
            print("---------------------")


def show_poss(A):
    print("Possibilities left:")
    for row in range(9):
        for poss_row in range(3):
            for col in range(9):
                for n in range(1, 4):
                    if A[row, col, 3 * poss_row + n] == 0:
                        print(".", end='')
                    else:
                        print(3 * poss_row + n, end='')
                print("", end=' ')
                if col == 2 or col == 5:
                    print("|", end=' ')
                elif col == 8:
                    print("")
        if row == 2 or row == 5:
            print("---------------------------------------")
        else:
            print("")