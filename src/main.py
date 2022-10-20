import argparse
import os

parser = argparse.ArgumentParser(description="Trains a neural network to play Snake using genetic algorithms.")

parser.add_argument('--mutation-rate', type=float, help='''The mutation rate to use for the genetic algorithm. 
                                                           This should be a float between 0 and 1.
                                                           By default, this is set to 0.01. Anything above 0.03 is not recommended.''')
parser.add_argument('--generations', type=int, help='The number of generations to run the training process for.')
parser.add_argument('--draw', action='store_true',
                    help='''Displays the first 10 snake games so you can visually see the training progress.
                            Heavily slows down the training process so this is not recommended.''')

if __name__ == "__main__":
    pass