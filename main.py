import pygame
import os
import glob
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Игра Кот и Мышь")
        
        self.clock = pygame.time.Clock()
        self.frame = 0
        self.game_paused = False
        self.game_over = False
        
        self.load_assets()
        self.setup_objects()
        
    def load_assets(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        animals_folder = os.path.join(current_directory, 'animals')
        
        # Загрузка изображений кота
        cat_folder = os.path.join(animals_folder, 'cats_1')
        self.cat_images_right = self.load_images(cat_folder, '0')
        if not self.cat_images_right:
            raise FileNotFoundError("Изображения кота не найдены")
        self.cat_images_left = [pygame.transform.flip(img, True, False) for img in self.cat_images_right]
        
        # Загрузка изображений мыши
        mouse_folder = os.path.join(animals_folder, 'mouse')
        self.mouse_images = {
            "right": self.load_images(mouse_folder, '0'),
            "left": [pygame.transform.flip(img, True, False) for img in self.load_images(mouse_folder, '0')],
            "down": self.load_images(mouse_folder, '1'),
            "up": self.load_images(mouse_folder, '2')
        }
        if not all(self.mouse_images.values()):
            raise FileNotFoundError("Изображения мыши не найдены")
        
    def setup_objects(self):
        # Настройка кота
        self.cat_rect = self.cat_images_right[0].get_rect(topleft=(100, 100))
        self.cat_direction = "right"
        
        # Настройка мыши
        self.mouse_rect = self.mouse_images["right"][0].get_rect(topleft=(500, 500))
        self.mouse_direction = "right"
        
    def load_images(self, folder, prefix, scale_factor=2):
        pattern = os.path.join(folder, f'{prefix}*.png')
        image_files = sorted(glob.glob(pattern))
        if not image_files:
            print(f"Изображения не найдены по пути: {pattern}")
        images = [pygame.transform.scale(pygame.image.load(img_file), 
                                         (pygame.image.load(img_file).get_width() * scale_factor, 
                                          pygame.image.load(img_file).get_height() * scale_factor)) 
                  for img_file in image_files]
        return images
    
    def draw_cat(self):
        if self.cat_direction == "right":
            self.screen.blit(self.cat_images_right[self.frame % len(self.cat_images_right)], self.cat_rect.topleft)
        elif self.cat_direction == "left":
            self.screen.blit(self.cat_images_left[self.frame % len(self.cat_images_left)], self.cat_rect.topleft)
    
    def draw_mouse(self):
        self.screen.blit(self.mouse_images[self.mouse_direction][self.frame % len(self.mouse_images[self.mouse_direction])], self.mouse_rect.topleft)
    
    def move_cat(self, keys):
        if keys[pygame.K_LEFT]:
            self.cat_rect.x -= 5
            self.cat_direction = "left"
        if keys[pygame.K_RIGHT]:
            self.cat_rect.x += 5
            self.cat_direction = "right"
        if keys[pygame.K_UP]:
            self.cat_rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.cat_rect.y += 5
        
        # Ограничение движения кота в пределах экрана
        self.cat_rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))
    
    def move_mouse(self):
        if random.randint(0, 100) < 10:
            self.mouse_direction = random.choice(["left", "right", "up", "down"])
        
        if self.mouse_direction == "left":
            self.mouse_rect.x -= 3
        elif self.mouse_direction == "right":
            self.mouse_rect.x += 3
        elif self.mouse_direction == "up":
            self.mouse_rect.y -= 3
        elif self.mouse_direction == "down":
            self.mouse_rect.y += 3
        
        self.mouse_rect.clamp_ip(pygame.Rect(0, 0, self.screen_width, self.screen_height))
    
    def draw_pause_menu(self):
        # Заливка полупрозрачным фоном
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)  # Прозрачность 50%
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Отрисовка текста меню паузы
        font = pygame.font.Font(None, 36)
        text_paused = font.render("Пауза", True, (255, 255, 255))
        text_rect_paused = text_paused.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(text_paused, text_rect_paused)

        # Отрисовка кнопок меню паузы
        button_continue = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2, 200, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), button_continue)
        text_continue = font.render("Продолжить", True, (0, 0, 0))
        text_rect_continue = text_continue.get_rect(center=button_continue.center)
        self.screen.blit(text_continue, text_rect_continue)

        button_restart = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 60, 200, 50)
        pygame.draw.rect(self.screen, (255, 255, 0), button_restart)
        text_restart = font.render("Начать заново", True, (0, 0, 0))
        text_rect_restart = text_restart.get_rect(center=button_restart.center)
        self.screen.blit(text_restart, text_rect_restart)

        pygame.display.flip()

        self.pause_buttons = (button_continue, button_restart)
    
    def draw_game_over(self):
        # Заливка полупрозрачным фоном
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(128)  # Прозрачность 50%
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Отрисовка текста экрана поражения
        font = pygame.font.Font(None, 36)
        text_game_over = font.render("Игра окончена", True, (255, 255, 255))
        text_rect_game_over = text_game_over.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(text_game_over, text_rect_game_over)

        # Отрисовка кнопок экрана поражения
        button_restart = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2, 200, 50)
        pygame.draw.rect(self.screen, (255, 255, 0), button_restart)
        text_restart = font.render("Начать заново", True, (0, 0, 0))
        text_rect_restart = text_restart.get_rect(center=button_restart.center)
        self.screen.blit(text_restart, text_rect_restart)

        button_quit = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 60, 200, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), button_quit)
        text_quit = font.render("Закончить", True, (0, 0, 0))
        text_rect_quit = text_quit.get_rect(center=button_quit.center)
        self.screen.blit(text_quit, text_rect_quit)

        pygame.display.flip()

        self.restart_button = button_restart
        self.quit_button = button_quit
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if not self.game_over:
                            self.game_paused = not self.game_paused
                            if self.game_paused:
                                self.draw_pause_menu()
                            else:
                                pygame.mouse.set_visible(False)
                                pygame.event.set_grab(True)
                        else:
                            self.game_over = False
                            self.mouse_rect.topleft = (500, 500)
                            self.cat_rect.topleft = (100, 100)
                            self.frame = 0

                    elif event.key == pygame.K_r and self.game_over:
                        self.game_over = False
                        self.mouse_rect.topleft = (500, 500)
                        self.cat_rect.topleft = (100, 100)
                        self.frame = 0

                    elif event.key == pygame.K_RETURN:
                        if self.game_paused:
                            mouse_pos = pygame.mouse.get_pos()
                            if self.pause_buttons[0].collidepoint(mouse_pos):  # кнопка "Продолжить"
                                self.game_paused = False
                                pygame.mouse.set_visible(False)
                                pygame.event.set_grab(True)
                            elif self.pause_buttons[1].collidepoint(mouse_pos):  # кнопка "Начать заново"
                                self.game_paused = False
                                pygame.mouse.set_visible(False)
                                pygame.event.set_grab(True)
                                self.mouse_rect.topleft = (500, 500)
                                self.cat_rect.topleft = (100, 100)
                                self.frame = 0

                        elif self.game_over:
                            mouse_pos = pygame.mouse.get_pos()
                            if self.restart_button.collidepoint(mouse_pos):  # кнопка "Начать заново"
                                self.game_over = False
                                self.mouse_rect.topleft = (500, 500)
                                self.cat_rect.topleft = (100, 100)
                                self.frame = 0
                            elif self.quit_button.collidepoint(mouse_pos):  # кнопка "Закончить"
                                running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_paused:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.pause_buttons[0].collidepoint(mouse_pos):  # кнопка "Продолжить"
                        self.game_paused = False
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                    elif self.pause_buttons[1].collidepoint(mouse_pos):  # кнопка "Начать заново"
                        self.game_paused = False
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                        self.mouse_rect.topleft = (500, 500)
                        self.cat_rect.topleft = (100, 100)
                        self.frame = 0
            
            if not self.game_paused:
                keys = pygame.key.get_pressed()
                self.move_cat(keys)
                
                if self.cat_rect.colliderect(self.mouse_rect):
                    self.game_over = True
                
                self.move_mouse()
                
                self.screen.fill((255, 255, 255))
                self.draw_cat()
                self.draw_mouse()
                pygame.display.flip()
                
                self.clock.tick(30)
                self.frame += 1
            else:
                self.clock.tick(10)
            
            if self.game_over:
                pygame.mouse.set_visible(True)
                pygame.event.set_grab(False)
                self.draw_game_over()
                self.game_paused = True
        
        pygame.quit()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
