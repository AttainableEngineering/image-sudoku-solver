import SudokuSolver
from BoardFromImg import GetBoardFromAppSC as GB

# Header
print("\nSudoku Engine:\n")

##
'''
In future iterations, get a request for a photo from online
'''

# Get Unsolved Board
print("...getting board...")
board = GB()
# board = GB("sudoku2.jpg") ## run default case until have website to host
print("\n\nUnsolved Board:\n")
SudokuSolver.PrintBoard(board)

# Median
print("\n----------------------\n")
print("...solving...")

# Solve Board
SudokuSolver.SolveBoard(board)
print("\n\nSolved Board:\n")
SudokuSolver.PrintBoard(board)
print('')