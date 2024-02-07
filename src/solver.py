# Sudoku Game

# starting Sudoku board
sudoku_board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

def print_board(board):
    print(" ------ ------- ------- ")
    for i, row in enumerate(board):
        if i % 3 == 0 and i != 0:
            print(" ------- ------- ------- ") 

        for j, value in enumerate(row):
            if j % 3 == 0:
                print("|", end=" ")

            print(value if value != 0 else "0", end=" ")

            if j == 8:
                print("|")

    print(" ------- ------- ------- \n")
    
# Display initial Sudoku board 
print("Initial Board:")
print_board(sudoku_board)

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None
                
def valid_Move(board, row, col, n):
    # Check if 'n' is not present in the current row
    if any(board[row][i] == n for i in range(9)):
        return False
    
    # Check if 'n' is not present in the current col
    if n in [board[i][col] for i in range(9)]:
        return False
    
    # Check if 'n' is not present in the current square
    start_row = 3 * (row // 3)
    start_col = 3 * (col // 3)
    if n in [board[i][j] for i in range(start_row, start_row + 3) for j in range(start_col, start_col + 3)]:
        return False  
    
    return True
    
def solve_sudoku(board):
    empty_celll = find_empty_cell(board)
    
    if not empty_celll:
        return True; # Sudoku Solved
    
    row, col = empty_celll
    
    for n in range(1,10): # between 1-9
        if valid_Move(board, row, col, n):
            board[row][col] = n
            
            if solve_sudoku(board):
                return True # solved
            
            board[row][col] = 0
            
    return False

solve_sudoku(sudoku_board)


# Display the solved Sudoku board
print("Solved Board:")
print_board(sudoku_board)


        