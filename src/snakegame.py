import random
import numpy as np

import pygame
from pygame import Vector2

from snake import Snake
from neuralnetwork import NeuralNetwork

SCALE = 16
SIZE = 256


class SnakeGame:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake")

        self.screen = pygame.display.set_mode((SIZE, SIZE))
        self.background = pygame.Surface(self.screen.get_size()).convert()

        # Objects
        sizes = [24, 30, 4]
        weights = [np.random.randn(y, x)
                   for x, y in zip(sizes[:-1], sizes[1:])]
        biases = [np.random.randn(y, 1) for y in sizes[1:]]

        self.snake = Snake(NeuralNetwork(sizes, weights, biases))
        self.spawn_apple()

        self.gameover = False

    def update(self, events):

        # Flag for making sure only 1 input is allowed per frame
        # inputted = False
        # for event in events:
        #     # Accept input
        #     if event.type == pygame.KEYDOWN and not inputted:
        #         inputted = True
        #         if event.key == pygame.K_LEFT:
        #             self.snake.change_direction("left")
        #         elif event.key == pygame.K_RIGHT:
        #             self.snake.change_direction("right")
        #         elif event.key == pygame.K_UP:
        #             self.snake.change_direction("up")
        #         elif event.key == pygame.K_DOWN:
        #             self.snake.change_direction("down")

        # Snake decides what direction to go in using the network
        self.snake.decide(self.apple, SIZE / SCALE)

        # he move
        self.snake.move()

        self.clear_screen()

        # Draw the snake
        for segment in self.snake.body:
            pygame.draw.rect(self.background, (255, 255, 255),
                             (segment.x * SCALE + 1, segment.y * SCALE + 1, SCALE - 1, SCALE - 1))

        # Draw the apple
        pygame.draw.rect(self.background, (255, 0, 0),
                         (self.apple.x * SCALE + 1, self.apple.y * SCALE + 1, SCALE - 1, SCALE - 1))

        self.render()

        # Check if the snake head is on the apple
        if self.snake.body[0] == self.apple:
            # If so grow the snake, spawn a new apple and increment score
            self.snake.grow()
            self.spawn_apple()
            self.snake.score += 1

        # Check for game overs
        self.check_for_collision()

    # Spawns an apple at a random position on the field, apple cannot be inside of the snake's body.
    def spawn_apple(self):
        self.apple = get_random_position()
        while self.apple in self.snake.body:
            self.apple = get_random_position()

    # Checks if the snake hits its own body or a wall
    def check_for_collision(self):
        if (self.snake.body[0] in self.snake.body[1:] or
            (self.snake.body[0].x >= (SIZE / SCALE) or self.snake.body[0].x < 0) or
                (self.snake.body[0].y >= (SIZE / SCALE) or self.snake.body[0].y < 0)):
            self.gameover = True

    # Fill background with black (clear screen)
    def clear_screen(self):
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

    # Blits everything to the screen
    def render(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    # Called once the snake dies
    # Clears the screen then displays the final score
    def display_gameover(self):
        self.clear_screen()

        font = pygame.font.SysFont('Comic Sans MS', 24)
        text = font.render(
            f"Score: {self.snake.score}", False, (255, 255, 255))
        textpos = text.get_rect()

        # Center the text
        textpos.centerx = self.background.get_rect().centerx
        textpos.centery = self.background.get_rect().centery
        self.background.blit(text, textpos)
        self.render()


def get_random_position():
    return Vector2(random.randint(0, SIZE / SCALE - 1),
                   random.randint(0, SIZE / SCALE - 1))
