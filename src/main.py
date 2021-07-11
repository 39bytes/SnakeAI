import time
import math
import json
import pygame

import numpy as np
from numpy.random import RandomState

from neuralnetwork import NeuralNetwork
from snakegame import SnakeGame
from population import Population
from snake import Snake

SCALE = 16
SIZE = 256

test = True


def main():
    fps = 15
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("SnakeAI")

    if test:
        screen = pygame.display.set_mode((SIZE, SIZE))
    else:
        screen = pygame.display.set_mode((SIZE * 5, SIZE * 2))

    background = pygame.Surface(screen.get_size()).convert()

    if test:  # Testing a single snake
        snake = load_snake("snakes.json")
        game = SnakeGame(snake, SIZE / SCALE,
                         RandomState(math.floor(time.time())))
        while True:
            # Fill background with black (clear screen)
            background.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            game.update()

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

            game.check_for_collision()

            if game.gameover:
                raise SystemExit

            # Blits everything to the screen
            screen.blit(background, (0, 0))
            pygame.display.flip()

            # Framerate
            pygame.time.wait(1000 // fps)

    # Create the population
    population = Population(300)
    games = initialize_games(population)

    create_json("snakes.json")

    # Game loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            # Speed up or slow down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and fps <= 115:  # max 120 fps
                    fps += 5
                if event.key == pygame.K_DOWN and fps >= 5:  # min 5 fps
                    fps -= 5

        # For offsetting each correctly in order to draw them in a 5x2 grid
        xOffset = 0
        yOffset = 0

        # Fill background with black (clear screen)
        background.fill((0, 0, 0))
        screen.blit(background, (0, 0))

        for num, game in enumerate(games):
            if num < 10:  # Only displaying the first 10 snakes
                # White grid lines
                pygame.draw.rect(background, (255, 255, 255),
                                 (xOffset * SIZE, yOffset * SIZE, SIZE, SIZE), width=1)
                if game.gameover:  # Draw black screen if dead
                    pygame.draw.rect(background, (0, 0, 0),
                                     (xOffset * SIZE + 1, yOffset * SIZE + 1, SIZE - 1, SIZE - 1))
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

        # Framerate
        pygame.time.wait(1000 // fps)

        # Check if all snakes are dead
        allDead = True
        numAlive = 0
        for game in games:
            if not game.gameover:
                numAlive += 1
                allDead = False
                break

        # Create the next generation if so
        if allDead:
            bestSnake = population.get_best_snake()  # Best performer for this generation
            print(f"Max Score: {bestSnake.score}")
            if bestSnake.score > population.bestScore:  # If the snake was a new best write it to disk
                population.bestScore = bestSnake.score
                write_snake("snakes.json", population.generation, bestSnake)

            population.create_next_gen()
            games = initialize_games(population)
            print(f"Generation:{population.generation}")


# Initializes each snake game with the same seed for its random number generator
def initialize_games(population):
    seed = math.floor(time.time())
    return [SnakeGame(snake=snake, gridSize=SIZE / SCALE, rng=RandomState(seed))
            for snake in population.snakes]


def create_json(filename):
    with open(filename, "w+") as f:
        f.write("[]")


def write_snake(filename, generation, snake):
    with open(filename, "r+") as f:
        try:
            data = json.load(f)
        except:
            data = []
        obj = {}
        obj["generation"] = generation
        obj["score"] = snake.score
        obj["weights"] = [arr.tolist()
                          for arr in snake.network.weights]
        obj["biases"] = [arr.tolist()
                         for arr in snake.network.biases]
        data.append(obj)
        f.seek(0)
        json.dump(data, f, indent=4)

# Loads a snake from disk for testing, returns the last snake by default.


def load_snake(filename, num=-1):
    with open(filename, "r+") as f:
        try:
            data = json.load(f)
        except:
            raise Exception('Snakes file has no snakes to load.')

        weights = [np.array(arr) for arr in data[num]["weights"]]
        biases = [np.array(arr) for arr in data[num]["biases"]]
        network = NeuralNetwork([24, 18, 4], weights, biases)

        return Snake(network)


if __name__ == '__main__':
    main()
