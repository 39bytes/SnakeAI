import pygame
import math
import time

from numpy.random import RandomState

from constants import MAX_FPS, SIZE, SCALE
from snakejson import load_snake
from snakegame import SnakeGame


# Much of this testing code is just reused from the training code


def test_snake(filename, num=-1):
    pygame.init()
    pygame.display.set_caption("SnakeAI")

    screen = pygame.display.set_mode((SIZE, SIZE))
    background = pygame.Surface(screen.get_size()).convert()

    snake = load_snake(filename, num)
    game = SnakeGame(snake, SIZE / SCALE,
                     RandomState(math.floor(time.time())))
    fps = 15
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Speed up or slow down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and fps + 5 <= MAX_FPS:
                    fps += 5
                if event.key == pygame.K_DOWN and fps - 5 >= 5:  # min 5 fps
                    fps -= 5
        # Fill background with black (clear screen)
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        game.update()

        # Draw the snake
        for segment in game.snake.body:
            pygame.draw.rect(background, (255, 255, 255),
                             (segment.x * SCALE + 1,
                                 segment.y * SCALE + 1,
                                 SCALE - 1, SCALE - 1))

        # Draw the apple
        pygame.draw.rect(background, (255, 0, 0),
                         (game.apple.x * SCALE + 1,
                             game.apple.y * SCALE + 1,
                             SCALE - 1, SCALE - 1))

        # Check for game overs
        game.check_for_collision()

        # Blits everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        pygame.time.wait(1000 // fps)

        if game.gameover:
            print(snake.score)
            raise SystemExit


if __name__ == "__main__":
    filename = input("Snakes file to load:")
    num = input("Snake number (blank for last):")

    test_snake(filename, int(num) if num != "" else -1)
