import json
import os

import numpy as np

from constants import *
from neuralnetwork import NeuralNetwork
from snake import Snake

OUTPUT_DIR_NAME = "output"

def create_output_folder():
    if not os.path.exists(OUTPUT_DIR_NAME):
        os.mkdir(OUTPUT_DIR_NAME)


def create_json(filename: str):
    with open(os.path.join(OUTPUT_DIR_NAME,filename), "w+") as f:
        f.write("[]")


def write_snake(filename: str, generation: int, snake: Snake):
    with open(os.path.join(OUTPUT_DIR_NAME,filename), "r+") as f:
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


def load_snake(filename: str, num=-1):
    # Loads a snake from disk for testing, returns the last snake by default.
    with open(os.path.join(OUTPUT_DIR_NAME,filename), "r+") as f:
        try:
            data = json.load(f)
        except:
            raise Exception('Snakes file has no snakes to load.')

        weights = [np.array(arr) for arr in data[num]["weights"]]
        biases = [np.array(arr) for arr in data[num]["biases"]]
        network = NeuralNetwork(NN_SHAPE, weights, biases)

        return Snake(network)

# Generation log is just an array of integers (best score for each gen)


def log_score(filename: str, score: int):
    with open(os.path.join(OUTPUT_DIR_NAME,filename), "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(score)
        f.seek(0)
        json.dump(data, f, indent=4)
