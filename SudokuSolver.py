##  Sodoku Solver Script
# - Carlos Ortiz, 20 Aug 2021 -

def PrintBoard(board):
    # Horizontal line
    for ii in range(len(board)):
        # seperate into sections of 3 rows and draw line
        if ii % 3 == 0 and ii != 0:
            print('- - - - - - - - - - -')
        
        # vertical lines
        for jj in range(len(board[0])):
            if jj % 3 == 0 and jj != 0:
                # Print vertical lines after every 3 values 
                print('| ', end = "")

            if jj == 8:
                # Newline after last, otherwise same line and space
                print(board[ii][jj])
            else:
                print(str(board[ii][jj]) + " ", end = "")

def FindEmptySpace(board):
    # increment through all rows and columns
    for ii in range(len(board)):
        for jj in range(len(board[0])):
            # if the value is 0 (empty square), return tuple of row and column
            if board[ii][jj] == 0:
                return (ii, jj) # row, col
                
    return None

def IsValid(board, number, position):
    
    # Check row
    for ii in range(len(board[0])):
        # Check elements in row, see if equal to number we just added in. if so return False
        if board[position[0]][ii] == number and position[1] != ii:
            return False
    
    # check column
    for ii in range(len(board)):
        # Check elements in row, see if equal to number we just added in. if so return False
        if board[ii][position[1]] == number and position[0] != ii:
            return False

    # Check 3x3 cubes
    # Define what box you're in, on board in form of:
    '''
    [
    0,0     0,1     0,2
    1,0     1,1     1,2
    2,0     2,1     2,2
    ]
    '''
    xBox = position[1] // 3
    yBox = position [0] // 3

    # Increment through cubes of numbers
    for ii in range(yBox * 3, yBox * 3 + 3):
        for jj in range(xBox * 3, xBox * 3 + 3):
            # check if any element in box is equal to what you just added
            if board[ii][jj] == number and (ii, jj) != position:
                return False
    
    return True

def SolveBoard(board):

    find = FindEmptySpace(board)
    
    # If false, no empty spaces, so board is solved
    if not find:
        return True
    else:
        # If a value was returned, get row and column number for recursion
        row, col = find


    for ii in range(1, 10):
        # Check if by adding values 1-9 into board is a valid board. If so, keep it
        if IsValid(board, ii, (row, col)):
            board[row][col] = ii
            
            # Keep looping through till solution is found or all numbers are looped and none valid
            if SolveBoard(board):
                return True
            
            board[row][col] = 0

    return False

if __name__ == "__main__":
    
    # example = [
    #     [7, 8, 0, 4, 0, 0, 1, 2, 0],
    #     [6, 0, 0, 0, 7, 5, 0, 0, 9],
    #     [0, 0, 0, 6, 0, 1, 0, 7, 8],
    #     [0, 0, 7, 0, 4, 0, 2, 6, 0],
    #     [0, 0, 1, 0, 5, 0, 9, 3, 0],
    #     [9, 0, 4, 0, 6, 0, 0, 0, 5],
    #     [0, 7, 0, 3, 0, 0, 0, 1, 2],
    #     [1, 2, 0, 0, 0, 7, 4, 0, 0],
    #     [0, 4, 9, 2, 0, 6, 0, 0, 7]
    # ]

    example = [
        [4, 0, 8, 0, 0, 6, 3, 0, 0],
        [3, 0, 0, 7, 0, 0, 0, 0, 0],
        [2, 0, 0, 4, 0, 5, 0, 0, 0],
        [0, 0, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 6, 2, 0, 0, 0, 0, 0],
        [5, 2, 0, 9, 0, 0, 8, 0, 7],
        [0, 4, 0, 8, 0, 2, 5, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 8, 0],
        [7, 0, 0, 0, 1, 3, 0, 6, 0]
    ]

    print("\nSodoku Solver:\n\nSolving Example Case:\n")
    print("\nBefore:\n")
    PrintBoard(example)
    SolveBoard(example)
    print("\n---------------------\n")
    print("\nAfter:\n")
    PrintBoard(example)
    print("")