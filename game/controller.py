# controller.py
import pygame
from game.snake import UP, DOWN, LEFT, RIGHT

class Controller:
    def __init__(self):
        self.direction = None

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = UP
            elif event.key == pygame.K_DOWN:
                self.direction = DOWN
            elif event.key == pygame.K_LEFT:
                self.direction = LEFT
            elif event.key == pygame.K_RIGHT:
                self.direction = RIGHT

    def get_direction(self):
        return self.direction
