import pygame
import numpy as np
import random
import math
import sys
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
            return (None, (depth+1)*100000000000)
        else:
            return (None, (depth+1)*-100000000000)
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

# Colors
RED_PLAYER = (255, 0, 0)
YELLOW_PLAYER = (0, 153, 0)
BACKGROUND_COLOR = (255, 255, 255)
BOARD_COLOR = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SQUARE_SIZE = 100
WIDTH = COL_SIZE*SQUARE_SIZE
HEIGHT = ROW_SIZE*SQUARE_SIZE + SQUARE_SIZE
RADIUS = 45
pygame.init()
pygame.font.init()

# Fonts
myfont = pygame.font.SysFont('OpenSans-Regular.ttf', 60)

win = pygame.display.set_mode((WIDTH, HEIGHT))
win.fill(BACKGROUND_COLOR)
pygame.display.update()

def draw_board(board):
    pygame.draw.rect(win, BOARD_COLOR, (0, 100, WIDTH,HEIGHT))
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

def choose_player():
    title = myfont.render("Play Connect 4", True, BLACK)
    titleRect = title.get_rect()
    titleRect.center = ((WIDTH / 2), 150)
    win.blit(title, titleRect)
    name = myfont.render("Made by Kush Bhagat", True, BLACK)
    nameRect = name.get_rect()
    nameRect.center = ((WIDTH/2), 225)
    win.blit(name, nameRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        playXButton = pygame.Rect(WIDTH/2 - 200, 300, 400, 50)
        playX = myfont.render("FIRST PLAYER", True, WHITE)
        playXRect = playX.get_rect()
        playXRect.center = playXButton.center
        pygame.draw.rect(win, BLACK, playXButton)
        win.blit(playX, playXRect)

        playOButton = pygame.Rect(WIDTH/2 - 200, 400, 400, 50)
        playO = myfont.render("SECOND PLAYER", True, WHITE)
        playORect = playO.get_rect()
        playORect.center = playOButton.center
        pygame.draw.rect(win, BLACK, playOButton)
        win.blit(playO, playORect)
        pygame.display.update()
        

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playXButton.collidepoint(mouse):
                time.sleep(0.2)
                return HUMAN_PLAYER
            elif playOButton.collidepoint(mouse):
                time.sleep(0.2)
                return AI_PLAYER


def play(first_player):
    #Initialize the board and pygame
    board = init_board()
    turn = first_player
    print (board)

    while True:
        # Check for winner
        draw_board(board)
        game_over = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

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
                        win.blit(text, (20,SQUARE_SIZE/2-20))
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
                win.blit(text, (20,SQUARE_SIZE/2-20))
                break
            draw_board(board)
            print (board[::-1])

    draw_board(board)
    print (board[::-1])

while True:
    win.fill(WHITE)
    first_player = choose_player()
    win.fill(WHITE)
    play(first_player)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        playAgain = pygame.Rect(WIDTH/2 + 25, SQUARE_SIZE/2-25, 300, 50)
        playAgainText = myfont.render("PLAY AGAIN?", True, WHITE)
        playAgainRect = playAgainText.get_rect()
        playAgainRect.center = playAgain.center
        pygame.draw.rect(win, BLACK, playAgain)
        win.blit(playAgainText, playAgainRect)
        pygame.display.update()

        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if playAgain.collidepoint(mouse):
                break

