import numpy as np
import utils
import strat
import btrack

# Function to check if the input is 9 integers as required. If ok, save them into the board array.
def input_row_to_array(input_row,board,row):
    row_ok = 0
    input_row = input_row.split(',')
    if len(input_row) != 9:
        print("Please enter a 9-digit row. Let's try again.")
        print()
        return row_ok
    try:
        input_row = [int(item) for item in input_row]
    except ValueError:
        print("Please enter only integers 0 to 9. Let's try again.")
        print()
        return row_ok
    else:
        row_ok = 1
        board[row] = input_row
        return row_ok

# Function to request user to enter 9 rows of 9 numbers to be saved as the board to be solved
def input_to_board():
    board = np.zeros((9, 9))
    row_no = 0
    while row_no < 9:
        in_ok = 0
        while in_ok == 0:
            row_in = input(f"Enter numbers for row no. {row_no+1}: ")
            in_ok = input_row_to_array(row_in,board,row_no)
        row_no += 1
    return board

# Function to allow amendments to the currently filled board
def amend_row(amend_input,A_in):
    amended = 0
    try:
        row2amend = int(amend_input)
    except:
        pass
    else:
        if 0 < row2amend < 10:
            in_ok = 0
            while in_ok == 0:
                row_in = input(f"What would you like to change row {row2amend} to? ")
                in_ok = input_row_to_array(row_in, A_in, row2amend - 1)
            print()
        amended = 1
    return amended

# Start of the Sudoku solver
# The Sudoku solver goes through the following steps:
# 1. Asks the user to choose to reload the previous board/puzzle or to enter a new puzzle
# 2. Allows the user to amend/make changes to the entered puzzle
# 3. Asks the user if the puzzle should be solved by the backtracking method or using Sudoku strategies
# 4. Run the selected solver and display the results
print("Welcome to the Sudoku solver!")
print()
print("Would you like to:")
print("1. Reuse the previous board/puzzle, or")
print("2. Enter a new board/puzzle?")
choice = 0
while choice != 1 and choice != 2:
    choice = input("Please choose option 1 or 2: ")
    try:
        choice = int(choice)
    except:
        pass
print()
if choice == 1:
    print("Load the previous board/puzzle")
    A_in = utils.load_puzzle("last_used_puzzle.txt")
else:
    print("Please enter the puzzle to solve row-by-row as comma separated rows of 9 numbers each.")
    print("You may use the following as a template:")
    print("0, 0, 0, 0, 0, 0, 0, 0, 0")
    print()
    print("'0' represents a blank cell. Replace them with numbers 1-9 for cells with known values.")
    print()

    # Take input to populate the Sudoku board
    A_in = input_to_board()
    print()

# Give the user a chance to make amendments to the board
A = utils.set_puzzle(A_in)
print()
row2amend = input("Would you like to amend any rows? Enter row number (1-9) if yes. Otherwise we shall continue. ")
print()
amended = amend_row(row2amend,A_in)
while amended == 1:
    row2amend = input("Would you like to amend any other rows? Enter row number (1-9) if yes. Otherwise we shall continue. ")
    print()
    amended = amend_row(row2amend, A_in)
A = utils.set_puzzle(A_in)
utils.save_puzzle("last_used_puzzle.txt",A_in)
print()

print("We shall proceed to solve the puzzle. Would you like to use: ")
print("1. strategies as taught on sudoku.com, or")
print("2. brute force i.e. backtracking algorithm?")
solve_by = 0
while solve_by != 1 and solve_by != 2:
    solve_by = input("Please choose option 1 or 2: ")
    try:
        solve_by = int(solve_by)
    except:
        pass
if solve_by == 1:
    strat.run_solve(A)
else:
    btrack.run_backtrack_solver(A)

print()
print('End!')