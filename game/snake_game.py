import pygame
import sys
import matplotlib.pyplot as plt
from game.snake import Snake, UP, DOWN, LEFT, RIGHT
from game.controller import Controller
from game.reward import Reward
from state_representation.state import get_state

NUMBER_OF_SQUARES_HORIZONTAL = 30
RECTANGLE_FRAME_SIZE = 5
SNAKE_COLOR = (150, 150, 150)  # Gris pâle
REWARD_COLOR = (255, 100, 100)

def initialize_pygame():
    pygame.init()
    infoObject = pygame.display.Info()
    screen_width = infoObject.current_w // 1.5
    screen_height = infoObject.current_h // 1.5
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Snake Game')
    return screen

def initialize_font():
    font_path = 'assets/RedditMono-Medium.ttf'
    font_size = 30
    try:
        font = pygame.font.Font(font_path, font_size)
        print(f"Police '{font_path}' chargée avec succès.")
        return font
    except Exception as e:
        print(f"Erreur lors du chargement de la police '{font_path}': {e}")
        sys.exit(1)

def draw_game_frame(screen):
    frame_color = (100, 100, 100)  # Gris foncé
    frame_thickness = RECTANGLE_FRAME_SIZE

    # Dimensions du cadre
    frameBuffer_Y = screen.get_height() // 15
    frame_height = screen.get_height() * 2 / 3
    frame_width = frame_height
    frame_x = (screen.get_width() - frame_width) // 2
    frame_y = (screen.get_height() - frame_height - frameBuffer_Y)

    # Dessiner le rectangle du cadre
    pygame.draw.rect(screen, frame_color, (frame_x, frame_y, frame_width, frame_height), frame_thickness)
    
    return frame_x, frame_y, frame_width, frame_height

def draw_grid(screen, frame_x, frame_y, frame_width, frame_height, nbre_squares_horizontal):
    color1 = (255, 255, 255)  # Blanc
    color2 = (225, 225, 225)  # Gris pâle

    frame_thickness = RECTANGLE_FRAME_SIZE
    
    # Taille des cellules carrées ajustée pour s'adapter parfaitement au cadre
    cell_size = (frame_width) // nbre_squares_horizontal
    rows = int(frame_height // cell_size)

    offset_x = frame_thickness / 2
    offset_y = frame_thickness / 2

    for row in range(rows):
        for col in range(nbre_squares_horizontal):
            color = color1 if (row + col) % 2 == 0 else color2
            pygame.draw.rect(screen, color, (frame_x + offset_x + col * cell_size, frame_y + offset_y + row * cell_size, cell_size, cell_size))

def draw_snake(screen, snake_positions, cell_size, frame_x, frame_y, offset_x, offset_y):
    for position in snake_positions:
        pygame.draw.rect(screen, SNAKE_COLOR, (frame_x + offset_x + position[0] * cell_size, frame_y + offset_y + position[1] * cell_size, cell_size, cell_size))

def draw_game_over(screen, font):
    game_over_text = font.render('Game Over', True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(game_over_text, game_over_rect)

def draw_score(screen, font, score):
    score_text = font.render(f'Score: {score}', True, (100, 100, 100))
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, screen.get_height() / 5))
    screen.blit(score_text, score_rect)

def reset_game(snake, reward, frame_x, frame_y, frame_width, frame_height, cell_size):
    snake.positions = [(17, 15), (16, 15), (15, 15)]
    snake.direction = RIGHT
    reward.position = reward.random_position(snake.positions)
    return 0, False


def main(USER_CONTROL, SNAKE_INITIAL_SPEED):
    screen = initialize_pygame()
    clock = pygame.time.Clock()

    font = initialize_font()
    
    title_text = font.render('ML Snake', True, (100, 100, 100))
    title_rect = title_text.get_rect(center=(screen.get_width() // 2, 50))

    # Initialisation du serpent (positions des segments)
    snake_positions = [(17, 15), (16, 15), (15, 15)]  # Par exemple, trois segments horizontaux
    snake_speed = SNAKE_INITIAL_SPEED  # Vitesse du serpent en ticks par seconde
    snake = Snake(snake_positions, snake_speed)

    # Initialisation de la récompense
    frame_x, frame_y, frame_width, frame_height = draw_game_frame(screen)
    cell_size = (frame_width) // NUMBER_OF_SQUARES_HORIZONTAL
    reward = Reward(frame_x, frame_y, frame_width, frame_height, cell_size, snake_positions)

    # Choisissez le contrôleur (utilisateur ou ML)
    user_control = USER_CONTROL
    controller = Controller()

    score = 0
    last_update_time = pygame.time.get_ticks()
    scores = []
    rewards = []
    
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif user_control and not game_over:
                controller.handle_event(event)
            elif game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                score, game_over = reset_game(snake, reward, frame_x, frame_y, frame_width, frame_height, cell_size)
                scores.append(score)
                rewards.append(reward_value)

        if not game_over:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time > 1000 // snake.speed:
                state = get_state(snake.positions, reward.position, frame_x, frame_y, frame_width, frame_height, cell_size)
                if user_control:
                    direction = controller.get_direction()
                else:
                    state = None  # Remplacez par l'état actuel du jeu
                    direction = controller.get_direction(state)
                if direction:
                    snake.change_direction(direction)
                snake.update()
                last_update_time = current_time

                # Vérifier les collisions
                if snake.check_collision(frame_x, frame_y, frame_width, frame_height, cell_size):
                    reward_value = -100  # Récompense négative pour collision
                    game_over = True

                # Vérifier si le serpent mange la récompense
                if snake.positions[0] == reward.position:
                    snake.grow()
                    reward_value = 10  # Récompense positive pour manger une pomme
                    reward = Reward(frame_x, frame_y, frame_width, frame_height, cell_size, snake.positions)
                    score += 1
                else:
                    reward_value = -0.1  # Récompense légèrement négative pour chaque mouvement
                
                rewards.append(reward_value)

        screen.fill((255, 255, 255))  # Remplir l'écran avec la couleur blanche
        screen.blit(title_text, title_rect)
        
        draw_score(screen, font, score)
        if not game_over:
            draw_game_frame(screen)
            draw_snake(screen, snake.positions, cell_size, frame_x, frame_y, RECTANGLE_FRAME_SIZE / 2, RECTANGLE_FRAME_SIZE / 2)
            reward.draw(screen, REWARD_COLOR, RECTANGLE_FRAME_SIZE / 2)

        if game_over:
            draw_game_over(screen, font)

        pygame.display.flip()   # Mettre à jour l'affichage
        clock.tick(60)          # Limiter à 60 images par seconde

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
