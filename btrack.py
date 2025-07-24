import numpy as np
import utils

# Backtracking solver
# Progress is tracked in a list of tuples describing the state of the puzzle
# Each tuple/state contains: [0] the board/array updated with the latest guess
#                            [1] the latest cell (numbered from 0 to 80, left to right then top to bottom) that was updated
#                            [2] the number guessed for that cell

# Scan starting from the latest cell that was filled to find the next blank cell,
# then guess the smallest possibility that exist for that cell
def find_next_empty_n_fill(S):
    A_curr = np.copy(S[-1][0])
    prev_cell_no = S[-1][1]
    row = prev_cell_no // 9
    col = prev_cell_no % 9
    for cell_no in range(prev_cell_no, 81):
        row = cell_no // 9
        col = cell_no % 9
        if A_curr[row, col, 10] == 0:
            break
    choice = 1
    while A_curr[row, col, choice] == 0:
        choice += 1
    utils.set_cell(A_curr, row, col, choice)
    S.append((A_curr, cell_no, choice))


# Take back the last guess, and
# i) try the next smallest remaining possibility for the latest cell
# ii) if no more possibilities remain for that cell, take back the guess in the previous blank cell
# iii) repeat i) and ii) until a next smallest remaining possibility guess can be made in the cell taken back
# i.e. we have backtracked until a new branch is found
def backtrack_n_find_branch(S):
    branched_off = 0
    while branched_off == 0:
        S_curr = S.pop()
        if len(S) == 0:
            return -1
        A_curr = np.copy(S[-1][0])
        cell_no = S_curr[1]
        row = cell_no // 9
        col = cell_no % 9
        choice = S_curr[2]
        for next_choice in range(choice + 1, 10):
            if A_curr[row, col, next_choice] == 1:
                utils.set_cell(A_curr, row, col, next_choice)
                S.append((A_curr, cell_no, next_choice))
                branched_off = 1
                break
    return 1


# To solve by backtracking, start filling the empty cells one-by-one, and check if any errors are detected.
# Once an error occurs, backtrack to find the next branch, and start filling cells one-by one from there.
# Repeat until the correct branch is found, which leads to the correct answer.
def run_backtrack_solver(A):
    S = [(A, -1, 0)]
    while True:
        while not (utils.check4errors(S[-1][0])) and not (utils.puzzle_complete(S[-1][0])):
            find_next_empty_n_fill(S)
            print(f"Filled in {S[-1][1:3]}")
            utils.show_puzzle(S[-1][0])
            # input("Press any key to continue")
        if utils.puzzle_complete(S[-1][0]) and not (utils.check4errors(S[-1][0])):
            break
        btrack_status = backtrack_n_find_branch(S)
        if btrack_status == -1:
            print("Error when backtracking, no solution possible!")
            break
        print(f"Filled in {S[-1][1:3]}")
        utils.show_puzzle(S[-1][0])
        # input("Press any key to continue")
        if utils.puzzle_complete(S[-1][0]) and not (utils.check4errors(S[-1][0])):
            break
    print("Puzzle completed!")