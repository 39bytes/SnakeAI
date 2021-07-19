from snakeai import SnakeAI


def test_mutation_rates():  # Tests 1%, 2%, 3%, and 5% mutation rates
    for i in range(1, 4):
        ai = SnakeAI(0.01, f"snakesCopyCross1Percent{i}.json",
                     f"scoresCopyCross1Percent{i}.json")
        ai.train()

        ai = SnakeAI(0.02, f"snakesCopyCross2Percent{i}.json",
                     f"scoresCopyCross2Percent{i}.json")
        ai.train()

        ai = SnakeAI(0.03, f"snakesCopyCross3Percent{i}.json",
                     f"scoresCopyCross3Percent{i}.json")
        ai.train()

        ai = SnakeAI(0.05, f"snakesCopyCross5Percent{i}.json",
                     f"scoresCopyCross5Percent{i}.json")
        ai.train()


if __name__ == '__main__':
    test_mutation_rates()
