import numpy as np
import utils

# Next comes the Sudoku strategies. Using the names given by sudoku.com

# If a cell has only one possibility left, fix/enter it
def check_obvious_singles(A):
    made_change = 0
    for row in range(9):
        for col in range(9):
            if sum(A[row, col, 1:10]) == 1:
                num2fix = np.where(A[row, col, 1:10] == 1)[0][0] + 1
                utils.set_cell(A, row, col, num2fix)
                made_change = 1
    if made_change == 1:
        print("Filled in cells with only one possible value after eliminating values already filled in their row/column/square")
        utils.show_puzzle(A)
        print()
    return made_change


# If any row, column, square has a possibility that exist only in one cell, fix/enter it
def check_hidden_singles(A):
    made_change = 0
    made_change += check_hidden_single_sqr(A)
    made_change += check_hidden_single_row(A)
    made_change += check_hidden_single_col(A)
    if made_change > 0:
        print("Filled in cell where they're the only ones that can take that value in a row/column/square")
        utils.show_puzzle(A)
        print()

    return 0 if made_change == 0 else 1


def check_hidden_single_row(A):
    made_change = 0
    for row in range(9):
        for poss in range(1, 10):
            if sum(A[row, :, poss]) == 1:
                col2fix = np.where(A[row, :, poss] == 1)[0][0]
                utils.set_cell(A, row, col2fix, poss)
                made_change = 1
    return made_change


def check_hidden_single_col(A):
    made_change = 0
    for col in range(9):
        for poss in range(1, 10):
            if sum(A[:, col, poss]) == 1:
                row2fix = np.where(A[:, col, poss] == 1)[0][0]
                utils.set_cell(A, row2fix, col, poss)
                made_change = 1
    return made_change


def check_hidden_single_sqr(A):
    made_change = 0
    # scan through the squares
    for sqr in range(1, 10):
        # in each square, check each possible value
        for poss in range(1, 10):
            chksum = 0
            row2fix = -1
            col2fix = -1
            # For each poss, use chksum to count how many cells in the square have it
            for row in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
                for col in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
                    if A[row, col, poss] == 1:
                        chksum += 1
                        row2fix = row
                        col2fix = col
            # If that poss showed up only once, fix/enter it
            if chksum == 1:
                utils.set_cell(A, row2fix, col2fix, poss)
                made_change = 1
    return made_change


# If any row, column, square has 2 cells with the same 2 poss left, remove those 2 poss from the rest of the cells
def check_obvious_pairs(A):
    made_change = 0
    A_init = np.copy(A)
    # Scan through all the cells
    for row in range(9):
        for col in range(9):
            # If that cell only has 2 poss left, trigger more checks
            if sum(A[row, col, 1:10]) == 2:
                clear_obvious_pair_row(A, row, col)
                clear_obvious_pair_col(A, row, col)
                clear_obvious_pair_sqr(A, row, col)
    if A.tolist() != A_init.tolist():
        made_change = 1
        print("Considered cells with identical possibility pairs in row/column/square")
        print("Removed those possibilities from other cells in row/column/square")
        print()
        check_obvious_singles(A)
    return made_change


def clear_obvious_pair_row(A, row, col):
    # Scan down the same row, if there's another cell with exact same 2 poss, remove these poss from other cells in the row
    for x in range(9):
        if x == col:
            continue
        elif A[row, x, 1:10].tolist() == A[row, col, 1:10].tolist():
            poss_to_cancel = np.where(A[row, col, 1:10] == 1)[0]
            for xx in range(9):
                if xx == x or xx == col:
                    continue
                A[row, xx, poss_to_cancel[0] + 1] = 0
                A[row, xx, poss_to_cancel[1] + 1] = 0


def clear_obvious_pair_col(A, row, col):
    # Scan down the same column, if there's another cell with exact same 2 poss, remove these poss from other cells in the column
    for y in range(9):
        if y == row:
            continue
        elif A[y, col, 1:10].tolist() == A[row, col, 1:10].tolist():
            poss_to_cancel = np.where(A[row, col, 1:10] == 1)[0]
            for yy in range(9):
                if yy == y or yy == row:
                    continue
                A[yy, col, poss_to_cancel[0] + 1] = 0
                A[yy, col, poss_to_cancel[1] + 1] = 0


def clear_obvious_pair_sqr(A, row, col):
    # Scan in the same square, if there's another cell with exact same 2 poss, remove these poss from other cells in the square
    sqr = 3 * (row // 3) + (col // 3 + 1)
    for x in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
        for y in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
            if x == col and y == row:
                continue
            elif A[y, x, 1:10].tolist() == A[row, col, 1:10].tolist():
                poss_to_cancel = np.where(A[row, col, 1:10] == 1)[0]
                for xx in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
                    for yy in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
                        if (xx == x and yy == y) or (xx == col and yy == row):
                            continue
                        A[yy, xx, poss_to_cancel[0] + 1] = 0
                        A[yy, xx, poss_to_cancel[1] + 1] = 0


# If any row, column, square has 3 cells with the same poss left that draw from the same 3 numbers, remove these 3 poss from the other cells
def check_obvious_triplets(A):
    made_change = 0
    A_init = np.copy(A)
    # Scan each row, note all the cells along row with only 2 or 3 possibilities
    for row in range(9):
        ind = np.where(np.logical_or(np.sum(A[row, :, 1:10], axis=1) == 2, np.sum(A[row, :, 1:10], axis=1) == 3))[0]
        # If there are less than 3 such cells, do nothing more
        if len(ind) < 3:
            continue
        # Otherwise, check all combinations of 3 cells, whether they only draw from 3 possibilities
        for i1 in range(len(ind)):
            for i2 in range(i1 + 1, len(ind)):
                for i3 in range(i2 + 1, len(ind)):
                    poss_union = np.bitwise_or(np.bitwise_or(A[row, ind[i1], 1:10], A[row, ind[i2], 1:10]),
                                               A[row, ind[i3], 1:10])
                    # if yes, remove these 3 possibilities from other cells in the row
                    if sum(poss_union) == 3:
                        trip_cols = np.array([ind[i1], ind[i2], ind[i3]])
                        trip = (np.where(poss_union) + np.array([1, 1, 1]))[0]
                        for col in range(9):
                            if np.isin(col, trip_cols):
                                continue
                            for poss in trip:
                                A[row, col, poss] = 0
    # Scan each column, note all the cells along column with only 2 or 3 possibilities
    for col in range(9):
        ind = np.where(np.logical_or(np.sum(A[:, col, 1:10], axis=1) == 2, np.sum(A[:, col, 1:10], axis=1) == 3))[0]
        # If there are less than 3 such cells, do nothing more
        if len(ind) < 3:
            continue
        # Otherwise, check all combinations of 3 cells, whether they only draw from 3 possibilities
        for i1 in range(len(ind)):
            for i2 in range(i1 + 1, len(ind)):
                for i3 in range(i2 + 1, len(ind)):
                    poss_union = np.bitwise_or(np.bitwise_or(A[ind[i1], col, 1:10], A[ind[i2], col, 1:10]),
                                               A[ind[i3], col, 1:10])
                    # if yes, remove these 3 possibilities from other cells in the column
                    if sum(poss_union) == 3:
                        trip_rows = np.array([ind[i1], ind[i2], ind[i3]])
                        trip = (np.where(poss_union) + np.array([1, 1, 1]))[0]
                        for row in range(9):
                            if np.isin(row, trip_rows):
                                continue
                            for poss in trip:
                                A[row, col, poss] = 0
    # Scan each square, note all the cells in square with only 2 or 3 possibilities
    for sqr in range(1, 10):
        A_sqr = A[3 * ((sqr - 1) // 3):3 * ((sqr - 1) // 3) + 3, 3 * ((sqr - 1) % 3):3 * ((sqr - 1) % 3) + 3]
        ind = np.where(np.logical_or(np.sum(A_sqr[:, :, 1:10], axis=2) == 2, np.sum(A_sqr[:, :, 1:10], axis=2) == 3))
        # If there are less than 3 such cells, do nothing more
        if len(ind[0]) < 3:
            continue
        # Otherwise, check all combinations of 3 cells, whether they only draw from 3 possibilities
        for i1 in range(len(ind[0])):
            for i2 in range(i1 + 1, len(ind[0])):
                for i3 in range(i2 + 1, len(ind[0])):
                    poss_union = np.bitwise_or(A_sqr[ind[0][i1], ind[1][i1], 1:10], A_sqr[ind[0][i2], ind[1][i2], 1:10])
                    poss_union = np.bitwise_or(poss_union, A_sqr[ind[0][i3], ind[1][i3], 1:10])
                    # if yes, remove these 3 possibilities from other cells in the column
                    if sum(poss_union) == 3:
                        trip_ind = np.array(
                            [[ind[0][i1], ind[0][i2], ind[0][i3]], [ind[1][i1], ind[1][i2], ind[1][i3]]])
                        trip = (np.where(poss_union) + np.array([1, 1, 1]))[0]
                        for row in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
                            for col in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
                                if np.all(np.array([row, col]) == trip_ind[:, 0] + np.array(
                                        [3 * ((sqr - 1) // 3), 3 * ((sqr - 1) % 3)])) or \
                                        np.all(np.array([row, col]) == trip_ind[:, 1] + np.array(
                                            [3 * ((sqr - 1) // 3), 3 * ((sqr - 1) % 3)])) or \
                                        np.all(np.array([row, col]) == trip_ind[:, 2] + np.array(
                                            [3 * ((sqr - 1) // 3), 3 * ((sqr - 1) % 3)])):
                                    continue
                                for poss in trip:
                                    A[row, col, poss] = 0
    if A.tolist() != A_init.tolist():
        made_change = 1
        print("Considered a triplet of possibilities exist only in the 3 cells in one row/column/square")
        print("Removed these possibilities from other cells in row/column/square")
        print()
        check_obvious_singles(A)
    return made_change


# If 2 poss exist only in 2 cells in a row/column/square, then these must be the only 2 poss in those 2 cells, remove other poss there
def check_hidden_pairs(A):
    made_change = 0
    A_init = np.copy(A)
    # Scan each row and each possibility
    for row in range(9):
        for poss1 in range(1, 10):
            # If there's a possibility that exists only twice in the row, mark the position and look for another one
            if sum(A[row, :, poss1]) == 2:
                poss1_pos = np.where(A[row, :, poss1] == 1)[0].tolist()
                for poss2 in range(poss1 + 1, 10):
                    # If a 2nd possibility that exists only twice is found, check if their positions are the same
                    # Clear other possibilities in those cells if the positions are the same
                    if sum(A[row, :, poss2]) == 2:
                        poss2_pos = np.where(A[row, :, poss2] == 1)[0].tolist()
                        if poss1_pos == poss2_pos:
                            for poss in range(1, 10):
                                if poss == poss1 or poss == poss2:
                                    continue
                                A[row, poss1_pos[0], poss] = 0
    # Scan each column and each possibility
    for col in range(9):
        for poss1 in range(1, 10):
            # If there's a possibility that exists only twice in the column, mark the position and look for another one
            if sum(A[:, col, poss1]) == 2:
                poss1_pos = np.where(A[:, col, poss1] == 1)[0].tolist()
                for poss2 in range(poss1 + 1, 10):
                    # If a 2nd possibility that exists only twice is found, check if their positions are the same
                    # Clear other possibilities in those cells if the positions are the same
                    if sum(A[:, col, poss2]) == 2:
                        poss2_pos = np.where(A[:, col, poss2] == 1)[0].tolist()
                        if poss1_pos == poss2_pos:
                            for poss in range(1, 10):
                                if poss == poss1 or poss == poss2:
                                    continue
                                A[poss1_pos[0], col, poss] = 0
    # Scan each square and each possibility
    for sqr in range(1, 10):
        # Slice out that square
        A_sqr = A[3 * ((sqr - 1) // 3):3 * ((sqr - 1) // 3) + 3, 3 * ((sqr - 1) % 3):3 * ((sqr - 1) % 3) + 3]
        for poss1 in range(1, 10):
            # If there's a possibility that exists only twice in the square, mark the position and look for another one
            if sum(sum(A_sqr[:, :, poss1])) == 2:
                poss1_pos_row = np.where(A_sqr[:, :, poss1] == 1)[0].tolist()
                poss1_pos_col = np.where(A_sqr[:, :, poss1] == 1)[1].tolist()
                for poss2 in range(poss1 + 1, 10):
                    # If a 2nd possibility that exists only twice is found, check if their positions are the same
                    # Clear other possibilities in those cells if the positions are the same
                    if sum(sum(A_sqr[:, :, poss2])) == 2:
                        poss2_pos_row = np.where(A_sqr[:, :, poss2] == 1)[0].tolist()
                        poss2_pos_col = np.where(A_sqr[:, :, poss2] == 1)[1].tolist()
                        if np.all(poss1_pos_row == poss2_pos_row) and np.all(poss1_pos_col == poss2_pos_col):
                            for poss in range(1, 10):
                                if poss == poss1 or poss == poss2:
                                    continue
                                A[3 * ((sqr - 1) // 3) + poss1_pos_row[0], 3 * ((sqr - 1) % 3) + poss1_pos_col[
                                    0], poss] = 0
                                A[3 * ((sqr - 1) // 3) + poss1_pos_row[1], 3 * ((sqr - 1) % 3) + poss1_pos_col[
                                    1], poss] = 0
    if A.tolist() != A_init.tolist():
        made_change = 1
        print("Considered a pair of possibilities exist only in the same 2 cells in one row/column/square")
        print("Removed other possibilities from those 2 cells, leaving just the pair")
        print()
        check_obvious_singles(A)
    return made_change


# If any square has a poss that exist in only one row/column, remove this poss from the rest of the row/column (that's not in this square)
def check_pointing_pair_trip_sqr(A):
    made_change = 0
    A_init = np.copy(A)
    for sqr in range(1, 10):
        # Slice out that square
        A_sqr = A[3 * ((sqr - 1) // 3):3 * ((sqr - 1) // 3) + 3, 3 * ((sqr - 1) % 3):3 * ((sqr - 1) % 3) + 3]
        for poss in range(1, 10):
            poss_pos = np.where(A_sqr[:, :, poss] == 1)
            # For each poss, check if the row/columns numbers are all the same, if yes remove poss in same row/column in other squares
            if len(np.unique(poss_pos[0])) == 1:
                row = 3 * ((sqr - 1) // 3) + poss_pos[0][0]
                for col in range(6):
                    A[row, (col + 3 * ((sqr - 1) % 3) + 3) % 9, poss] = 0
            if len(np.unique(poss_pos[1])) == 1:
                col = 3 * ((sqr - 1) % 3) + poss_pos[1][0]
                for row in range(6):
                    A[(row + 3 * ((sqr - 1) // 3) + 3) % 9, col, poss] = 0
    if A.tolist() != A_init.tolist():
        made_change = 1
        print("Considered possibilities in a square that exist only in one row/column")
        print("Removed those possibilities from other cells along same row/column but in other squares")
        print()
        check_obvious_singles(A)
    return made_change


# If any row/column has a poss that exist in only one square, remove this poss from the rest of the square
def check_pointing_pair_trip_rowcol(A):
    made_change = 0
    A_init = np.copy(A)
    # Scan each row, check if any poss exists only in one square
    for row in range(9):
        for poss in range(1, 10):
            poss_sqr = A[row, np.where(A[row, :, poss] == 1), 0]
            # If yes, remove poss from other rows of this square
            if len(np.unique(poss_sqr)) == 1:
                sqr = poss_sqr[0][0]
                for y in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
                    if y != row:
                        for col in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
                            A[y, col, poss] = 0
    # Scan each column, check if any poss exists only in one square
    for col in range(9):
        for poss in range(1, 10):
            poss_sqr = A[np.where(A[:, col, poss] == 1), col, 0]
            # If yes, remove poss from other columns of this square
            if len(np.unique(poss_sqr)) == 1:
                sqr = poss_sqr[0][0]
                for x in range(3 * ((sqr - 1) % 3), 3 * ((sqr - 1) % 3) + 3):
                    if x != col:
                        for row in range(3 * ((sqr - 1) // 3), 3 * ((sqr - 1) // 3) + 3):
                            A[row, x, poss] = 0
    if A.tolist() != A_init.tolist():
        made_change = 1
        print("Considered possibilities in a row/column that exist only in one square")
        print("Removed those possibilities from other cells in the same square but in other row/column")
        print()
        check_obvious_singles(A)
    return made_change

# Try to solve the puzzle by running through the different strategies
def run_solve(A):
    print("Start state:")
    utils.show_puzzle(A)
    print()
    made_change = 1
    while made_change != 0:
        made_change = 0
        print('check_obvious_singles')
        made_change += check_obvious_singles(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

        print('check_hidden_singles')
        made_change += check_hidden_singles(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

        print('check_obvious_pairs')
        made_change += check_obvious_pairs(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

        print('check_obvious_triplets')
        made_change += check_obvious_triplets(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

        print('check_hidden_pairs')
        made_change += check_hidden_pairs(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

        print('check_pointing_pair_trip_sqr')
        made_change += check_pointing_pair_trip_sqr(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

        print('check_pointing_pair_trip_rowcol')
        made_change += check_pointing_pair_trip_rowcol(A)
        if utils.check4errors(A):
            break
        elif utils.puzzle_complete(A):
            print("Puzzle completed!")
            utils.show_puzzle(A)
            break

    else:
        print("Stuck! No change after cyling through all strategies.")
        utils.show_puzzle(A)