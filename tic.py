import pygame
import numpy as np
import sys
import math

BLACK = (0, 0, 0)
RED = (200, 20, 20)
BLUE = (20, 20, 200)
WHITE = (255, 255, 255)
LINE_COLOR = (200, 200, 200)

ROW_COUNT = 3
COLUMN_COUNT = 3
WIN_NO = 3
EMPTY = 0

PLAYER1 = 0
PLAYER2 = 1

PLAYER1_PIECE = 1
PLAYER2_PIECE = 2

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def make_move(board, row, col, symbol):
    board[row][col] = symbol
    
def is_valid_move(board, row, col):
    return board[row][col] == 0

def winning_move(board, piece):
    # check for horizontal wins
    for c in range(COLUMN_COUNT+1-WIN_NO):
        for r in range(ROW_COUNT):
            ctr = False
            for i in range(WIN_NO):
                if board[r][c + i] == piece:
                    ctr = True
                else:
                    ctr = False
                    break
            if ctr == True:
                break
        if ctr == True:
            break
    if ctr == True:
        return True
    
    # check for vertical wins
    for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT+1-WIN_NO):
                ctr = False
                for i in range(WIN_NO):
                    if board[r + i][c] == piece:
                        ctr = True
                    else:
                        ctr = False
                        break
                if ctr == True:
                    break
            if ctr == True:
                break
    if ctr == True:
            return True
        
    # check for positive slope diagonal wins
    for c in range(COLUMN_COUNT+1-WIN_NO):
            for r in range(ROW_COUNT+1-WIN_NO):
                ctr = False
                for i in range(WIN_NO):
                    if board[r + i][c + i] == piece:
                        ctr = True
                    else:
                        ctr = False
                        break
                if ctr == True:
                    break
            if ctr == True:
                break
    if ctr == True:
            return True
        
    # check for negative slope diagonal wins
    for c in range(COLUMN_COUNT+1-WIN_NO):
            for r in range(WIN_NO - 1, ROW_COUNT):
                ctr = False
                for i in range(WIN_NO):
                    if board[r - i][c + i] == piece:
                        ctr = True
                    else:
                        ctr = False
                        break
                if ctr == True:
                    break
            if ctr == True:
                break
    if ctr == True:
            return True

def draw_board(board):
    #draw column lines
    i = 1
    col_section = width / COLUMN_COUNT
    while i < COLUMN_COUNT:
        pygame.draw.line(screen, LINE_COLOR, (col_section, 0), (col_section, height))
        col_section = col_section + (width / COLUMN_COUNT)
        i += 1
        
    #draw row lines
    i = 1
    row_section = height / ROW_COUNT
    while i < ROW_COUNT:
        pygame.draw.line(screen, LINE_COLOR, (0, row_section), (width, row_section))
        row_section = row_section + (height / ROW_COUNT)
        i += 1
        
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):  
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, BLUE, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def get_valid_locations_col(board, col):
    valid_locations_col = []
    for col in range(COLUMN_COUNT):
        if is_valid_move(board, row, col):
            valid_locations_col.append(col)
    return valid_locations_col

def get_valid_locations_row(board, row):
    valid_locations_row = []
    for row in range(ROW_COUNT):
        if is_valid_move(board, row, col):
            valid_locations_row.append(row)
    return valid_locations_row

board = create_board()
print(board)
game_over = False
turn = 0

pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
screen.fill(BLACK)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("monospace", 20)
text1 = font.render('PLAYER 1 WINS YIPPEE!!!', True, WHITE)
text2 = font.render('PLAYER 2 WINS YIPPEE!!!', True, WHITE)

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            if turn == PLAYER1:
                
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(math.floor(posx/SQUARESIZE))
                row = int(math.floor(posy/SQUARESIZE))
                
                if is_valid_move(board, row, col):
                    make_move(board, row, col, 1)
                    turn += 1
                    
                    if winning_move(board, 1):
                        print("PLAYER 1 WINS YIPPEE!!!")
                        screen.blit(text1, text1.get_rect(center = screen.get_rect().center))
                        pygame.display.flip()
                        game_over = True
                
            else:
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(math.floor(posx/SQUARESIZE))
                row = int(math.floor(posy/SQUARESIZE))
                
                if is_valid_move(board, row, col):
                    make_move(board, row, col, 2)
                    turn -=1
                    
                    if winning_move(board, 2):
                        print("PLAYER 2 WINS YIPPEE!!!")
                        screen.blit(text2, text2.get_rect(center = screen.get_rect().center))
                        pygame.display.flip()
                        game_over = True
            
            '''if game_over == False and all(piece == PLAYER1_PIECE or piece == PLAYER2_PIECE for piece in itertools.chain.from_iterable(board)):
                print("It's a draw")
                game_over = True'''
        
            if len(get_valid_locations_row(board, row)) == 0 and len(get_valid_locations_col(board, col)) == 0:
                print("It's a draw")
                game_over = True
        
            print(board)
            draw_board(board)
            
            if game_over:
                pygame.time.wait(2000)