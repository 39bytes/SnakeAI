import numpy as np


class NeuralNetwork:
    def __init__(self, sizes, weights, biases):
        self.sizes = sizes
        self.weights = weights
        self.biases = biases

    """Activation in the next layer equals
    ReLU(WeightMatrix * CurrentActivations + Biases)
    """

    def evaluate(self, inputs):
        a = inputs
        for w, b in zip(self.weights, self.biases):
            a = relu(np.dot(w, a) + b)

        # Returns brightest activation in output layer
        return np.argmax(a)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

# Activation function


def relu(z):
    return np.maximum(0, z)
