import argparse
import os
from trainer import SnakeTrainer

def main():
    parser = argparse.ArgumentParser(description="Trains a neural network to play Snake using genetic algorithms.")

    parser.add_argument('--mutation', '-m', type=float, default=0.01,
                         help='''The mutation rate to use for the genetic algorithm. 
                                 This should be a float between 0 and 1.
                                 By default, this is set to 0.01. Anything above 0.03 is not recommended.''')
    parser.add_argument('--generations', '-g', type=int, default=200,
                        help='The number of generations to run the training process for.')
    parser.add_argument('--visualize', action='store_true',
                        help='''Displays the first 10 snake games in every generation so you can visually see the training progress.
                                Heavily slows down the training process so this is not recommended.''')
    parser.add_argument('-o', '--output',
                        type=str,
                        help='''The JSON file that the best models from each generation will be
                                stored in.''')
    args = parser.parse_args()

    if not 0 <= args.mutation <= 1:
        raise ValueError("Mutation rate should be in between 0 and 1.")
    
    output = args.output
    if not output:
        output = ""
        
    
    trainer = SnakeTrainer(mutationRate=args.mutation, 
                           maxGeneration=args.generations,
                           visualize=args.visualize,
                           bestSnakesFile=output,
                           scoresFile="")
    trainer.train()
        
        

if __name__ == "__main__":
    main()