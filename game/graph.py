import pygame

class Graph:
    def __init__(self, x, y, width, height, point_color, title_text, x_axis_text, y_axis_text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.point_color = point_color
        self.title_text = title_text
        self.x_axis_text = x_axis_text
        self.y_axis_text = y_axis_text
        self.data_x = []
        self.data_y = []
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 25)

    def update_data(self, data_x, data_y):
        self.data_x = data_x
        self.data_y = data_y

    def draw(self, screen):
        # Dessiner les axes
        pygame.draw.line(screen, (100, 100, 100), (self.x, self.y + self.height), (self.x + self.width * 1.10, self.y + self.height), 2)  # Axe X
        pygame.draw.line(screen, (100, 100, 100), (self.x, self.y - self.height * 0.1), (self.x, self.y + self.height), 2)  # Axe Y

        # Titre et labels des axes
        title_text = self.title_font.render(self.title_text, True, (100, 100, 100))
        screen.blit(title_text, (self.x + self.width // 2 - title_text.get_width() // 2, self.y - self.height * 0.20))

        x_label = self.font.render(self.x_axis_text, True, (100, 100, 100))
        screen.blit(x_label, (self.x + self.width // 2 - x_label.get_width() // 2, self.y + self.height + 10))

        y_label = self.font.render(self.y_axis_text, True, (100, 100, 100))
        y_label = pygame.transform.rotate(y_label, 90)
        screen.blit(y_label, (self.x - y_label.get_width() // 2 - 20, self.y + self.height // 2 - y_label.get_height() // 2))

        if not self.data_x or not self.data_y:
            return

        max_value = max(self.data_y) if self.data_y else 1

        if len(self.data_y) > 0:
            mean_value = sum(self.data_y) / len(self.data_y)
        else:
            mean_value = 0

        points = [
            (
                self.x + (self.width * (i / (len(self.data_x) - 1))) if len(self.data_x) > 1 else self.x + self.width // 2,
                self.y + self.height - (self.height * (y / max_value)) if max_value != 0 else self.y + self.height
            )
            for i, y in enumerate(self.data_y)
        ]

        if len(points) == 1:
            pygame.draw.circle(screen, self.point_color, (int(points[0][0]), int(points[0][1])), 3)
        else:
            for i in range(1, len(points)):
                pygame.draw.line(screen, self.point_color, points[i - 1], points[i], 1)

            for point in points:
                pygame.draw.circle(screen, self.point_color, (int(point[0]), int(point[1])), 3)

        # Annotations pour max et moyenne
        if max_value != 0:
            if max_value != mean_value:
                max_text = self.font.render(f'Max: {max_value}', True, (0, 0, 0))
                max_y_position = self.y + self.height - self.height * (max_value / max_value)
                screen.blit(max_text, (self.x + self.width + 10, max_y_position - max_text.get_height() // 2))
                pygame.draw.line(screen, (255, 0, 0), (self.x, max_y_position), (self.x + self.width, max_y_position), 1)

                mean_text = self.font.render(f'Mean: {mean_value:.2f}', True, (0, 0, 0))
                mean_y_position = self.y + self.height - self.height * (mean_value / max_value)
                screen.blit(mean_text, (self.x + self.width + 10, mean_y_position - mean_text.get_height() // 2))
                pygame.draw.line(screen, (0, 255, 0), (self.x, mean_y_position), (self.x + self.width, mean_y_position), 1)
            else:
                max_text = self.font.render(f'Max/Mean: {max_value}', True, (0, 0, 0))
                max_y_position = self.y + self.height - self.height * (max_value / max_value)
                screen.blit(max_text, (self.x + self.width + 10, max_y_position - max_text.get_height() // 2))
                pygame.draw.line(screen, (255, 0, 0), (self.x, max_y_position), (self.x + self.width, max_y_position), 1)
