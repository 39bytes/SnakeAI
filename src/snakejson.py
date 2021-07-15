import json
import numpy as np
from neuralnetwork import NeuralNetwork
from snake import Snake
import constants


def create_json(filename):
    with open(filename, "w+") as f:
        f.write("[]")


def write_snake(filename, generation, snake):
    with open(filename, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
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


def load_snake(filename, num=-1):
    # Loads a snake from disk for testing, returns the last snake by default.
    with open(filename, "r+") as f:
        try:
            data = json.load(f)
        except:
            raise Exception('Snakes file has no snakes to load.')

        weights = [np.array(arr) for arr in data[num]["weights"]]
        biases = [np.array(arr) for arr in data[num]["biases"]]
        network = NeuralNetwork(constants.NN_SIZES, weights, biases)

        return Snake(network)

# Generation log is just an array of integers (best score for each gen)
def log_score(filename, score):
    with open(filename, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(score)
        f.seek(0)
        json.dump(data, f, indent=4)