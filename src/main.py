import pygame
import time
import math
import sys

from numpy.random import RandomState

from snakegame import SnakeGame
from population import Population

SCALE = 16
SIZE = 256


def main():
    fps = 15
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("SnakeAI")

    screen = pygame.display.set_mode((SIZE * 5, SIZE * 2))
    background = pygame.Surface(screen.get_size()).convert()

    # Create the population
    population = Population(300)
    games = initialize_games(population)

    # Game loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    fps += 5
                if event.key == pygame.K_DOWN:
                    fps -= 5

        # For offsetting each correctly in order to draw them in a 5x2 grid
        xOffset = 0
        yOffset = 0

        # Fill background with black (clear screen)
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for num, game in enumerate(games):
            if num < 10:
                pygame.draw.rect(background, (255, 255, 255),
                                 (xOffset * SIZE, yOffset * SIZE, SIZE, SIZE), width=1)
                if game.gameover:  # Draw black screen if dead
                    pygame.draw.rect(background, (0, 0, 0),
                                     (xOffset * SIZE, yOffset * SIZE, SIZE, SIZE))
                    xOffset += 1
                    if xOffset == 5:
                        xOffset = 0
                        yOffset += 1
                    continue

            game.update()

            if num < 10:
                # Draw the snake
                for segment in game.snake.body:
                    pygame.draw.rect(background, (255, 255, 255),
                                     (xOffset * SIZE + segment.x * SCALE + 1,
                                     yOffset * SIZE + segment.y * SCALE + 1,
                                     SCALE - 1, SCALE - 1))

                # Draw the apple
                pygame.draw.rect(background, (255, 0, 0),
                                 (xOffset * SIZE + game.apple.x * SCALE + 1,
                                 yOffset * SIZE + game.apple.y * SCALE + 1,
                                 SCALE - 1, SCALE - 1))

                xOffset += 1
                if xOffset == 5:
                    xOffset = 0
                    yOffset += 1

            # Check for game overs
            game.check_for_collision()

        # Blits everything to the screen
        screen.blit(background, (0, 0))
        pygame.display.flip()

        pygame.time.wait(1000 // fps)  # 15 fps

        allDead = True
        numAlive = 0
        for game in games:
            if not game.gameover:
                numAlive += 1
                allDead = False

        # sys.stdout.write((" " * (4 - len(str(numAlive)))) +
        #                  f"\rGeneration: {population.generation}, Snakes alive: {numAlive}")
        # sys.stdout.flush()

        if allDead:
            print(f"Max Score: {population.get_highest_score()}")
            population.create_next_gen()
            games = initialize_games(population)
            print(f"Generation:{population.generation}")


def initialize_games(population):
    seed = math.floor(time.time())
    return [SnakeGame(snake=snake, gridSize=SIZE / SCALE, rng=RandomState(seed))
            for snake in population.snakes]


if __name__ == '__main__':
    main()
