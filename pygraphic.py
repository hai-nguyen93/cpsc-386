import pygame
import sys
from pygame.locals import *

# Setup pygame
pygame.init()

# Setup the window
ws = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Hello World!')

# Setup the color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Setup the font
basicFont = pygame.font.SysFont(None, 48)

# Setup the text
text = basicFont.render('Hello World!', True, WHITE, BLUE)
textRect = text.get_rect()
textRect.centerx = ws.get_rect().centerx
textRect.centery = ws.get_rect().centery

# Draw the background
ws.fill(WHITE)

# Draw a green polygon
pygame.draw.polygon(ws, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))

# Draw some blue lines
pygame.draw.line(ws, BLUE, (60, 60), (120, 60), 4)
pygame.draw.line(ws, BLUE, (120, 60), (60, 120))
pygame.draw.line(ws, BLUE, (60, 120), (120, 120), 4)

# Draw a blue circle
pygame.draw.circle(ws, BLUE, (300, 50), 20, 0)

# Draw a red ellipse
pygame.draw.ellipse(ws, RED, (300, 250, 40, 80), 1)

# Draw the text's background rectangle
pygame.draw.rect(ws, RED, (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))

# Get a pixel array of the surface
pixArray = pygame.PixelArray(ws)
pixArray[480][380] = BLACK
del pixArray

# Draw the text onto the surface
ws.blit(text, textRect)

# Draw the window onto the screen
pygame.display.update()

# Run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
