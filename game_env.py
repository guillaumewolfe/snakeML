import pygame
import sys
from game.snake import Snake, UP, DOWN, LEFT, RIGHT
from game.controller import Controller
from game.reward import Reward
from game.graph import Graph  # Importer la classe Graph
from state_representation.state import get_state

NUMBER_OF_SQUARES_HORIZONTAL = 30
RECTANGLE_FRAME_SIZE = 5
SNAKE_COLOR = (150, 150, 150)  # Gris pâle
REWARD_COLOR = (255, 100, 100)

class SnakeGameEnv:
    def __init__(self, user_control=True, initial_speed=5, screen_width=1200, screen_height=800):
        self.user_control = user_control
        self.snake_initial_speed = initial_speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.frame_offset_x = screen_width * 0.2  # Décalage pour déplacer le jeu à gauche
        self.score = 0
        self.list_of_scores = []
        self.screen = self.initialize_pygame()
        self.font = self.initialize_font()
        self.fontScore = self.initialize_font(20)
        self.graph = Graph(self.screen_width - self.frame_offset_x -100, self.screen_height/2, self.screen_height/4, self.screen_height/4, (150, 150, 150), "Score", "Episodes", "Score")

        self.controller = Controller()
        self.last_update_time = pygame.time.get_ticks()
        self.reset(shouldAppend = False)


    def initialize_pygame(self):
        pygame.init()
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        return screen

    def initialize_font(self, size=30):
        font_path = 'assets/RedditMono-Medium.ttf'
        font_size = size
        try:
            font = pygame.font.Font(font_path, font_size)
            return font
        except Exception as e:
            print(f"Erreur lors du chargement de la police '{font_path}': {e}")
            sys.exit(1)

    def draw_game_frame(self):
        frame_color = (100, 100, 100)  # Gris foncé
        frame_thickness = RECTANGLE_FRAME_SIZE

        # Dimensions du cadre
        frameBuffer_Y = self.screen.get_height() // 15
        frame_height = self.screen.get_height() * 2 / 3
        frame_width = frame_height
        frame_x = (self.screen.get_width() - frame_width) // 2 - self.frame_offset_x
        frame_y = (self.screen.get_height() - frame_height - frameBuffer_Y)

        # Dessiner le rectangle du cadre
        pygame.draw.rect(self.screen, frame_color, (frame_x, frame_y, frame_width, frame_height), frame_thickness)
        
        return frame_x, frame_y, frame_width, frame_height

    def draw_grid(self, frame_x, frame_y, frame_width, frame_height):
        color1 = (255, 255, 255)  # Blanc
        color2 = (225, 225, 225)  # Gris pâle

        frame_thickness = RECTANGLE_FRAME_SIZE
        
        # Taille des cellules carrées ajustée pour s'adapter parfaitement au cadre
        cell_size = (frame_width) // NUMBER_OF_SQUARES_HORIZONTAL
        rows = int(frame_height // cell_size)

        offset_x = frame_thickness / 2
        offset_y = frame_thickness / 2

        for row in range(rows):
            for col in range(NUMBER_OF_SQUARES_HORIZONTAL):
                color = color1 if (row + col) % 2 == 0 else color2
                pygame.draw.rect(self.screen, color, (frame_x + offset_x + col * cell_size, frame_y + offset_y + row * cell_size, cell_size, cell_size))

    def draw_snake(self, snake_positions, cell_size, frame_x, frame_y, offset_x, offset_y):
        for position in snake_positions:
            pygame.draw.rect(self.screen, SNAKE_COLOR, (frame_x + offset_x + position[0] * cell_size, frame_y + offset_y + position[1] * cell_size, cell_size, cell_size))

    def draw_game_over(self):
        game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, game_over_rect)

    def draw_score(self, score):
        score_text = self.fontScore.render(f'Score: {score}', True, (100, 100, 100))
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2 - self.frame_offset_x, self.screen.get_height() / 5))
        self.screen.blit(score_text, score_rect)

    def reset(self, shouldAppend = True):
        self.snake_positions = [(17, 15), (16, 15), (15, 15)]  # Initialisation du serpent
        self.snake_speed = self.snake_initial_speed
        self.snake = Snake(self.snake_positions, self.snake_speed)

        frame_x, frame_y, frame_width, frame_height = self.draw_game_frame()
        cell_size = (frame_width) // NUMBER_OF_SQUARES_HORIZONTAL
        self.reward = Reward(frame_x, frame_y, frame_width, frame_height, cell_size, self.snake_positions)
        if shouldAppend:
            self.list_of_scores.append(self.score)
        self.score = 0
        self.game_over = False
        self.update_graph()
        return self.get_state()

    def get_state(self):
        frame_x, frame_y, frame_width, frame_height = self.draw_game_frame()
        cell_size = (frame_width) // NUMBER_OF_SQUARES_HORIZONTAL
        state = get_state(self.snake.positions, self.reward.position, frame_x, frame_y, frame_width, frame_height, cell_size)
        return state

    def step(self, action):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update_time > 1000 // self.snake.speed:
            if action is not None:
                self.snake.change_direction(action)
            self.snake.update()
            self.last_update_time = current_time

            frame_x, frame_y, frame_width, frame_height = self.draw_game_frame()
            cell_size = (frame_width) // NUMBER_OF_SQUARES_HORIZONTAL

            reward_value = -0.1  # Récompense légèrement négative pour chaque mouvement

            # Vérifier les collisions
            if self.snake.check_collision(frame_x, frame_y, frame_width, frame_height, cell_size):
                reward_value = -100  # Récompense négative pour collision
                self.game_over = True

            # Vérifier si le serpent mange la récompense
            if self.snake.positions[0] == self.reward.position:
                self.snake.grow()
                reward_value = 10  # Récompense positive pour manger une pomme
                self.reward = Reward(frame_x, frame_y, frame_width, frame_height, cell_size, self.snake.positions)
                self.score += 1

            return self.get_state(), reward_value, self.game_over
        else:
            return self.get_state(), 0, self.game_over

    def render(self):
        self.screen.fill((255, 255, 255))  # Remplir l'écran avec la couleur blanche
        title_text = self.font.render('ML Snake', True, (100, 100, 100))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(title_text, title_rect)

        self.draw_score(self.score)
        if not self.game_over:
            frame_x, frame_y, frame_width, frame_height = self.draw_game_frame()
            cell_size = (frame_width) // NUMBER_OF_SQUARES_HORIZONTAL
            self.draw_snake(self.snake.positions, cell_size, frame_x, frame_y, RECTANGLE_FRAME_SIZE / 2, RECTANGLE_FRAME_SIZE / 2)
            self.reward.draw(self.screen, REWARD_COLOR, RECTANGLE_FRAME_SIZE / 2)

        if self.game_over:
            self.draw_game_over()

        self.graph.draw(self.screen)  # Dessiner le graphique
        pygame.display.flip()   # Mettre à jour l'affichage

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.user_control and not self.game_over:
                self.controller.handle_event(event)
            elif self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.reset()

    def update_graph(self):
        data_x = list(range(len(self.list_of_scores)))
        data_y = self.list_of_scores
        self.graph.update_data(data_x, data_y)
