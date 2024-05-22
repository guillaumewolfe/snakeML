# snake.py
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self, positions, speed):
        self.positions = positions
        self.direction = RIGHT
        self.speed = speed

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def update(self):
        new_head = (self.positions[0][0] + self.direction[0], self.positions[0][1] + self.direction[1])
        self.positions = [new_head] + self.positions[:-1]

    def grow(self):
        self.positions.append(self.positions[-1])

    def check_collision(self, frame_x, frame_y, frame_width, frame_height, cell_size):
        head_x, head_y = self.positions[0]

        # Check collision with walls
        if (head_x < 0 or 
            head_y < 0 or
            head_x >= frame_width // cell_size or
            head_y >= frame_height // cell_size):
            return True

        # Check collision with itself
        if self.positions[0] in self.positions[1:]:
            return True

        return False
