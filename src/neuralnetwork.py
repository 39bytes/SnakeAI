from typing import Tuple

import numpy as np


class NeuralNetwork:
    def __init__(self, sizes: Tuple[int, ...], weights: np.ndarray, biases: np.ndarray):
        self.sizes = sizes  # The number of neurons in each layer
        self.weights = weights
        self.biases = biases

    def evaluate(self, inputs: np.ndarray):
        a = inputs
        for w, b in zip(self.weights, self.biases):
            a = sigmoid(np.dot(w, a) + b)

        return np.argmax(a)


# Activation functions
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def relu(z):
    return np.maximum(0, z)
