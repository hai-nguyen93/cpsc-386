import pygame
import random


class Ball:
    def __init__(self, x, y, velocity, image):
        self.x = x
        self.y = y
        self.velocity = pygame.math.Vector2()  # convert a velocity tuple to vector2
        self.velocity.x = velocity[0]
        self.velocity.y = velocity[1]
        self.image = image
        self.image_rect = image.get_rect()

    def update(self):
        self.x += self.velocity.x
        self.y += self.velocity.y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


class Paddle:
    def __init__(self, x, y, image, vertical=True):
        self.x = x
        self.y = y
        self.image = image
        self.vertical = vertical
        self.image_rect = image.get_rect()


class Score:
    def __init__(self):
        self.point = 0
        self.game_point = 0

    def reset(self):
        self.point, self.game_point = 0, 0
