from game_env import SnakeGameEnv
import pygame
import sys
from menu import Menu

def main():
    menu = Menu()
    choice, screen_width, screen_height = menu.run()
    initialSpeed = 10
    user_control = True if choice == 'manual' else False
    env = SnakeGameEnv(user_control=user_control, initial_speed = initialSpeed, screen_width=screen_width, screen_height=screen_height)
    clock = pygame.time.Clock()
    
    while True:
        env.handle_events()
        if not env.game_over:
            action = env.controller.get_direction() if env.user_control else None  # Remplacer par le modèle pour le ML
            state, reward, done = env.step(action)
        env.render()
        clock.tick(60)  # Limiter à 60 images par seconde

if __name__ == "__main__":
    main()
