import math
import random
from functools import reduce
from operator import attrgetter
from typing import Tuple

import numpy as np

from constants import *
from neuralnetwork import NeuralNetwork
from snake import Snake


class Population:
    def __init__(self, size: int, mutationRate: float):
        self.size = size
        # Initializes the population with random genes
        self.snakes = [generate_random_snake() for x in range(self.size)]

        self.mutationRate = mutationRate
        self.generation = 1
        self.elitismPercent = 0.05

        # The best score yet across all generations
        self.bestScore = 0

    def get_best_snake(self):
        return max(self.snakes, key=attrgetter('score'))

    def calc_roulette_wheel_probs(self):
        fitnessSum = sum([snake.fitness for snake in self.snakes])
        return [snake.fitness/fitnessSum for snake in self.snakes]

    def elitist_select(self):
        for snake in self.snakes:
            snake.calc_fitness()

        ordered = sorted(self.snakes, key=attrgetter('fitness'), reverse=True)

        # Returns the the top percentage according to elitismPercent
        return ordered[:int(self.elitismPercent * self.size)]

    def point_crossover(self, snake1: Snake, snake2: Snake):
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
        return Snake(NeuralNetwork(NN_SHAPE, childWeights, childBiases))

    # This method relies entirely on mutation for evolution
    def copy_and_mutate(self, snake: Snake):
        childWeights = flatten(snake.network.weights)
        childBiases = flatten(snake.network.biases)

        weightShapes = [x.shape for x in snake.network.weights]
        biasShapes = [x.shape for x in snake.network.biases]

        self.mutate(childWeights)
        self.mutate(childBiases)

        childWeights = unflatten(childWeights, weightShapes)
        childBiases = unflatten(childBiases, biasShapes)

        return Snake(NeuralNetwork(NN_SHAPE, childWeights, childBiases))

    def create_next_gen(self):
        matingPool = self.elitist_select()
        newGen = []

        # Crossover will decrease with time to allow for more stable evolution
        crossover_percent = get_proportion_to_crossover(self.generation)
        crossover_amount = int(crossover_percent * POPULATION_SIZE)

        for _ in range(crossover_amount):
            # Picks 2 parents for the crossover
            # It is possible that the same snake is chosen both times, but this isn't a big deal
            parent1 = matingPool[random.randint(0, len(matingPool) - 1)]
            parent2 = matingPool[random.randint(0, len(matingPool) - 1)]
            child = self.point_crossover(parent1, parent2)
            newGen.append(child)
        
        for _ in range(POPULATION_SIZE - crossover_amount):
            parent = matingPool[random.randint(0, len(matingPool) - 1)]
            child = self.copy_and_mutate(parent)
            newGen.append(child)

        self.snakes = newGen
        self.generation += 1

    def mutate(self, arr: np.ndarray):
        for i in range(len(arr)):
            if np.random.rand() <= self.mutationRate:
                arr[i] = np.random.randn()


def generate_random_snake():
    """Weights is a list of randomly generated matrices with dimensions
    y by x, where x is the number of neurons in layer L and y is the number
    of neurons in the layer L+1.

    Biases is a list of randomly generated column vectors for each
    layer excluding the input layer.
    """
    sizes = NN_SHAPE
    weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
    biases = [np.random.randn(y, 1) for y in sizes[1:]]

    return Snake(NeuralNetwork(sizes, weights, biases))


# Function for flattening weights and biases into a 1d array for crossover
def flatten(arr: np.ndarray):
    # Flatten list of 2d arrays into list of 1d
    flattened = [x.flatten() for x in arr]

    # Joins each 1d array in the list into a single 1d np array
    return reduce(lambda a, b: np.concatenate((a, b)), flattened)


# Function that unflattens arrays produced by the above function back into their original shape
def unflatten(arr: np.ndarray, shapes: Tuple[int, ...]):
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

# Crossover will be always applied for the first 
def get_proportion_to_crossover(generation: int):
    if generation <= 100:
        return 1
    else:
        return 2/(1 + math.exp(generation/60))
