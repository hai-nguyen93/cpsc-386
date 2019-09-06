import pygame
import sys
import time
from pygame.locals import *


class Box:
    def __init__(self, x, y, width, height, color, velocity):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = velocity


# Set up pygame.
pygame.init()

# Set up the window.
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
ws = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Animation')

# Setup the colors.
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the boxes
# b1 = {'rect': pygame.Rect(300, 80, 50, 100), 'color': RED, 'velocity': pygame.math.Vector2(4, -4)}
b2 = {'rect': pygame.Rect(200, 200, 20, 20), 'color': GREEN, 'velocity': pygame.math.Vector2(-4, 4)}
b3 = {'rect': pygame.Rect(100, 150, 60, 60), 'color': BLUE, 'velocity': pygame.math.Vector2(-4, 4)}
b4 = Box(10, 10, 30, 30, RED, pygame.math.Vector2(4, -4))
boxes = [b2, b3]

# Game loop
while True:
    # Check for QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw the white b[
    ws.fill(WHITE)

    for b in boxes:
        # Move the boxes
        r = b['rect']
        v = b['velocity']
        r.left += v.x
        r.top += v.y

        # Check if the box has moved out of window
        if r.top < 0 or r.bottom > WINDOWHEIGHT:
            v.y *= -1
        if r.left < 0 or r.right > WINDOWWIDTH:
            v.x *= -1

        # Draw the box
        pygame.draw.rect(ws, b['color'], r)

    b4.x += b4.velocity.x
    b4.y += b4.velocity.y
    if b4.y < 0 or b4.y + b4.height > WINDOWHEIGHT:
        b4.velocity.y *= -1
    if b4.x < 0 or b4.x + b4.width > WINDOWWIDTH:
        b4.velocity.x *= -1
    pygame.draw.rect(ws, b4.color, pygame.Rect(b4.x, b4.y, b4.width, b4.height))

    # Draw the window
    pygame.display.update()
    time.sleep(0.5)
