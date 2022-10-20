import math
from typing import Literal

import numpy as np
from numpy.random import RandomState
from pygame import Vector2

from neuralnetwork import NeuralNetwork


class Snake:
    def __init__(self, network: NeuralNetwork):
        # Each part of the snakes body as (x, y) coordinates. First elem is the head, last elem is the tail
        self.body = [Vector2(3, 8), Vector2(2, 8), Vector2(1, 8)]
        # Direction the snake is going, (1, 0) is to the right, (0, 1) is down, etc.
        self.direction = Vector2(1, 0)

        self.movesSurvived = 0
        self.movesLeft = 100

        self.score = 0
        self.fitness = 0

        # The neural network which does the decisions
        self.network = network

    def move(self):
        # Add direction to head
        new_head = self.body[0] + self.direction

        # Push that to the top of the stack
        self.body.insert(0, new_head)

        # Pop the last elem
        self.body.pop()

        self.movesSurvived += 1
        self.movesLeft -= 1

    def change_direction(self, d: Literal["up", "down", "right", "left"]):
        # Don't let the snake go in the opposite direction
        if d == "up" and self.direction != Vector2(0, 1):
            self.direction = Vector2(0, -1)
        elif d == "down" and self.direction != Vector2(0, -1):
            self.direction = Vector2(0, 1)
        elif d == "left" and self.direction != Vector2(1, 0):
            self.direction = Vector2(-1, 0)
        elif d == "right" and self.direction != Vector2(-1, 0):
            self.direction = Vector2(1, 0)

    # gridSize is used for determining the distance from the head to a wall
    def decide(self, applePos: Vector2, gridSize: int):
        inputs = self.look(applePos, gridSize)
        move = self.network.evaluate(inputs)

        if move == 0:
            self.change_direction("up")
        elif move == 1:
            self.change_direction("down")
        elif move == 2:
            self.change_direction("right")
        elif move == 3:
            self.change_direction("left")

    """ Looks in 8 directions in order to determine the inputs
    Each direction has 3 values associated with it:
    1: Is the apple in that direction? (bool)
    2: 1 / (Distance to a body segment)
    3: 1 / (Distance to a wall in that direction)
    The reciprocal of distances is taken so that the activation
    is greater when the distance is small (ex: if the snake is
    right next to a wall the activation should be 1) """

    def look(self, applePos: Vector2, gridSize: int):
        directions = (Vector2(0, -1),  # Up
                      Vector2(1, -1),  # Up-right
                      Vector2(1, 0),  # Right
                      Vector2(1, 1),  # Down-right
                      Vector2(0, 1),  # Down
                      Vector2(-1, 1),  # Down-Left
                      Vector2(-1, 0),  # Left
                      Vector2(-1, -1))  # Up-Left

        # Values to be returned as input to the neural network
        values = [0] * 24

        for index, direction in enumerate(directions):
            dist = 0

            # Look from the snake head
            position = self.body[0]

            # Ensures the body segment used as input is the closest one
            bodyFound = False

            # While position is within the grid bounds
            while (0 <= position.x < gridSize) and (0 <= position.y < gridSize):
                # Go forward in that direction by 1
                position = position + direction
                dist += 1

                if position == applePos:
                    values[index * 3] = 1

                if position in self.body and not bodyFound:
                    values[index * 3 + 1] = 1 / dist
                    bodyFound = True

                if (not (0 < position.x < gridSize)) or (not (0 < position.y < gridSize)):
                    values[index * 3 + 2] = 1 / dist

        # Convert to numpy array and transpose to column vector
        return np.atleast_2d(np.array(values)).T

    def grow(self):
        # If the snake grows it means that it ate an apple so give it more moves before it dies
        if self.score <= 50:
            self.movesLeft = 150
        else:
            self.movesLeft = 255
        self.score += 1

        # The direction the tail is traveling
        d = self.body[-2] - self.body[-1]
        self.body.append(self.body[-1] - d)  # Add to body

    def calc_fitness(self):
        self.fitness = ((3 * self.score) ** 2 + self.movesSurvived / 10)

        
class SnakeGame:
    def __init__(self, snake: Snake, gridSize: int, rng: RandomState):
        self.gridSize = gridSize
        self.gameover = False

        self.snake = snake

        """The random number generator for the game
        Each instance of a game has the same seed for its random number generator
        for a generation so that each snake has the same conditions."""
        self.rng = rng
        self.spawn_apple()

    def update(self):
        # Snake decides what direction to go in using the network
        self.snake.decide(self.apple, self.gridSize)

        # he move
        self.snake.move()

        # Check if the snake head is on the apple
        if self.snake.body[0] == self.apple:
            # If so grow the snake, spawn a new apple and increment score
            self.snake.grow()
            self.spawn_apple()
            self.snake.score += 1

        if self.snake.movesLeft == 0:
            self.gameover = True

    # Spawns an apple at a random position on the field, apple cannot be inside of the snake's body.
    def spawn_apple(self):
        self.apple = self.get_random_position()
        while self.apple in self.snake.body:
            self.apple = self.get_random_position()

    # Checks if the snake hits its own body or a wall
    def check_for_collision(self):
        if (self.snake.body[0] in self.snake.body[1:] or
            (self.snake.body[0].x >= (self.gridSize) or self.snake.body[0].x < 0) or
                (self.snake.body[0].y >= (self.gridSize) or self.snake.body[0].y < 0)):
            self.gameover = True

    def get_random_position(self):
        return Vector2(self.rng.randint(0, self.gridSize),
                       self.rng.randint(0, self.gridSize))
