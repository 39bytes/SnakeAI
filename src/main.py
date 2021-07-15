import time
import math
import pygame

from numpy.random import RandomState

from snakegame import SnakeGame
from population import Population
from snakejson import create_json, write_snake, load_snake, log_score

SCALE = 16
SIZE = 256

train = False


class SnakeAI:
    def __init__(self, training):
        pygame.init()
        pygame.display.set_caption("SnakeAI")

        timestamp = get_timestamp()
        self.bestSnakesFile = f"snakes{timestamp}.json"
        self.scoresFile = f"scores{timestamp}.json"

        if training:
            self.screen = pygame.display.set_mode(
                (SIZE * 5, SIZE * 2))  # Display 10 snakes
        else:
            # Display only the one snake to test
            self.screen = pygame.display.set_mode((SIZE, SIZE))
        self.background = pygame.Surface(self.screen.get_size()).convert()

        self.fps = 15

    def train(self):
        # Create log files
        create_json(self.bestSnakesFile)
        create_json(self.scoresFile)

        # Initialisation
        population = Population(300)
        games = self.initialize_games(population)

        # Game loop
        while True:
            self.get_input()
            self.update(games)
            pygame.time.wait(1000 // self.fps)

            # Check if all snakes are dead
            allDead = True
            numAlive = 0
            for game in games:
                if not game.gameover:
                    numAlive += 1
                    allDead = False
                    break

            if allDead:
                games = self.next_gen(population)

    def test(self, filename, num=-1):
        snake = load_snake(filename, num)
        # Put the single game in an array so i can reuse the update function
        game = [SnakeGame(snake, SIZE / SCALE,
                          RandomState(math.floor(time.time())))]
        while True:
            self.get_input()
            self.update(game)
            pygame.time.wait(1000 // self.fps)

            if game[0].gameover:
                raise SystemExit

    # Initializes each snake game with the same seed for its random number generator
    def initialize_games(self, population):
        seed = math.floor(time.time())
        return [SnakeGame(snake=snake, gridSize=SIZE / SCALE, rng=RandomState(seed))
                for snake in population.snakes]

    def get_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
            # Speed up or slow down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.fps <= 115:  # max 120 fps
                    self.fps += 5
                if event.key == pygame.K_DOWN and self.fps >= 5:  # min 5 fps
                    self.fps -= 5

    def update(self, games):
        # For offsetting each correctly in order to draw them in a 5x2 grid
        xOffset = 0
        yOffset = 0

        # Fill background with black (clear screen)
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        for num, game in enumerate(games):
            if num < 10:  # Only displaying the first 10 snakes
                # White grid lines
                pygame.draw.rect(self.background, (255, 255, 255),
                                 (xOffset * SIZE, yOffset * SIZE, SIZE, SIZE), width=1)
                if game.gameover:  # Draw black screen if dead
                    pygame.draw.rect(self.background, (0, 0, 0),
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
                    pygame.draw.rect(self.background, (255, 255, 255),
                                     (xOffset * SIZE + segment.x * SCALE + 1,
                                     yOffset * SIZE + segment.y * SCALE + 1,
                                     SCALE - 1, SCALE - 1))

                # Draw the apple
                pygame.draw.rect(self.background, (255, 0, 0),
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
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    # Writes this generation to disk and creates the next generation
    def next_gen(self, population):
        bestSnake = population.get_best_snake()  # Best performer for this generation
        print(f"Max Score: {bestSnake.score}")
        if bestSnake.score > population.bestScore:  # If the snake was a new best write it to disk
            population.bestScore = bestSnake.score
            write_snake(self.bestSnakesFile, population.generation, bestSnake)
        log_score(self.scoresFile, bestSnake.score)

        population.create_next_gen()
        print(f"Generation:{population.generation}")
        return self.initialize_games(population)


def get_timestamp():
    return math.floor(time.time())


if __name__ == '__main__':
    s = SnakeAI(train)
    if train:
        s.train()
    else:
        s.test("snakes1626367905.json")
