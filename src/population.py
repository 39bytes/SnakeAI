from operator import attrgetter
from functools import reduce

import random
import numpy as np

from snake import Snake
from neuralnetwork import NeuralNetwork
import constants


class Population:
    def __init__(self, size, mutationRate):
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

    def roulette_wheel_select(self):
        matingPool = []
        for snake in self.snakes:
            snake.calc_fitness()

        # Sum of all snake fitness values
        fitnessSum = sum([snake.fitness for snake in self.snakes])

        # Normalize each fitness value to an integer between 0 and the population size
        for snake in self.snakes:
            snake.fitness = round(snake.fitness/fitnessSum * self.size)
            # Add the snake to the mating pool that many times
            for _ in range(snake.fitness):
                matingPool.append(snake)

        return matingPool

    def elitist_select(self):
        matingPool = []
        for snake in self.snakes:
            snake.calc_fitness()

        ordered = sorted(self.snakes, key=attrgetter('fitness'), reverse=True)

        # Returns the the top percentage according to elitismPercent
        return ordered[:int(self.elitismPercent * self.size)]

        # fitnessSum = sum([snake.fitness for snake in fittest])

        # for snake in self.snakes:
        #     snake.fitness = round(snake.fitness/fitnessSum * len(fittest))
        #     for _ in range(snake.fitness):
        #         matingPool.append(snake)

        # return matingPool

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
        return Snake(NeuralNetwork(constants.NN_SIZES, childWeights, childBiases))

    # Copies the genes to child and mutates
    # This method relies entirely on mutation for evolution
    def copy_crossover(self, snake: Snake):
        childWeights = flatten(snake.network.weights)
        childBiases = flatten(snake.network.biases)

        weightShapes = [x.shape for x in snake.network.weights]
        biasShapes = [x.shape for x in snake.network.biases]

        self.mutate(childWeights)
        self.mutate(childBiases)

        childWeights = unflatten(childWeights, weightShapes)
        childBiases = unflatten(childBiases, biasShapes)

        return Snake(NeuralNetwork(constants.NN_SIZES, childWeights, childBiases))

    def create_next_gen(self):
        matingPool = self.roulette_wheel_select()
        newGen = []

        # for _ in range(self.size):
        #     # Picks 2 parents for the crossover
        #     parent1 = matingPool[random.randint(0, len(matingPool) - 1)]
        #     parent2 = matingPool[random.randint(0, len(matingPool) - 1)]
        #     child = self.point_crossover(parent1, parent2)
        #     newGen.append(child)
        for _ in range(self.size):
            parent = matingPool[random.randint(0, len(matingPool) - 1)]
            child = self.copy_crossover(parent)
            newGen.append(child)

        self.snakes = newGen
        self.generation += 1

    def mutate(self, arr):
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
    sizes = constants.NN_SIZES
    weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
    biases = [np.random.randn(y, 1) for y in sizes[1:]]

    return Snake(NeuralNetwork(sizes, weights, biases))


# Function for flattening weights and biases into a 1d array for crossover
def flatten(arr):
    # Flatten list of 2d arrays into list of 1d
    flattened = [x.flatten() for x in arr]

    # Joins each 1d array in the list into a single 1d np array
    return reduce(lambda a, b: np.concatenate((a, b)), flattened)


# Function that unflattens arrays produced by the above function back into their original shape
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
