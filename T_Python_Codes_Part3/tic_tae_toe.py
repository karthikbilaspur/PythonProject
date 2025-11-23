import pygame
import sys
from pygame.locals import *
import numpy as np
import random

# Constants
width = 800
height = 800
board_rows = 3
board_columns = 3
cross_width = 25
square_size = width//board_columns
line_Width = 15
red = (255, 0, 0)
bg_color = (28, 170, 156)
line_color = (23, 145, 135)
circle_color = (239, 231, 200)
cross_color = (66, 66, 66)
space = square_size//4
circle_radius = square_size//3
circle_width = 14

pygame.init()
screen = pygame.display.set_mode((height, width))
pygame.display.set_caption('Tic Tac Toe!')
screen.fill(bg_color)

font = pygame.font.Font('freesansbold.ttf', 25)
text = font.render('Press R to restart', True, (0, 255, 0), (0, 0, 128))
Won = font.render(" Won", True, (0, 0, 128), (0, 255, 0))
leave = font.render("Press X to Exit", True, (255, 255, 255), red)
leaveRect = text.get_rect()
textRect = text.get_rect()
winRect = Won.get_rect()
winRect.center = (100, 30)
textRect.center = (width-400, 30)
leaveRect.center = (width-120, 30)

board = np.zeros((board_rows, board_columns))

def draw_figures():
    for row in range(board_rows):
        for col in range(board_columns):
            if board[row][col] == 1:
                pygame.draw.circle(screen, circle_color, (int(col*square_size + square_size//2), int(row*square_size + square_size//2)), circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, cross_color, (col*square_size + space, row*square_size + square_size - space), (col*square_size+square_size - space, row*square_size + space), cross_width)
                pygame.draw.line(screen, cross_color, (col*square_size + space, row*square_size + space), (col*square_size + square_size - space, row*square_size + square_size - space), cross_width)

def draw_lines():
    pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_Width)
    pygame.draw.line(screen, line_color, (0, 2*square_size), (width, 2*square_size), line_Width)
    pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_Width)
    pygame.draw.line(screen, line_color, (2*square_size, 0), (2*square_size, height), line_Width)

def mark_square(row: int, col: int, player: int):
    board[row][col] = player

def available_square(row: int, col: int):
    return board[row][col] == 0

def is_board_full():
    for row in range(board_rows):
        for col in range(board_columns):
            if board[row][col] == 0:
                return False
    return True

def check_win(player: int):
    for col in range(board_columns):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_winning_line(col, player)
            return True
    for row in range(board_rows):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_winning_line(row, player)
            return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal(player)
        return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_des_diagonal(player)
        return True

def draw_horizontal_winning_line(row: int, player: int):
    posY = row*square_size + square_size//2
    if (player == 1):
        color = circle_color
    else:
        color = cross_color
    pygame.draw.line(screen, color, (15, posY), (width-15, posY), 15)

def draw_vertical_winning_line(col: int, player: int):
    posX = col*square_size + square_size//2
    if (player == 1):
        color = circle_color
    else:
        color = cross_color
    pygame.draw.line(screen, color, (posX, 15), (posX, width-15), 15)

def draw_asc_diagonal(player: int):
    if (player == 1):
        color = circle_color
    else:
        color = cross_color
    pygame.draw.line(screen, color, (15, height-15), (width-15, 15), 15)

def draw_des_diagonal(player: int):
    if (player == 1):
        color = circle_color
    else:
        color = cross_color
    pygame.draw.line(screen, color, (15, 15), (width-15, height-15), 15)

def compMove():
    possibleMove = []
    for row in range(board_rows):
        for col in range(board_columns):
            if board[row][col] == 0:
                possibleMove.append((row, col))

    move = (0, 0)
    for let in [2, 1]:
        for i in possibleMove:
            boardCopy = board.copy()
            boardCopy[i[0]][i[1]] = let
            if check_win(let):
                move = i
                return move

    if (0, 0) in possibleMove:
        move = (0, 0)
        return move
    if (0, 2) in possibleMove:
        move = (0, 2)
        return move
    if (2, 0) in possibleMove:
        move = (2, 0)
        return move
    if (2, 2) in possibleMove:
        move = (2, 2)
        return move
    if (1, 1) in possibleMove:
        move = (1, 1)
        return move

    move = random.choice(possibleMove)
    return move

def restart():
    screen.fill(bg_color)
    draw_lines()
    for row in range(board_rows):
        for col in range(board_columns):
            board[row][col] = 0

draw_lines()
player = 1
game_over = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player == 1:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = int(mouseY // square_size)
            clicked_column = int(mouseX // square_size)
            if available_square(clicked_row, clicked_column):
                mark_square(clicked_row, clicked_column, player)
                if (check_win(player)):
                    game_over = True
                    Won = font.render("Player"+str(player) + " Won ", True, (0, 0, 128), (0, 255, 0))
                    screen.blit(Won, winRect)
                    screen.blit(text, textRect)
                    screen.blit(leave, leaveRect)
                player = 2
                draw_figures()
        if player == 2 and not game_over:
            move = compMove()
            mark_square(move[0], move[1], player)
            if (check_win(player)):
                game_over = True
                Won = font.render("Player"+str(player) + " Won ", True, (0, 0, 128), (0, 255, 0))
                screen.blit(Won, winRect)
                screen.blit(text, textRect)
                screen.blit(leave, leaveRect)
            player = 1
            draw_figures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False
                player = 1
            elif event.key == pygame.K_x:
                pygame.quit()
                sys.exit()
    pygame.display.update()