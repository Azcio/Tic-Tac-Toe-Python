import sys #import System-specific parameters, allows interaction with python environment
import pygame #import libaray for creating games/appliations, functions for handling 
                #graphics, sound and user input
import numpy as np #import library for numerical computations

pygame.init() #Function that initlialises all imported pygame modules

#colours of GUI
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
SEMI_WHITE = (208, 208, 208, 128)
SEMI_BLACK = (0, 0, 0, 94)
selection_colours = [(255, 255, 255), (255, 255, 255), (255, 255, 255)] #used for highlighting the user interactions (X, O, LINES over x & o)

#Proportions & Sizes
LOGICAL_HEIGHT = 750  # height for game calculations
STATUS_BAR_HEIGHT = 50  # Fixed height for the status bar
HEIGHT = LOGICAL_HEIGHT + STATUS_BAR_HEIGHT  # Total screen height
WIDTH = 800
#Board layout
LINE_WIDTH = 5 #thickness of the grid lines used to draw the game board
BOARD_ROWS = 3 #Number of rows
BOARD_COLS = 3 #Number of columns
SQUARE_SIZE = WIDTH // BOARD_COLS #calculate the size of each square on the grid evenly
CIRCLE_RADIUS = SQUARE_SIZE // 3 #radius of the O used in the game
CIRCLE_WIDTH = 15 # thickness of the circle's outline
CROSS_WIDTH = 25 #thickness of the cross symbol

Difficulty = "" #variable named Difficulty = empty string

#create the main window for the game with the title
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) #create and display the window with dimesions from earlier
pygame.display.set_caption('Tic-Tac-Toe') #Create and display the title "Tic-Tac-Toe"

BACKGROUND_IMAGE = pygame.image.load('GameBackground.jpg') #grab and use image as background in the window
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))  # Scale to fit screen

SCREEN.fill(WHITE) #Fill the entire screen with "White", used for tranmission from menu to game
BOARD = np.zeros((BOARD_ROWS, BOARD_COLS)) # create new array filled with zeros with the dimensions of the grid 3x3

def draw_lines(color = SEMI_WHITE): #function to draw grid line with the colour "semi white"
    for i in range(1, BOARD_ROWS): #loop iterates over each row and column of the board, starting at 1
        pygame.draw.line(SCREEN, color, (0, SQUARE_SIZE * i), (WIDTH, SQUARE_SIZE * i), LINE_WIDTH)
        pygame.draw.line(SCREEN, color, (SQUARE_SIZE * i, 0), (SQUARE_SIZE * i, LOGICAL_HEIGHT), LINE_WIDTH)

def draw_figures(color = [RED, WHITE]): #draw X (WHITE) AND O (RED)
    for row in range(BOARD_ROWS): 
        for col in range(BOARD_COLS):
            #check if the current square is 1 (means user interactions)user places here
            if BOARD[row][col] == 1: #then draw circle
                pygame.draw.circle(SCREEN, color[0], (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
         #else if current square is 2 then draw X
            elif BOARD[row][col] == 2:
                pygame.draw.line(SCREEN, color[1], (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), CROSS_WIDTH)
                pygame.draw.line(SCREEN, color[1], (col * SQUARE_SIZE + SQUARE_SIZE // 4, row * SQUARE_SIZE + 3 * SQUARE_SIZE // 4), (col * SQUARE_SIZE + 3 * SQUARE_SIZE // 4, row * SQUARE_SIZE + SQUARE_SIZE // 4), CROSS_WIDTH)

#function that will update game board when player interacts with sqaure
def mark_square(row, col, player):
    BOARD[row][col] = player

#function that will check if a square is empty/available for a player
def available_square(row, col):
    return BOARD[row][col] == 0

#function that will check if grid is full of X/O and no more available space
def is_board_full(check_board = BOARD):
    for row in range(BOARD_ROWS): #loop through every row 
        for col in range(BOARD_COLS): #and every coloum on the board
            if check_board[row][col] == 0: #if a square is 0/empty/availble 
                return False #return false/ board is not completly full
    return True #if there are no 0 then return true theres no more spaces left

#function to check if a player won by coloum
def check_win(player, check_board = BOARD):
    for col in range(BOARD_COLS): #loop through coloum
        #if the 1,2 and 3 coloum has either all 1 or all 2 then return true that player won
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True
        
    #function to check if a player won by row
    for row in range(BOARD_ROWS): #loop through rows
        #if the 1,2 and 3 coloum has either all 1 or all 2 then return true that player won
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True
        
    #function checks for a diagonal win by checking top right corner (2,0), middle (1,1) and bottom left (0,2) 
        if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
         return True
        
     #function checks for a diagonal win by checking top left corner (0,0), middle (1,1) and bottom right (2,2)
        if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
         return True
    
    return False #if diagonal win condition isnt met then false, player didnt win diagonally

#Minimax Algorithm
#checks for win/loss conditions
def minimax(minimax_board, depth, max_depth, is_maximizing):
    if check_win(2, minimax_board):
        return 10 - depth  # Favor quicker wins
    elif check_win(1, minimax_board):
        return depth - 10  # Favor slower losses
    elif is_board_full(minimax_board) or depth == max_depth:
        return 0  # Neutral score for a draw or max depth reached
    
    if is_maximizing:
        best_score = float('-inf')  # Start with the worst score
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2  # Player 2's move
                    score = minimax(minimax_board, depth + 1, max_depth, False)
                    minimax_board[row][col] = 0  # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')  # Start with the best score for minimizing
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1  # Player 1's move
                    score = minimax(minimax_board, depth + 1, max_depth, True)
                    minimax_board[row][col] = 0  # Undo move
                    best_score = min(score, best_score)
        return best_score
        
    #function to determine bots best move using minimax algorithm with max_depth
def best_move(max_depth):
    best_score = float('-inf') # Start with the worst possible score (negative infinity)
    move = (-1, -1) # Placeholder for the best move coordinates/grid square
    
    for row in range(BOARD_ROWS): # loop through all rows
        for col in range(BOARD_COLS): #loop through all colums
            if BOARD[row][col] == 0: # if a square is 0, 
                BOARD[row][col] = 2  # Simulate player 2's move
                score = minimax(BOARD, 0, max_depth, False)  # Call minimax with max_depth
                BOARD[row][col] = 0  # Undo the move
                
                if score > best_score:
                    best_score = score
                    move = (row, col)
    
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)  # Mark the best move on the board
        return True
    return False

def welcome_screen():

    SCREEN.blit(BACKGROUND_IMAGE, (0, 0)) #draw the background image at the top left corner
    custom_font = pygame.font.Font("Font_Style.ttf", 50) #Loads a custom font at size 50
    custom_title = custom_font.render('Welcome to Tic-Tac-Toe!', True, RED) #display title in red
    custom_rect = custom_title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    SCREEN.blit(custom_title, custom_rect)
    
    #display the instructions/game modes in different colours
    font_instructions = pygame.font.Font("Font_Style.ttf", 30)
    instructions = [
        'Press 1 for Easy',
        'Press 2 for Medium',
        'Press 3 for Hard',
    ]
    
    for i, line in enumerate(instructions):
        text = font_instructions.render(line, True, selection_colours[i])
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
        SCREEN.blit(text, text_rect)
    
    pygame.display.update() #call and display all elements

    while True:
        for event in pygame.event.get(): #fetch all mouse events
            if event.type == pygame.QUIT: #if user clicks close window then the program will exit
                sys.exit()
            if event.type == pygame.KEYDOWN:#pygame.KEYDOWN detects when a key is pressed.
                if event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2
                elif event.key == pygame.K_3:
                    return 5

max_depth = welcome_screen() #call welcome_screen function
print(f"I'm at the welcome screen and max depth is {max_depth}")
SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
draw_lines()

player = 1
game_over = False

def draw_retry_button():
    button_width = 200
    button_height = 50
    button_x = (WIDTH - button_width) // 2
    button_y = HEIGHT - 100  # Position below the game board

    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_color = GREEN if (button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height) else WHITE

    pygame.draw.rect(SCREEN, button_color, (button_x, button_y, button_width, button_height), border_radius=10)

    font = pygame.font.Font("Font_Style.ttf", 30)
    text = font.render("Retry", True, BLACK)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    SCREEN.blit(text, text_rect)

    return (button_x, button_y, button_width, button_height)

def draw_status_bar(message="", color=BLACK, font_size=30, difficulty=""):
    status_bar_height = 40
    status_bar = pygame.Surface((WIDTH, status_bar_height), pygame.SRCALPHA)  # Transparent surface
    status_bar.fill(SEMI_BLACK)  # Semi-transparent black

    SCREEN.blit(status_bar, (0, HEIGHT - status_bar_height))

    font = pygame.font.Font("Font_Style.ttf", font_size)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - status_bar_height // 2))

    SCREEN.blit(text, text_rect)

    difficulty_font = pygame.font.Font("Font_Style.ttf", 19)
    difficulty_text = difficulty_font.render(f'Difficulty: {difficulty}', True, WHITE)
    difficulty_rect = difficulty_text.get_rect(right=WIDTH - 10, centery=HEIGHT - status_bar_height // 2)
    
    # Blit the difficulty text onto the status bar
    SCREEN.blit(difficulty_text, difficulty_rect)


# Example usage of the status bar in the game loop
game_over_message = ""

while True:

    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))  # Draw background image
    draw_lines()  # Draw game board lines
    draw_figures()  # Draw current board state

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            Clicked_row = event.pos[1] // SQUARE_SIZE
            Clicked_col = event.pos[0] // SQUARE_SIZE

            if available_square(Clicked_row, Clicked_col):
                mark_square(Clicked_row, Clicked_col, player)
                if check_win(player):
                    game_over = True
                player = player % 2 + 1

                if not game_over:
                    if best_move(max_depth):
                        if check_win(2):
                            game_over = True
                    player = player % 2 + 1

                if not game_over:
                    if is_board_full():
                        game_over = True

    # Translate max_depth to difficulty level string
    if max_depth == 1:
        difficulty = "Easy"
    elif max_depth == 2:
        difficulty = "Medium"
    elif max_depth == 5:
        difficulty = "Hard"
    else:
        difficulty = "Unknown"

    if not game_over:
        draw_figures()
        draw_status_bar("Game is Running...", color=SEMI_WHITE, difficulty=difficulty)
    else:
        if check_win(1):
            draw_figures([GREEN, GREEN])
            draw_lines(GREEN)
            game_over_message = "You Won!"
            draw_status_bar(game_over_message, color=GREEN, difficulty=difficulty)
        elif check_win(2):
            draw_figures([RED, RED])
            draw_lines(RED)
            game_over_message = "You Loose!"
            draw_status_bar(game_over_message, color=RED, difficulty=difficulty)
        else:
            draw_figures([GREY, GREY])
            draw_lines(GREY)
            game_over_message = "It's a Draw!"
            draw_status_bar(game_over_message, color=BLUE, difficulty=difficulty)
            
        if game_over:
         button_rect = draw_retry_button()  # Draw retry button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                button_x, button_y, button_width, button_height = button_rect
                
                # Check if Retry button is clicked
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    BOARD.fill(0)  # Reset the board
                    player = 1
                    game_over = False
                    game_over_message = ""

                    max_depth = welcome_screen() 
    
    pygame.display.update()
