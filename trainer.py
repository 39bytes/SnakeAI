import math
import time
from typing import List

from numpy.random import RandomState

from constants import *
from population import Population
from renderer import Renderer
from snake import SnakeGame
from snakejson import create_json, create_output_folder, log_score, write_snake

class SnakeTrainer:
    def __init__(self, mutationRate: float, maxGeneration: int, 
                 visualize: bool, bestSnakesFile="", scoresFile=""):
        # Make the output filenames use the current timestamp if not specified
        timestamp = get_timestamp()

        self.bestSnakesFile = f"snakes{timestamp}.json" if not bestSnakesFile else bestSnakesFile
        self.scoresFile = f"scores{timestamp}.json" if not scoresFile else scoresFile
        
        # Create log files
        create_output_folder()
        create_json(self.bestSnakesFile)
        # create_json(self.scoresFile)

        self.visualize = visualize
        self.mutationRate = mutationRate
        self.maxGeneration = maxGeneration

        # This initializes pygame if drawing is enabled
        if visualize:
            self.renderer = Renderer()
        
    def train(self):
        # Initialization
        population = Population(POPULATION_SIZE, self.mutationRate)
        games = self.initialize_games(population)

        # Game loop
        while population.generation <= self.maxGeneration:  # Train for 300 generations
            self.update(games)

            # Check if all snakes are dead
            active_games = [game for game in games if not game.gameover]
            allDead = len(active_games) == 0

            # If so, move onto the next generation
            if allDead:
                games = self.next_gen(population)

    def initialize_games(self, population: Population):
        # Initializes each snake game with the same seed for its random number generator
        seed = math.floor(time.time())
        return [SnakeGame(snake=snake, gridSize=int(SIZE / SCALE), rng=RandomState(seed))
                for snake in population.snakes]

    def update(self, games: List[SnakeGame]):
        if self.visualize:
            self.renderer.draw(games)

        for game in games:
            game.update()
    
    # Writes this generation to disk and creates the next generation
    def next_gen(self, population: Population):
        bestSnake = population.get_best_snake()  # Best performer for this generation
        print(f"Highest Score: {bestSnake.score} (Generation {population.generation}/{self.maxGeneration})")

        if bestSnake.score > population.bestScore:  # If the snake was a new best write it to disk
            population.bestScore = bestSnake.score
            write_snake(self.bestSnakesFile, population.generation, bestSnake)

        # Log the best score for this generation
        # log_score(self.scoresFile, bestSnake.score)

        # Create the next generation of snakes
        population.create_next_gen()

        # Return a new list of games with the new generation
        return self.initialize_games(population)


def get_timestamp():  # Returns the current timestamp (seconds)
    return math.floor(time.time())

if __name__ == '__main__':
    s = SnakeTrainer(mutationRate=0.01, maxGeneration=200, visualize=False)
    s.train()
