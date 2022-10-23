# SnakeAI

A program that uses a genetic algorithm to train a neural network to play Snake.

# Dependencies

- NumPy 1.23.4
- Pygame 2.1.2

# Installation

Run the following command:

```
pip install -r requirements.txt
```

# Usage

```
main.py [-h] [--mutation MUTATION] [--generations GENERATIONS] [--visualize]
        [-o OUTPUT]

options:
  -h, --help            show this help message and exit
  --mutation MUTATION   The mutation rate to use for the genetic algorithm. This should
                        be a float between 0 and 1. By default, this is set to 0.01.
                        Anything above 0.03 is not recommended.
  --generations GENERATIONS
                        The number of generations to run the training process for.
  --visualize           Displays the first 10 snake games so you can visually see the
                        training progress. Heavily slows down the training process so
                        this is not recommended.
                        If visualization is on, the up and down arrow keys can be used
                        to increase or decrease the framerate cap limit.
  -o OUTPUT, --output OUTPUT
                        The JSON file that the best models from each generation will be
                        stored in.
```
