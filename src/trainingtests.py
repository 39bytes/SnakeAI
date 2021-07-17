from snakeai import SnakeAI


def test_mutation_rates():  # Tests 1%, 2%, 3%, and 5% mutation rates
    ai = SnakeAI(0.01, "snakesCopyCross1Percent3.json",
                 "scoresCopyCross1Percent3.json")
    ai.train()

    ai = SnakeAI(0.02, "snakesCopyCross2Percent3.json",
                 "scoresCopyCross2Percent3.json")
    ai.train()

    ai = SnakeAI(0.03, "snakesCopyCross3Percent3.json",
                 "scoresCopyCross3Percent3.json")
    ai.train()

    ai = SnakeAI(0.05, "snakesCopyCross5Percent3.json",
                 "scoresCopyCross5Percent3.json")
    ai.train()


if __name__ == '__main__':
    test_mutation_rates()
