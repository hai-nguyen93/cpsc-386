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


def draw_text(surface, text, x, y):
    font = pygame.font.Font(None, 30)
    text_render = font.render(text, True, WHITE, BLACK)
    text_rect = text_render.get_rect()
    text_rect.left = x + 20
    text_rect.top = y + 20
    surface.blit(text_render, text_rect)


def reset_ball(ball):
    ball.x = 400
    ball.y = 250
    ball.velocity.x = random.randint(-9, 10) * 1.2
    ball.velocity.y = random.randint(-9, 10) * 1.2
    while ball.velocity.magnitude() <= 7 or ball.velocity.x == 0 or ball.velocity.y == 0:
        ball.velocity.x = random.randint(-9, 10) * 1.2
        ball.velocity.y = random.randint(-9, 10) * 1.2


def play_game(surface):
    move_up, move_down, move_left, move_right = False, False, False, False

    ball_image = pygame.image.load('images/ball.png')
    vertical_paddle_image = pygame.image.load('images/vertical_paddle.png')
    horizontal_paddle_image = pygame.image.load('images/horizontal_paddle.png')
    ball = objects.Ball(x=400, y=250, velocity=(5, 0), image=ball_image)

    player = objects.Score()
    computer = objects.Score()
    player_paddles = []
    player_paddles.append(objects.Paddle(SCR_WIDTH-vertical_paddle_image.get_rect().right, 250, vertical_paddle_image))
    computer_paddles = []
    computer_paddles.append(objects.Paddle(0, 250, vertical_paddle_image))

    no_winner = True
    while no_winner:
        # Check for winner
        if player.game_point == 3 or computer.game_point == 3:
            no_winner = False

            # Display winner

            # Play again
            draw_text(surface, 'Play again? (Press Y or N)', SCR_WIDTH / 2 - 136, SCR_HEIGHT / 2 - 40)
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

        # Check game score
        if player.point >= 11 and player.point - computer.point >= 2:
            player.game_point += 1
            player.point, computer.point = 0, 0
        if computer.point >= 11 and computer.point - player.point >= 2:
            computer.game_point += 1
            player.point, computer.point = 0, 0

        ball.update()
        if ball.y < 0 or ball.y + ball.image_rect.bottom >= SCR_HEIGHT-SCORES_HEIGHT:
            if ball.x + ball.image_rect.centerx <= SCR_WIDTH/2:
                player.point += 1
            else:
                computer.point += 1
            reset_ball(ball)
        if ball.x < 0:
            player.point += 1
            reset_ball(ball)
        if ball.x + ball.image_rect.right > SCR_WIDTH:
            computer.point += 1
            reset_ball(ball)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    move_up = True
                if event.key == K_DOWN:
                    move_down = True

            if event.type == KEYUP:
                if event.key == K_UP:
                    move_up = False
                if event.key == K_DOWN:
                    move_down = False

        # Move paddles
        if move_up:
            for paddle in player_paddles:
                if paddle.vertical:
                    if paddle.y > 0:
                        paddle.y -= 10
        if move_down:
            for paddle in player_paddles:
                if paddle.vertical:
                    if paddle.y + paddle.image_rect.bottom < SCR_HEIGHT-SCORES_HEIGHT:
                        paddle.y += 10

        # Check for collision
        ball_rect = pygame.Rect(ball.x, ball.y, ball.image_rect.right, ball.image_rect.bottom)
        for paddle in player_paddles:
            paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.image_rect.right, paddle.image_rect.bottom)
            if ball_rect.colliderect(paddle_rect):
                if paddle.vertical:
                    ball.velocity.x *= -1
        for paddle in computer_paddles:
            paddle_rect = pygame.Rect(paddle.x, paddle.y, paddle.image_rect.right, paddle.image_rect.bottom)
            if ball_rect.colliderect(paddle_rect):
                if paddle.vertical:
                    ball.velocity.x *= -1

        print((ball.x, ball.y))
        print((ball_rect.x, ball_rect.y))

        surface.fill(BLACK)
        pygame.draw.line(surface, WHITE, (0, SCR_HEIGHT - SCORES_HEIGHT), (SCR_WIDTH, SCR_HEIGHT - SCORES_HEIGHT))
        pygame.draw.line(surface, WHITE, (SCR_WIDTH / 2, 0), (SCR_WIDTH / 2, SCR_HEIGHT - SCORES_HEIGHT))

        draw_text(surface, 'Player: {}'.format(player.point), x=SCR_WIDTH/2, y=SCR_HEIGHT-SCORES_HEIGHT)
        draw_text(surface, 'Game point: {}'.format(player.game_point), x=SCR_WIDTH/2, y=SCR_HEIGHT-SCORES_HEIGHT+40)
        draw_text(surface, 'Computer: {}'.format(computer.point), x=0, y=SCR_HEIGHT-SCORES_HEIGHT)
        draw_text(surface, 'Game point: {}'.format(computer.game_point), x=0, y=SCR_HEIGHT-SCORES_HEIGHT+40)

        surface.blit(ball_image, (ball.x, ball.y))
        for paddle in computer_paddles:
            surface.blit(paddle.image, (paddle.x, paddle.y))
        for paddle in player_paddles:
            surface.blit(paddle.image, (paddle.x, paddle.y))



        pygame.display.update()
        time.sleep(0.017)


def play():
    pygame.init()
    surface = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT), 0, 32)
    pygame.display.set_caption('Pong')

    surface.fill(BLACK)
    pygame.draw.line(surface, WHITE, (0, SCR_HEIGHT-SCORES_HEIGHT), (SCR_WIDTH, SCR_HEIGHT-SCORES_HEIGHT))
    pygame.draw.line(surface, WHITE, (SCR_WIDTH/2, 0), (SCR_WIDTH/2, SCR_HEIGHT-SCORES_HEIGHT))

    pygame.display.update()
    play_game(surface)


play()
