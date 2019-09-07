import pygame
import sys
from pygame.locals import *
from math import floor
import random

WIDTH = 8
HEIGHT = 8

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BG = (170, 126, 50)

SQUARES = 8
SCORES_HEIGHT = SQUARES ** 2
SCR_WIDTH = SQUARES ** 3
SCR_HEIGHT = SCR_WIDTH + SCORES_HEIGHT

SIDE = round(SCR_WIDTH / SQUARES)
RADIUS = round(SQUARES / 2.0)

def draw_piece(surface, x, y, radius, color):
    pygame.transform.scale(surface, (round(x/2.0), round(y/2.0)))
    pygame.draw.circle(surface, color, (int((x+0.5)*SIDE), int((y+0.5)*SIDE)), radius*SQUARES-2, 0)

def draw_board(surface, board):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            piece = board[x][y]
            if piece in ['X', 'O']:
                draw_piece(surface=surface, x=x, y=y, radius=RADIUS, color=BLACK if piece == 'X' else WHITE)

def get_new_board():
    board = []
    for i in range(HEIGHT):
        board.append([' ' for _ in range(8)])
    return board

def is_on_board(x, y):
    return x in range(WIDTH) and y in range(HEIGHT)

def is_on_corner(x, y):
    xcorners = [0, WIDTH - 1]
    ycorners = [0, HEIGHT - 1]
    return x in xcorners and y in ycorners

def is_valid_move(board, tile, xstart, ystart):
    if board[xstart][ystart] != ' ' or not is_on_board(xstart, ystart):
        return False
    other_tile = 'O' if tile == 'X' else 'X'

    tiles_to_flip = []
    choices = [el for el in range(-1, 2)]
    for xdir, ydir in [[x,y] for x in choices for y in choices]:
        x, y = xstart, ystart
        x += xdir
        y += ydir
        while is_on_board(x, y) and board[x][y] == other_tile:
            x += xdir
            y += ydir
            if is_on_board(x, y) and board[x][y] == tile:
                while True:
                    x -= xdir
                    y -= ydir
                    if x == xstart and y == ystart:
                        break
                    tiles_to_flip.append([x, y])
    if not tiles_to_flip:
        return False
    return tiles_to_flip

def get_board_with_valid_moves(board, tile):
    board_copy = get_board_copy(board = board)

    for x, y in get_valid_moves(board=board_copy, tile=tile):
        board_copy[x][y] = '.'
    return board_copy

def get_valid_moves(board, tile):
    valid_moves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if is_valid_move(board=board, tile=tile, xstart=x, ystart=y):
                valid_moves.append([x, y])
    return valid_moves

def get_score_of_board(board):
    xscore = oscore = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                xscore += 1
            elif board[x][y] == 'O':
                oscore += 1
    return {'X': xscore, 'O': oscore}

def who_goes_first():
    return 'computer' if random.randint(0, 1) == 0 else 'player'

def make_move(board, tile, xstart, ystart):
    tiles_to_flip = is_valid_move(board=board, tile=tile, xstart=xstart, ystart=ystart)
    if not tiles_to_flip:
        return False
    board[xstart][ystart] = tile
    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True

def get_board_copy(board):
    board_copy = get_new_board()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board_copy[x][y] = board[x][y]
    return board_copy

def get_player_move():
    mouse_up_detected = False
    x, y = -1, -1
    while not mouse_up_detected:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x, y = floor(pos[0]/SIDE), floor(pos[1]/SIDE)
                mouse_up_detected = True

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    return [x, y]

def get_computer_move(board, computer_tile):
    poss_moves = get_valid_moves(board=board, tile=computer_tile)
    random.shuffle(poss_moves)
    for x, y in poss_moves:
        if is_on_corner(x, y):
            return [x, y]

    best_score = -1
    best_move = []
    for x, y in poss_moves:
        board_copy = get_board_copy(board)
        make_move(board=board_copy, tile=computer_tile, xstart=x, ystart=y)
        score = get_score_of_board(board_copy)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move

def print_score(board, player_tile, computer_tile):
    scores = get_score_of_board(board)
    print('\nYour score: %s points. Computer: %s points.' % (scores[player_tile], scores[computer_tile]))

def play_game(surface, player_tile, computer_tile):
    turn = who_goes_first()

    board = get_new_board()
    board[3][3] = board[4][4] = 'X'
    board[4][3] = board[3][4] = 'O'
    draw_board(surface=surface, board=board)
    pygame.display.update()

    no_winner = True
    while no_winner:
        player_valid_moves = get_valid_moves(board=board, tile=player_tile)
        computer_valid_moves = get_valid_moves(board=board, tile=computer_tile)

        if len(player_valid_moves) == 0 and len(computer_valid_moves) == 0:
            return board  # end the game, no one can move
        elif turn == 'player':
            if len(player_valid_moves) > 0:
                draw_board(surface=surface, board=board)
                move = get_player_move()
                while not is_valid_move(board=board, tile=player_tile, xstart=move[0], ystart=move[1]):
                    print('player move invalid -- try again...')
                    move = get_player_move()
                make_move(board=board, tile=player_tile, xstart=move[0], ystart=move[1])
                pygame.display.update()
                turn = 'computer'
        elif turn == 'computer':
            if len(computer_valid_moves) > 0:
                draw_board(surface=surface, board=board)
                move = get_computer_move(board=board, computer_tile=computer_tile)
                make_move(board=board, tile=computer_tile, xstart=move[0], ystart=move[1])
            turn = 'player'

        draw_board(surface=surface, board=board)
        scores = get_score_of_board(board)
        draw_score(surface=surface, text='Player: {}'.format(scores[player_tile]),x=0, y=SCR_WIDTH)
        draw_score(surface=surface, text='Computer: {}'.format(scores[computer_tile]), x=SCR_WIDTH-250, y=SCR_WIDTH)
        if scores['X'] + scores['O'] == 64:
            no_winner = False
            print('Player wins!') if scores['X'] > scores['O'] else print('Computer wins!')
            answer = input('Press ENTER to exit')
            sys.exit()

        pygame.display.update()


def draw_score(surface, text, x, y):
    font = pygame.font.Font(None, 48)
    text_render = font.render(text, True, WHITE, BLUE)

    text_rect = text_render.get_rect()
    text_rect.centerx = x + 100
    text_rect.centery = y + 30
    surface.blit(text_render, text_rect)


def play():
    pygame.init()

    surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), 0, 32)
    pygame.display.set_caption('Othello')
    board = get_new_board()

    surface.fill(BG)
    for x in range(SQUARES):
        for y in range(SQUARES):
            draw_square(surface=surface, x=x*SIDE, y=y*SIDE, s=SIDE, bg_color=BLACK)

    scores = get_score_of_board(board)
    draw_score(surface=surface, text='Player: {}'.format(scores['X']), x=0, y=SCR_WIDTH)
    draw_score(surface=surface, text='Computer: {}'.format(scores['O']), x=SCR_WIDTH - 250, y=SCR_WIDTH)
    pygame.display.update()

    player_tile, computer_tile = ['X', 'O']

    pygame.display.update()
    play_game(surface=surface, player_tile=player_tile, computer_tile=computer_tile)


def draw_square(surface, x, y, s, bg_color, thick=4):
    pygame.draw.line(surface, bg_color, (x, y), (x+s, y), thick)
    pygame.draw.line(surface, bg_color, (x+s, y), (x+s, y+s), thick)
    pygame.draw.line(surface, bg_color, (x+s, y+s), (x, y+s), thick)
    pygame.draw.line(surface, bg_color, (x, y+s), (x, y), thick)


play()
