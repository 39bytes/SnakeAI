import pygame

from constants import *


class Renderer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SnakeAI")
        self.screen = pygame.display.set_mode(
            (SIZE * 5, SIZE * 2))  # Display 10 snakes
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.fps = DEFAULT_FPS
    
    def get_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # Speed up or slow down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.fps + 10 <= MAX_FPS:
                    self.fps += 10
                if event.key == pygame.K_DOWN and self.fps >= 10:  # min 5 fps
                    self.fps -= 10
    
    def draw(self, games):
        # For offsetting each correctly in order to draw them in a 5x2 grid
        xOffset = 0
        yOffset = 0
        self.get_input()
        self.background.fill((0, 0, 0))
        self.screen.blit(self.background, (0, 0))

        for num, game in enumerate(games):
            if num < 10:  # Only displaying the first 10 snakes
                # White grid lines
                pygame.draw.rect(self.background, (255, 255, 255),
                                 (xOffset * SIZE, yOffset * SIZE, SIZE, SIZE), width=1)
                if game.gameover:  # Draw black screen if dead
                    pygame.draw.rect(self.background, (0, 0, 0),
                                     (xOffset * SIZE + 1, yOffset * SIZE + 1, SIZE - 1, SIZE - 1))
                    xOffset += 1
                    if xOffset == 5:
                        xOffset = 0
                        yOffset += 1
                    continue # No need to draw the snake/continue updating
                
                # Draw the snake
                for segment in game.snake.body:
                    pygame.draw.rect(self.background, (255, 255, 255),
                                     (xOffset * SIZE + segment.x * SCALE + 1,
                                     yOffset * SIZE + segment.y * SCALE + 1,
                                     SCALE - 1, SCALE - 1))

                # Draw the apple
                pygame.draw.rect(self.background, (255, 0, 0),
                                 (xOffset * SIZE + game.apple.x * SCALE + 1,
                                 yOffset * SIZE + game.apple.y * SCALE + 1,
                                 SCALE - 1, SCALE - 1))

                xOffset += 1
                if xOffset == 5:
                    xOffset = 0
                    yOffset += 1
        
        # Blits everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()
        pygame.time.wait(1000 // self.fps)
