from pygame import Vector2


class SnakeGame:

    def __init__(self, snake, gridSize, rng):
        self.gridSize = gridSize
        self.gameover = False

        self.snake = snake

        """The random number generator for the game
        Each instance of a game has the same seed for its random number generator
        for a generation so that each snake has the same conditions."""
        self.rng = rng
        self.spawn_apple()

    def update(self):
        # Snake decides what direction to go in using the network
        self.snake.decide(self.apple, self.gridSize)

        # he move
        self.snake.move()

        # Check if the snake head is on the apple
        if self.snake.body[0] == self.apple:
            # If so grow the snake, spawn a new apple and increment score
            self.snake.grow()
            self.spawn_apple()
            self.snake.score += 1

        if self.snake.movesLeft == 0:
            self.gameover = True

    # Spawns an apple at a random position on the field, apple cannot be inside of the snake's body.
    def spawn_apple(self):
        self.apple = self.get_random_position()
        while self.apple in self.snake.body:
            self.apple = self.get_random_position()

    # Checks if the snake hits its own body or a wall
    def check_for_collision(self):
        if (self.snake.body[0] in self.snake.body[1:] or
            (self.snake.body[0].x >= (self.gridSize) or self.snake.body[0].x < 0) or
                (self.snake.body[0].y >= (self.gridSize) or self.snake.body[0].y < 0)):
            self.gameover = True

    def get_random_position(self):
        return Vector2(self.rng.randint(0, self.gridSize),
                       self.rng.randint(0, self.gridSize))
