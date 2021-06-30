import pygame

from snakegame import SnakeGame


def main():
    game = SnakeGame()

    # Game loop
    while not game.gameover:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return
        game.update(events)
        pygame.time.wait(1000 // 15)  # 15 fps

    game.display_gameover()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return


if __name__ == '__main__':
    main()
