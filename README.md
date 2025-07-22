# Sudoku Solver

## Introduction

Welcome to my Sudoku solver. This is just a personal project I embarked on to get more familiar with Python.  

Two different solvers have been coded:  
1. A solver that uses conventional Sudoku strategies to systematically eliminate possibilities, and 
2. A brute-force solver that uses the backtracking algorithm.

## Data Structure

The puzzle is stored and processed as a 9x9x11 numpy array. The 11 items contained in each cell of the puzzle represent:  

| Item no. | Represents                                                                                                                                                                                                    |
|----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0        | Which 3x3 square, numbered 1-9, starting from the top left and incrementing left-to-right before moving to the next row. Eventually not a useful piece of data to store, may be removed in a future revision. |
| 1-9      | Whether '1', '2',..., '9' is a possible answer in this cell, indicated by a 1 or 0                                                                                                                            |
| 10       | 0 if the answer to this cell has not been decided, digit from 1 to 9 if it has                                                                                                                                |  

In this way, what possibilities remain for each cell can be tracked as the puzzle is being solved. And once the value for any cell has been decided, all the possibilities will be set to 0.  

When checking for errors, other than verifying that there are not repeated numbers along each row and column and in each 3x3 square, we also verify that there are no cells with no possibilities left (which would make the puzzle unsolvable).  

## Solve by Sudoku strategies
The strategies are well known, and are clearly described by [sudoku.com](https://sudoku.com/sudoku-rules/)  

Each strategy for identifying the answer for a cell or eliminating possibilities from a cell is coded as one (or in some cases two) functions in `utils.py`. As of this moment, Hidden Triplets, X-wing, Y-wing and Swordfish have not been coded. Nonetheless, it seems that even the most difficult puzzles can be solved with the available strategies.  

If the user chooses to solve the puzzle using the strategies, the code will apply the different strategies one-by-one, and if the puzzle has not been solved after the last strategy is applied, repeat the process again.  

## Solve by backtracking algorithm
For this, the current state of the puzzle is tracked as a tuple consisting `(current puzzle state, cell_no just filled, digit just filled in cell)`. The cell numbers run from 0 to 80, starting from the top left and incrementing left-to-right before moving to the next row. As the cells are filled, a list of such tuples is constructed to help keep track of the progress. And when backtracking is performed, the latest tuple is popped from the list and the information used to progress to a new branch.  

The solver will fill the first blank cell with the smallest possible answer, and repeat with subsequent blank cells. If it reaches a state where an error is detected, it will take back the attempt, and try to fill the latest cell with the next smallest possible answer. If no possibilities remain in that cell, the solver will then proceed to backtrack by one more cell, and try the next smallest possibility there instead.  

This process continues until the whole puzzle is filled without any errors.  

## Work in-progress

Things that I'd still like to do:  
- Make a UI. Probably using Streamlit for starters. One day I might try Pygame or Pyglet.
- Finish coding Hidden Triplets, X-wing, Y-wing and Swordfish. 
- Tidy up the strategy codes more. At the moment there are still many layers of nested loops.
- Figure out if there's a way to increase the efficiency (on average) of the backtrack algorithm.
- Compare how much faster solving by strategy is compared to backtracking.