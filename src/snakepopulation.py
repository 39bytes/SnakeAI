from operator import attrgetter
from functools import reduce
import random

import numpy as np

from snake import Snake
from neuralnetwork import NeuralNetwork


class SnakePopulation:
    def __init__(self):
        self.snakes = [generate_random_snake() for x in range(10)]
        self.mutationRate = 0.05
        self.generation = 1

    def select(self):
        ordered = sorted(self.snakes, key=attrgetter(
            'score', 'movesSurvived'), reverse=True)

        # Top 4 snakes
        return ordered[:4]

    def crossover(self, snake1: Snake, snake2: Snake):
        # Both snakes have the same network shapes
        weightShapes = [x.shape for x in snake1.network.weights]
        biasShapes = [x.shape for x in snake1.network.biases]

        # Flatten both arrays into 1d for crossover
        weights1 = flatten(snake1.network.weights)
        weights2 = flatten(snake2.network.weights)

        # Pick a random crossover point for the weights
        weightCrossover = random.randint(1, len(weights1) - 1)

        # Swap, weights2 becomes the child's weights
        weights2[0:weightCrossover] = weights1[0:weightCrossover]

        # Same but for biases
        biases1 = flatten(snake1.network.biases)
        biases2 = flatten(snake2.network.biases)

        biasCrossover = random.randint(1, len(snake1.network.biases))

        biases2[0:biasCrossover] = biases1[0:biasCrossover]

        childWeights = weights2
        childBiases = biases2

        # Mutate
        self.mutate(childWeights)
        self.mutate(childBiases)

        childWeights = unflatten(childWeights, weightShapes)
        childBiases = unflatten(childBiases, biasShapes)

        # Return a child created from the crossed over genes
        return Snake(NeuralNetwork([24, 30, 4], childWeights, childBiases))

    def create_next_gen(self):
        newGen = []
        fittest = self.select()
        for i in range(10):
            # Picks 2 parents for the crossover
            parents = np.random.choice(range(4), 2, replace=False)
            child = self.crossover(fittest[parents[0]], fittest[parents[1]])
            newGen.append(child)
        self.snakes = newGen

    def mutate(self, arr):
        for i in range(len(arr)):
            if np.random.rand() < self.mutationRate:
                arr[i] = np.random.randn()


"""Weights is a list of randomly generated matrices with dimensions
y by x, where x is the number of neurons in layer L and y is the number
of neurons in the layer L+1.

Biases is a list of randomly generated column vectors for each
layer excluding the input layer.
"""


def generate_random_snake():
    sizes = [24, 30, 4]
    weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
    biases = [np.random.randn(y, 1) for y in sizes[1:]]

    return Snake(NeuralNetwork(sizes, weights, biases))

# Function for flattening weights and biases into a 1d array for crossover


def flatten(arr):
    # Flatten list of 2d arrays into list of 1d
    flattened = [x.flatten() for x in arr]

    # Joins each 1d array in the list into a single 1d np array
    return reduce(lambda a, b: np.concatenate((a, b)), flattened)


def unflatten(arr, shapes):
    unflattened = []

    index = 0
    for shape in shapes:
        # Gets the total length of the shape (ex: 2x3 matrix = 6)
        size = np.product(shape)

        # Reshapes each slice back into its matrix shape
        unflattened.append(np.reshape(arr[index:index+size], shape))

        # Move to the next slice starting point
        index += size
    return unflattened
