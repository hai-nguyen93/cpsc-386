import pygame
import sys
from pygame.locals import *
import random
import objects
import time

SCR_WIDTH = 800
SCR_HEIGHT = 600
SCORES_HEIGHT = SCR_HEIGHT / 6

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def draw_score(surface, text, x, y):
    font = pygame.font.Font(None, 30)
    text_render = font.render(text, True, WHITE, BLACK)
    text_rect = text_render.get_rect()
    text_rect.left = x + 20
    text_rect.top = y + 20
    surface.blit(text_render, text_rect)


def play_game(surface, player, player_paddles, computer, computer_paddles):
    no_winner = True
    while no_winner:
        if player.game_point == 3 or computer.game_point == 3:
            no_winner = False
            draw_score(surface, 'Play again? (Press Y or N)', SCR_WIDTH/2 - 136, SCR_HEIGHT/2 - 40)
            pygame.display.update()
            play_again = False
            while not play_again:
                for event in pygame.event.get():
                    if event.type == KEYUP:
                        if event.key == K_y:
                            player.reset()
                            computer.reset()
                            no_winner = True
                            play_again = True
                            break
                        elif event.key == K_n:
                            pygame.quit()
                            sys.exit()

        if player.point >= 11:
            player.game_point += 1
            player.point, computer.point = 0, 0
        if computer.point >= 11:
            computer.game_point += 1
            player.point, computer.point = 0, 0

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_UP:
                    player.point += 1

        surface.fill(BLACK)
        pygame.draw.line(surface, WHITE, (0, SCR_HEIGHT - SCORES_HEIGHT), (SCR_WIDTH, SCR_HEIGHT - SCORES_HEIGHT))
        pygame.draw.line(surface, WHITE, (SCR_WIDTH / 2, 0), (SCR_WIDTH / 2, SCR_HEIGHT - SCORES_HEIGHT))

        draw_score(surface, 'Player: {}'.format(player.point), x=SCR_WIDTH/2, y=SCR_HEIGHT-SCORES_HEIGHT)
        draw_score(surface, 'Game point: {}'.format(player.game_point), x=SCR_WIDTH/2, y=SCR_HEIGHT-SCORES_HEIGHT+40)
        draw_score(surface, 'Computer: {}'.format(computer.point), x=0, y=SCR_HEIGHT-SCORES_HEIGHT)
        draw_score(surface, 'Game point: {}'.format(computer.game_point), x=0, y=SCR_HEIGHT-SCORES_HEIGHT+40)

        pygame.display.update()
        time.sleep(0.017)


def play():
    pygame.init()
    surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), 0, 32)
    pygame.display.set_caption('Pong')

    player = objects.Score()
    computer = objects.Score()
    player_paddles = []
    computer_paddles = []

    surface.fill(BLACK)
    pygame.draw.line(surface, WHITE, (0, SCR_HEIGHT-SCORES_HEIGHT), (SCR_WIDTH, SCR_HEIGHT-SCORES_HEIGHT))
    pygame.draw.line(surface, WHITE, (SCR_WIDTH/2, 0), (SCR_WIDTH/2, SCR_HEIGHT-SCORES_HEIGHT))

    pygame.display.update()
    play_game(surface=surface, player=player, player_paddles=player_paddles,
              computer=computer, computer_paddles=computer_paddles)


play()
