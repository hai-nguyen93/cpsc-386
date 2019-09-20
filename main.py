import sys
import pygame
from pygame.locals import *
from settings import Settings
from ship import Ship
import game_functions as gf

BLACK = (0, 0, 0)
FPS = 60

def play():
    pygame.init()
    game_settings = Settings()
    surface = pygame.display.set_mode((game_settings.scr_width, game_settings.scr_height))
    pygame.display.set_caption('Alien Invasion')
    main_clock = pygame.time.Clock()

    # Make a ship
    ship = Ship(game_settings=game_settings, screen=surface)

    # Main game loop
    while True:
        gf.check_events(ship)
        ship.update()
        gf.update_screen(game_settings, screen=surface, ship=ship)

        main_clock.tick(FPS)


play()
