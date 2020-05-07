import pygame
import numpy as np
import random
import math
from copy import deepcopy
import time

ROW_SIZE = 6
COL_SIZE = 7

EMPTY = 0
HUMAN_PLAYER = 1
AI_PLAYER = 2

def init_board():
    board = np.zeros((ROW_SIZE, COL_SIZE))
    return board

def available_actions(board):
    actions = []
    for col in range(COL_SIZE):
        if board[ROW_SIZE-1][col] == EMPTY:
            actions.append(col)
    return actions

def gameover(board):
    # Check for win vertically
        for row in range(ROW_SIZE-3):
            for col in range(COL_SIZE):
                if board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col] != EMPTY:
                    return board[row][col]

        # Check for win horizontally
        for row in range(ROW_SIZE):
            for col in range(COL_SIZE-3):
                if board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3] != EMPTY:
                    return board[row][col]

        # Check for win diagonally
        for row in range(ROW_SIZE-3):
            for col in range (COL_SIZE-3):
                if board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3] != EMPTY:
                    return board[row][col]

        for row in range(3, ROW_SIZE):
            for col in range (COL_SIZE-3):
                if board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3] != EMPTY:
                    return board[row][col]
        return None

def highest_valid_row(board, col):
    for i in range(ROW_SIZE):
        if np.all(board[i][col] == EMPTY):
            return i

def make_move(board, col, player):
    row = highest_valid_row(board, col)
    theBoard = deepcopy(board)
    if player == HUMAN_PLAYER:
        theBoard[row][col] = 1
    else:
        theBoard[row][col] = 2
    return theBoard

def evaluate(four_piece, player):
    score = 0
    if player == HUMAN_PLAYER:
        opposition = AI_PLAYER
    else:
        opposition = HUMAN_PLAYER

    player_count = four_piece.count(player)
    opposition_count = four_piece.count(opposition)
    empty_count = four_piece.count(EMPTY)
    if player_count == 4:
        score += 100
    elif player_count == 3:
        score += 3
        if empty_count == 1: score += 2
        elif opposition_count == 1: score -= 2
    elif player_count == 2:
        score += 1
        if empty_count == 2: score += 1
        if opposition_count == 2: score -= 1
    if opposition_count == 3:
        score -= 3
        if empty_count == 1: score -= 2
        elif player_count == 1 : score += 1
    return score

def score_position(board, player):
    score = 0

    # Making sure the center column has more weight than the other columns
    center_column = [int(i) for i in list(board[:, COL_SIZE//2])]
    center_count = center_column.count(player)
    score += center_count * 3

    # Weighing the Horizontal pieces
    for row in range(ROW_SIZE):
        the_row = [int(i) for i in list(board[row,:])]
        for col in range(COL_SIZE-3):
            four_piece = the_row[col:col+4]
            score += evaluate(four_piece, player)

    # Weighing the Vertical pieces
    for col in range(COL_SIZE):
        the_col = [int(i) for i in list(board[:,col])]
        for row in range(ROW_SIZE-3):
            four_piece = the_col[row:row+4]
            score += evaluate(four_piece, player)

    # Weighin the Diagonal pieces
    for row in range(ROW_SIZE-3):
        for col in range(COL_SIZE-3):
            four_piece = [board[row+i][col+i] for i in range(4)]
            score += evaluate(four_piece, player)
    for row in range(3, ROW_SIZE):
        for col in range(COL_SIZE-3):
            four_piece = [board[row-i][col+i] for i in range(4)]
            score += evaluate(four_piece, player)
    return score



def minimax (board, depth, alpha, beta, maximizingPlayer):
    finished = gameover(board)

    if not finished is None: #If someone won
        if finished == AI_PLAYER:
            return (None, 100000000000000)
        else:
            return (None, -100000000000000)
    if depth == 0: # If the depth for depth limit minimax reaches 0
        return (None, score_position(board, AI_PLAYER))
    actions = available_actions(board)
    if len(actions) == 0: # If the board is completely full and it is a tie        
        return (None, 0)

    if maximizingPlayer:
        maxEvaluation = -math.inf
        bestAction = random.choice(actions)
        for a in actions:
            board_copy = make_move(board, a, AI_PLAYER)
            evaluation = minimax(board_copy, depth-1, alpha, beta, False)[1]
            if evaluation > maxEvaluation:
                maxEvaluation = evaluation
                bestAction = a
            alpha = max (alpha, evaluation)
            if beta <= alpha:
                break
        return (bestAction, maxEvaluation)
    else:
        minEvaluation = math.inf
        bestAction = random.choice(actions)
        for a in actions:
            board_copy = make_move(board, a, HUMAN_PLAYER)
            evaluation = minimax(board_copy, depth-1, alpha, beta, True)[1]
            if evaluation < minEvaluation:
                minEvaluation = evaluation
                bestAction = a
            beta = min (beta, evaluation)
            if beta <= alpha:
                break
        return (bestAction, minEvaluation)

RED_PLAYER = (255, 0, 0)
YELLOW_PLAYER = (0, 153, 0)
BACKGROUND_COLOR = (255, 255, 255)
BOARD_COLOR = (0, 0, 255)
SQUARE_SIZE = 100
WIDTH = COL_SIZE*SQUARE_SIZE
HEIGHT = ROW_SIZE*SQUARE_SIZE + SQUARE_SIZE
RADIUS = 45
pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 60)
win = pygame.display.set_mode((COL_SIZE*SQUARE_SIZE, ROW_SIZE*SQUARE_SIZE + SQUARE_SIZE))
win.fill(BACKGROUND_COLOR)
pygame.display.update()

def draw_board(board):
    pygame.draw.rect(win, BOARD_COLOR, (0, 100, WIDTH, ROW_SIZE*SQUARE_SIZE + SQUARE_SIZE))
    row_height = 500
    for row in range (ROW_SIZE):
        for col in range (COL_SIZE):
            if board[row][col] == HUMAN_PLAYER:
                pygame.draw.circle(win, RED_PLAYER, (col*SQUARE_SIZE + 50, row*SQUARE_SIZE + 150 + row_height), RADIUS)
            elif board[row][col] == AI_PLAYER:
                pygame.draw.circle(win, YELLOW_PLAYER, (col*SQUARE_SIZE + 50, row*SQUARE_SIZE + 150 + row_height), RADIUS)
            else:
                pygame.draw.circle(win, BACKGROUND_COLOR, (col*SQUARE_SIZE + 50, row*SQUARE_SIZE + 150 + row_height), RADIUS)
        row_height -= 200
    pygame.display.update()

def play():
    #Initialize the board and pygame
    board = init_board()
    turn = AI_PLAYER
    print (board)

    while True:
        # Check for winner
        draw_board(board)
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(win, BACKGROUND_COLOR, (0,0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == HUMAN_PLAYER:
                    pygame.draw.circle(win, RED_PLAYER, (posx, int(SQUARE_SIZE/2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(win, BACKGROUND_COLOR, (0,0, WIDTH, SQUARE_SIZE))
                if turn == HUMAN_PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARE_SIZE))
                    board = make_move(board, col, turn)
                    turn = AI_PLAYER

                    if gameover(board) == HUMAN_PLAYER:
                        text = myfont.render('PLAYER 1 WINS!', True, RED_PLAYER)
                        win.blit(text, (70,10))
                        game_over = True
                        break
                    draw_board(board)
                    print (board[::-1])

        if game_over:
            break
        if turn == AI_PLAYER:
            col, score = minimax(board, 5, -math.inf, math.inf, True)
            board = make_move(board, col, turn)
            turn = HUMAN_PLAYER

            if gameover(board) == AI_PLAYER:
                text = myfont.render('PLAYER 2 WINS!', True, YELLOW_PLAYER)
                win.blit(text, (70,10))
                break
            draw_board(board)
            print (board[::-1])

    draw_board(board)
    print (board[::-1])
    pygame.time.wait(3000)
play()