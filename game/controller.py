# controller.py
import pygame
from game.snake import UP, DOWN, LEFT, RIGHT

class Controller:
    def __init__(self):
        self.direction = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.direction = UP
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.direction = DOWN
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.direction = LEFT
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.direction = RIGHT

    def get_direction(self):
        return self.direction
