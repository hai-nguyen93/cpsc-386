import sys
import pygame
from pygame.locals import *


RIGHT_KEYS = [K_d, K_RIGHT]
LEFT_KEYS = [K_a, K_LEFT]


def terminate():
    pygame.quit()
    sys.exit()


def check_events(ship):
    """Respong to keypresses and mouse events."""
    for e in pygame.event.get():
        if e.type == QUIT:
            terminate()
        if e.type == KEYDOWN:
            check_keydown_events(e, ship)
        if e.type == KEYUP:
            check_keyup_events(e, ship)


def check_keydown_events(event, ship):
    """Respond to key presses"""
    if event.key in RIGHT_KEYS:
        ship.move_right = True
    if event.key in LEFT_KEYS:
        ship.move_left = True


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == K_ESCAPE:
        terminate()
    if event.key in RIGHT_KEYS:
        ship.move_right = False
    if event.key in LEFT_KEYS:
        ship.move_left = False


def update_screen(game_settings, screen, ship):
    """Redraw the screen"""
    screen.fill(game_settings.bg_color)
    ship.draw()

    pygame.display.update()