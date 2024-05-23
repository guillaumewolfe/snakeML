import pygame
import sys
import os

class Menu:
    def __init__(self, screen_width=1200, screen_height=800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = self.initialize_pygame()
        self.font = self.initialize_font()
        self.small_font = self.initialize_font(size=20)
        self.title_text = self.font.render('ML Snake', True, (100, 100, 100))
        self.title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.manual_img = pygame.image.load('assets/manual.png').convert_alpha()
        self.ml_img = pygame.image.load('assets/ml.png').convert_alpha()
        self.manual_img = self.change_image_color(self.manual_img, (255, 255, 255, 128))  # Couleur plus pâle
        self.ml_img = self.change_image_color(self.ml_img, (255, 255, 255, 128))          # Couleur plus pâle
        self.resize_images()
        self.running = True

    def initialize_pygame(self):
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen_width = pygame.display.Info().current_w // 1.5
        self.screen_height = pygame.display.Info().current_h // 1.5
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game Menu')
        return screen

    def initialize_font(self, size=50):
        font_path = 'assets/RedditMono-Medium.ttf'
        try:
            font = pygame.font.Font(font_path, size)
            return font
        except Exception as e:
            print(f"Erreur lors du chargement de la police '{font_path}': {e}")
            sys.exit(1)

    def change_image_color(self, image, color):
        image = image.copy()
        image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return image

    def resize_images(self):
        self.manual_img = pygame.transform.scale(self.manual_img, (75, 75))
        self.ml_img = pygame.transform.scale(self.ml_img, (75, 75))

    def draw_menu(self):
        self.screen.fill((255, 255, 255))  # Remplir l'écran avec la couleur blanche
        self.screen.blit(self.title_text, self.title_rect)

        imageOffset = 10
        textOffset = 30
        manual_rect = self.manual_img.get_rect(center=(self.screen.get_width() // 3, self.screen.get_height() // 2 + imageOffset))
        ml_rect = self.ml_img.get_rect(center=(2 * self.screen.get_width() // 3, self.screen.get_height() // 2 + imageOffset))

        self.screen.blit(self.manual_img, manual_rect)
        self.screen.blit(self.ml_img, ml_rect)

        # Ajouter du texte sous les images
        manual_text = self.small_font.render('Manuel', True, (100, 100, 100))
        ml_text = self.small_font.render('Machine Learning', True, (100, 100, 100))

        manual_text_rect = manual_text.get_rect(center=(manual_rect.centerx, manual_rect.bottom + textOffset))
        ml_text_rect = ml_text.get_rect(center=(ml_rect.centerx, ml_rect.bottom + textOffset))

        self.screen.blit(manual_text, manual_text_rect)
        self.screen.blit(ml_text, ml_text_rect)

        pygame.display.flip()
        return manual_rect, ml_rect

    def handle_events(self, manual_rect, ml_rect):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if manual_rect.collidepoint(event.pos):
                    return 'manual'
                elif ml_rect.collidepoint(event.pos):
                    return 'ml'
        return None

    def run(self):
        while self.running:
            manual_rect, ml_rect = self.draw_menu()
            selection = self.handle_events(manual_rect, ml_rect)
            if selection:
                self.running = False
                return selection, self.screen_width, self.screen_height
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    menu = Menu()
    choice, screen_width, screen_height = menu.run()
    print(f"Choice: {choice}, Width: {screen_width}, Height: {screen_height}")
