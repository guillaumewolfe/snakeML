# reward.py
import random
import pygame

class Reward:
    def __init__(self, frame_x, frame_y, frame_width, frame_height, cell_size, snake_positions):
        self.cell_size = cell_size
        self.frame_x = frame_x
        self.frame_y = frame_y
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.position = self.random_position(snake_positions)

    def random_position(self, snake_positions):
        columns = self.frame_width // self.cell_size
        rows = self.frame_height // self.cell_size
        position = (random.randint(0, columns - 1), random.randint(0, rows - 1))
        while position in snake_positions:
            position = (random.randint(0, columns - 1), random.randint(0, rows - 1))
        return position

    def draw(self, screen, color, frame_offset):
        
        pygame.draw.rect(screen, color, (self.frame_x + frame_offset + self.position[0] * self.cell_size, self.frame_y + frame_offset + self.position[1] * self.cell_size, self.cell_size, self.cell_size))