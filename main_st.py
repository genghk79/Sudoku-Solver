from os import WCONTINUED

import streamlit as st
import numpy as np
import utils
import strat
import btrack
import time

# st.set_page_config(layout="wide")

# Initialize grid state
if "board" not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)
if "solver_state" not in st.session_state:
    st.session_state.solver_state = 0
if "solver_info" not in st.session_state:
    st.session_state.solver_info = 0

c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns(9)

def update_board(row,col,input_no):
    if st.session_state[input_no] == '':
        st.session_state.board[row,col] = 0
    else:
        try:
            st.session_state.board[row,col] = int(st.session_state[input_no])
        except:
            pass

st.title("Sudoku Solver")

st.markdown("""
    Welcome to my Sudoku Solver!  
    This is just a personal project I embarked on to get more familiar with Python.
    """)
st.divider()
st.subheader("Step 1: Key in the Sudoku puzzle to solve")
c1, c2 = st.columns(2)
with c1:
    if st.button("Load previous board/puzzle"):
        st.session_state.board = utils.load_puzzle("last_used_puzzle.txt")
with c2:
    if st.button("Clear board"):
        st.session_state.board = np.zeros((9, 9), dtype=int)

for sqr_row in range(3):  # 0 for top, 1 for middle, 2 for bottom
    with st.container():
        sqr_cols = st.columns(3, border=True)  # 3 blocks in a row
        for sqr, st_sqr in enumerate(sqr_cols):  # Left to right 3x3 blocks
            with st_sqr:
                col_blocks = st.columns(3)  # 3 columns inside each block
                for col, st_col in enumerate(col_blocks):
                    with st_col:
                        for row in range(3):  # 3 rows per block
                            row_no = 3*sqr_row + row
                            col_no = 3*sqr + col
                            cell_id = f"cell{row_no}{col_no}"
                            input_key = f"input{row_no}{col_no}"
                            st.text_input(
                                cell_id,
                                value=('' if st.session_state.board[row_no,col_no]==0 else int(st.session_state.board[row_no,col_no])),
                                max_chars=1,
                                key=input_key,
                                label_visibility="hidden",
                                on_change=update_board,
                                args=(row_no, col_no, input_key)
                            )

see_board = st.expander("You can see the numpy array of the board if you want")
see_board.write(st.session_state['board'])

st.divider()

st.subheader("Step 2: Choose which solver to use")
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        solver = st.radio("Solver choice:",["Sudoku strategies","Backtracking algorithm"],
                          captions=['As explained on [sudoku.com](https://sudoku.com/sudoku-rules/)',
                                    "Brute-force but systematic search"])
    with c2:
        step_by_step = st.radio("Do you want to see the solver working step-by-step?",
                                ["No","Yes"])
        if step_by_step == "Yes":
            st.write("How much time (in seconds, max 5s) to wait between each step?")
            step_time = st.number_input("wait time", min_value=0.1, max_value=5.0, step=0.1, format="%0.1f")
        else:
            step_time = 0

st.divider()

st.subheader("Step 3: Watch the solver do its job")
st.write("Just press 'Solve' when you're ready")
A = utils.set_puzzle(st.session_state['board'])

def curr_board(A):
    return A[:,:,10]

def solve_strat(A):
    strategies = [
        'check_obvious_singles',
        'check_hidden_singles',
        'check_obvious_pairs',
        'check_obvious_triplets',
        'check_hidden_pairs',
        'check_pointing_pair_trip_sqr',
        'check_pointing_pair_trip_rowcol'
    ]

    made_change = 1
    while made_change != 0:
        made_change = 0
        for strat_name in strategies:
            st.session_state.solver_info = strat_name
            strategy_fn = getattr(strat, strat_name)
            made_change += strategy_fn(A)

            solver_status.info(f"Solving using `{strat_name}`")
            st.session_state['board'] = curr_board(A)
            show_board()
            time.sleep(step_time)

            if utils.check4errors(A):
                st.session_state.solver_state = -1
                return
            elif utils.puzzle_complete(A):
                st.session_state.solver_state = 1
                return

def solve_btrack(A):
    if "S" not in st.session_state:
        st.session_state.S = [(A, 0, 0)]
    while True:
        while not (utils.check4errors(st.session_state.S[-1][0])) and not (utils.puzzle_complete(st.session_state.S[-1][0])):
            btrack.find_next_empty_n_fill(st.session_state.S)
            solver_status.info(f"Solving with backtracking algorithm")
            st.session_state['board'] = curr_board(st.session_state.S[-1][0])
            show_board()
            time.sleep(step_time)
        if utils.puzzle_complete(st.session_state.S[-1][0]) and not (utils.check4errors(st.session_state.S[-1][0])):
            st.session_state.solver_state = 1
            del st.session_state.S
            break
        btrack_status = btrack.backtrack_n_find_branch(st.session_state.S)
        if btrack_status == -1:
            st.session_state.solver_state = -1
            del st.session_state.S
            break
        st.session_state['board'] = curr_board(st.session_state.S[-1][0])
        show_board()
        time.sleep(step_time)
        if utils.puzzle_complete(st.session_state.S[-1][0]) and not (utils.check4errors(st.session_state.S[-1][0])):
            st.session_state.solver_state = 1
            del st.session_state.S
            break
    print("Puzzle completed!")

def solve_now(A):
    utils.save_puzzle("last_used_puzzle.txt", st.session_state['board'])
    if solver == "Sudoku strategies":
        solve_strat(A)
    else:
        solve_btrack(A)

with st.container():
    c1, c2 = st.columns([15,85])
    with c1:
        st.button("Solve", on_click=solve_now, args=(A,))
    with c2:
        solver_status = st.empty()
        if st.session_state.solver_state == 1:
            solver_status.success(f"Solved successfully!")
        elif st.session_state.solver_state == -1:
            solver_status.error(f"Error while solving!")

board_rows = [st.empty() for _ in range(3)]

def show_row_of_sqr(sqr_row):
    sqr_cols = st.columns(3, border=True)  # 3 blocks in a row
    for sqr, st_sqr in enumerate(sqr_cols):  # Left to right 3x3 blocks
        with st_sqr:
            col_blocks = st.columns(3)  # 3 columns inside each block
            for col, st_col in enumerate(col_blocks):
                with st_col:
                    for row in range(3):  # 3 rows per block
                        row_no = 3*sqr_row + row
                        col_no = 3*sqr + col
                        st.write('.' if st.session_state.board[row_no, col_no]== 0 else str(int(st.session_state.board[row_no, col_no])))

def show_board():
    for i, board_row in enumerate(board_rows):
        with board_row.container():
            show_row_of_sqr(i)


show_board()

