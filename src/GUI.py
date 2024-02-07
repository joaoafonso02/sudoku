# GUI
import pygame
import time
import src.solver as solver

pygame.init()

# Sudoku Game
selected_cell = None
input_digit = None
start_time = None
solved_board = solver.sudoku_board
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

def handle_input_events(events):
    global selected_cell, input_digit, sudoku_board

    for event in events:
        if event.type == pygame.QUIT:
            return True  
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_x, mouse_y = event.pos
                selected_cell = get_clicked_cell(mouse_x, mouse_y)
                print(selected_cell)
                input_digit = None 

        elif event.type == pygame.KEYDOWN:
            if selected_cell is not None:
                if event.unicode.isdigit() and int(event.unicode) in range(1, 10):
                    input_digit = int(event.unicode)
                    update_board(selected_cell, input_digit)

    return False

def update_board(cell, digit):
    row, col = cell
    if sudoku_board[row][col] == 0: # check if cell's empty
        sudoku_board[row][col] = digit
        update_display()

def get_clicked_cell(mouse_x, mouse_y):
    cell_size = width // 9
    col = mouse_x // cell_size
    row = mouse_y // cell_size
    return int(row), int(col)

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

def draw_timer(font, start_time):
    if start_time is not None:
        current_time = int(time.time() - start_time)
        minutes = current_time // 60
        seconds = current_time % 60
        time_text = font.render(f"{minutes}:{seconds:02d}", True, black)
        screen.blit(time_text, (40, 570))

def update_display():
    screen.fill(white)
    draw_grid()
    draw_numbers(sudoku_board, font)
    draw_timer(font, start_time)  # Pass start_time as an argument

    pygame.display.flip()
    
def solve_and_update():
    empty_cell = find_empty_cell(sudoku_board)

    if not empty_cell:
        return True  # Sudoku Solved

    row, col = empty_cell

    for n in range(1, 10):  # between 1-9
        if valid_Move(sudoku_board, row, col, n):
            sudoku_board[row][col] = n
            update_display()
            pygame.time.delay(1)  
            pygame.event.get() 

            if solve_and_update():
                return True 

            sudoku_board[row][col] = 0

    return False

width, height = 550, 550
screen = pygame.display.set_mode((width, height+50))
pygame.display.set_caption("Sudoku Game")
white = (255, 255, 255)
black = (0, 0, 0)
font = pygame.font.Font(None, 32)

def draw_grid():
    cell_size = width // 9
    for i in range(10):
        line_width = 2 if i % 3 == 0 else 1
        pygame.draw.line(screen, black, (i * cell_size, 0), (i * cell_size, height), line_width)
        pygame.draw.line(screen, black, (0, i * cell_size), (width, i * cell_size), line_width)

def draw_numbers(board, font):
    cell_size = width // 9
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text = font.render(str(board[i][j]), True, black)
                x = j * cell_size + cell_size // 3
                y = i * cell_size + cell_size // 3
                screen.blit(text, (x, y))
            
def draw_solver_button(font):
    button_rect = pygame.Rect(475, 565, 70, 30)
    pygame.draw.rect(screen, (210, 210, 210), button_rect)
    text = font.render("Solve", True, black)
    screen.blit(text, (480, 570))
    
def is_mouse_over_button(button_rect):
    mx, my = pygame.mouse.get_pos()
    return button_rect.collidepoint(mx, my)

running = True
clock = pygame.time.Clock()
solve_button_clicked = False  
timer_font = pygame.font.Font(None, 24)
running = True
show_solve_button = True  

while running:
    events = pygame.event.get()
    handle_input_events(events)
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_solve_button and is_mouse_over_button(pygame.Rect(475, 565, 70, 30)):
                solve_button_clicked = True
                show_solve_button = False  # Hide the button
                start_time = time.time()
                
                
    screen.fill(white)
    draw_grid()
    draw_numbers(sudoku_board, font)

    if solve_button_clicked:
        solve_and_update()

    if show_solve_button:
        draw_solver_button(font)

    pygame.display.flip()
    clock.tick(30)  # 30fps

pygame.quit()