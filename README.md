# SnakeAI

A program that uses a genetic algorithm to train a neural network to play Snake.

## Dependencies

- NumPy 1.23.4
- Pygame 2.1.2

## Installation

1. Clone the repository by running `git clone https://github.com/JeffDotPng/SnakeAI` in the command line.

2. Navigate to the newly created directory and run `pip install -r requirements.txt` to install the required packages.

## Usage

```
$ main.py [-h] [-m [P]] [-g [N]] [-o [filename]] [--visualize]
```

The `-h` flag displays a help message.

The `-m` flag specifies the mutation rate used by the genetic algorithm.
Genes will be mutated with probability `P`. This should be a float between 0 and 1. If no mutation rate is provided, this is set to 0.01 by default.
Anything above 0.03 is not recommended.

The `-g` flag specifies the number of generations to train for.
The program will train for `N` generations then stop. If this is not specified, this is set to 200 by default.

The `-o` flag specifies the filename of the file that the trained
models will be stored in. This file stores every model that was better than the last best model. This must be a `.json` file. If not specified,
it will be set to `snakes{currentTimestamp}.json`.

The `--visualize` flag toggles the training visualization, which displays the first 10 snake games so you can visually see the training progress. If this is turned on, the up and down arrow keys can be used to increase/decrease the FPS.
Heavily slows down the training process so this is not recommended.

To tweak other settings such as population size, grid size, etc. edit `constants.py`.

### Example Usage

To train for 1000 generations using the default mutation rate of 0.01:
`$ python main.py -g 1000 -o output.json`

After training has completed, run `snaketest.py`, which will let you watch your trained snake play the game.

```
$ python snaketest.py
Snakes file to load: output/output.json
Snake number (blank for last):
```

**Note:** Due to the randomness in snake, it may not perform as well as it did in training!
