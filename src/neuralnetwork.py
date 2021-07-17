import numpy as np


class NeuralNetwork:
    def __init__(self, sizes, weights, biases):
        self.sizes = sizes  # The number of neurons in each layer
        self.weights = weights
        self.biases = biases

    """Activation in the next layer equals
    activationFunction(WeightMatrix * CurrentActivations + Biases)
    """

    def evaluate(self, inputs):
        a = inputs
        for w, b in zip(self.weights, self.biases):
            a = sigmoid(np.dot(w, a) + b)

        # Returns brightest activation in output layer
        return np.argmax(a)

# Activation functions


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def relu(z):
    return np.maximum(0, z)
