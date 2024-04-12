import pygame
import numpy as np
import sys
import math
import itertools

BLACK = (0, 0, 0)
RED = (200, 20, 20)
BLUE = (20, 20, 200)
WHITE = (255, 255, 255)
LINE_COLOR = (200, 200, 200)

ROW_COUNT = 3
COLUMN_COUNT = 3
WIN_NO = 3
EMPTY = 0

PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def make_move(board, row, col, piece):
    board[row][col] = piece
    
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

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE
        
    if window.count(piece) == WIN_NO:
        score += 100
    elif window.count(piece) == WIN_NO - 1 and window.count(EMPTY) == 1:
        score += 10
    elif window.count(piece) == WIN_NO - 2 and window.count(EMPTY) == 2:
        score += 5
        
    if window.count(opp_piece) == WIN_NO - 1 and window.count(EMPTY) ==1:
        score -= 50
    return score

def score_position(board, piece):
    score = 0
    
    # score horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - (WIN_NO - 1)):
            window = row_array[c:c + WIN_NO]
            score += evaluate_window(window, piece)
                
    # score vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - (WIN_NO - 1)):
            window = col_array[r:r + WIN_NO]
            score += evaluate_window(window, piece)
    
    # score pos diagonal            
    for r in range(ROW_COUNT - (WIN_NO - 1)):
        for c in range(COLUMN_COUNT - (WIN_NO - 1)):
            window = [board[r + i][c + i] for i in range(WIN_NO)]
            score += evaluate_window(window, piece)
    
    # score neg diagonal
    for r in range(ROW_COUNT - (WIN_NO - 1)):
        for c in range(COLUMN_COUNT - (WIN_NO - 1)):
            window = [board[r + (WIN_NO - 1) - i][c + i] for i in range(WIN_NO)]
            score += evaluate_window(window, piece)
            
    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or (len(get_valid_locations_row(board, row)) == 0 and len(get_valid_locations_col(board, col)) == 0)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 10000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000)
            else: #game is over, no more valid moves
                return (None, 0)
        else: #depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if board[row][col] == 0:
                    b_copy = board.copy()
                    make_move(b_copy, row, col, AI_PIECE)
                    new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
                    if new_score > value:
                        value = new_score
                        bestMove = (row, col)
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
        return bestMove, value
        
    else: #minimizing player
        value = math.inf
        for col in range(COLUMN_COUNT):
            for row in range(ROW_COUNT):
                if board[row][col] == 0:
                    b_copy = board.copy()
                    make_move(b_copy, row, col, PLAYER_PIECE)
                    new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
                    if new_score < value:
                        value = new_score
                        bestMove = (row, col)
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
        return bestMove, value

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
            
            if turn == PLAYER:
                
                posx = event.pos[0]
                posy = event.pos[1]
                col = int(math.floor(posx/SQUARESIZE))
                row = int(math.floor(posy/SQUARESIZE))
                
                if is_valid_move(board, row, col):
                    make_move(board, row, col, PLAYER_PIECE)
                    turn += 1
                    
                    if winning_move(board, PLAYER_PIECE) or (game_over == False and all(piece == PLAYER_PIECE or piece == AI_PIECE for piece in itertools.chain.from_iterable(board))):
                        if winning_move(board, PLAYER_PIECE):
                            print("PLAYER 1 WINS YIPPEE!!!")
                            screen.blit(text1, text1.get_rect(center = screen.get_rect().center))
                            pygame.display.flip()
                            game_over = True
                        else:
                            print("It's a draw")
                            game_over = True

                    print(board)
                    draw_board(board)
                    
    if turn == AI and not game_over:
        
        bestMove, minimax_score = minimax(board, 4, -math.inf, math.inf, True)
        (row, col) = bestMove

        if is_valid_move(board, row, col):
            make_move(board, row, col, AI_PIECE)
            turn -=1
            
            if winning_move(board, AI_PIECE) or (game_over == False and all(piece == PLAYER_PIECE or piece == AI_PIECE for piece in itertools.chain.from_iterable(board))):
                if winning_move(board, AI_PIECE):
                    print("PLAYER 2 WINS YIPPEE!!!")
                    screen.blit(text2, text2.get_rect(center = screen.get_rect().center))
                    pygame.display.flip()
                    game_over = True
                else:
                    print("It's a draw")
                    game_over = True

            print(board)
            draw_board(board)
            
    '''if game_over == False and all(piece == PLAYER_PIECE or piece == AI_PIECE for piece in itertools.chain.from_iterable(board)):
        print("It's a draw")
        game_over = True'''

    if game_over:
        pygame.time.wait(2000)