import pygame
import os
import glob
import random

class Cat(pygame.sprite.Sprite):
    def __init__(self, initial_position, images_right, images_left, speed=5):
        super().__init__()
        self.images_right = images_right
        self.images_left = images_left
        self.image = self.images_right[0]
        self.rect = self.image.get_rect(topleft=initial_position)
        self.speed = speed
        self.direction = "right"
        self.frame = 0

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = "left"
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = "right"
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Ограничение движения кота в пределах экрана
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))

        self.frame += 1

    def draw(self, screen):
        if self.direction == "right":
            screen.blit(self.images_right[self.frame % len(self.images_right)], self.rect.topleft)
        elif self.direction == "left":
            screen.blit(self.images_left[self.frame % len(self.images_left)], self.rect.topleft)


class Mouse(pygame.sprite.Sprite):
    def __init__(self, initial_position, images, speed=3):
        super().__init__()
        self.images = images
        self.image = self.images["right"][0]
        self.rect = self.image.get_rect(topleft=initial_position)
        self.speed = speed
        self.direction = "right"
        self.frame = 0

    def update(self):
        if random.randint(0, 100) < 10:  # случайное движение с вероятностью 10% каждый кадр
            self.direction = random.choice(["left", "right", "up", "down"])

        if self.direction == "left":
            if self.rect.x - self.speed >= 0:
                self.rect.x -= self.speed
        elif self.direction == "right":
            if self.rect.x + self.speed <= 800 - self.rect.width:
                self.rect.x += self.speed
        elif self.direction == "up":
            if self.rect.y - self.speed >= 0:
                self.rect.y -= self.speed
        elif self.direction == "down":
            if self.rect.y + self.speed <= 600 - self.rect.height:
                self.rect.y += self.speed

        self.frame += 1

    def draw(self, screen):
        screen.blit(self.images[self.direction][self.frame % len(self.images[self.direction])], self.rect.topleft)


class Game:
    def __init__(self):
        pygame.init()

        # Настройки экрана
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Игра Кот и Мышь")

        # Загрузка изображений
        self.load_images()

        # Создание игровых объектов
        self.cat = Cat((100, 100), self.cat_images_right, self.cat_images_left)
        self.mouse = Mouse((500, 500), self.mouse_images)

        # Игровые переменные
        self.game_paused = False
        self.game_over = False

        # Таймер
        self.clock = pygame.time.Clock()

        # Создание кнопок
        self.create_buttons()

    def load_images(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        animals_folder = os.path.join(current_directory, 'animals')

        cat_folder = os.path.join(animals_folder, 'cats_1')
        self.cat_images_right = self.load_images_from_folder(cat_folder, '0')
        self.cat_images_left = [pygame.transform.flip(img, True, False) for img in self.cat_images_right]

        mouse_folder = os.path.join(animals_folder, 'mouse')
        self.mouse_images = {
            "right": self.load_images_from_folder(mouse_folder, '0'),
            "left": [pygame.transform.flip(img, True, False) for img in self.load_images_from_folder(mouse_folder, '0')],
            "down": self.load_images_from_folder(mouse_folder, '1'),
            "up": self.load_images_from_folder(mouse_folder, '2')
        }

    def load_images_from_folder(self, folder, prefix, scale_factor=2):
        pattern = os.path.join(folder, f'{prefix}*.png')
        image_files = sorted(glob.glob(pattern))
        if not image_files:
            print(f"Изображения не найдены по пути: {pattern}")
        images = [pygame.transform.scale(pygame.image.load(img_file), 
                                          (pygame.image.load(img_file).get_width() * scale_factor, 
                                           pygame.image.load(img_file).get_height() * scale_factor)) 
                  for img_file in image_files]
        return images

    def create_buttons(self):
        # Кнопка "Начать заново"
        self.button_restart = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 10, 200, 50)
        self.button_restart_text = "Начать заново"

        # Кнопка "Выйти"
        self.button_quit = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 70, 200, 50)
        self.button_quit_text = "Выйти"

    def draw_pause_menu(self):
        # Отрисовка текста меню паузы
        font = pygame.font.Font(None, 36)
        text_paused = font.render("Пауза", True, (255, 255, 255))
        text_rect_paused = text_paused.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(text_paused, text_rect_paused)

        # Отрисовка кнопок
        pygame.draw.rect(self.screen, (0, 128, 255), self.button_restart)
        pygame.draw.rect(self.screen, (0, 128, 255), self.button_quit)

        font = pygame.font.Font(None, 28)
        text_restart = font.render(self.button_restart_text, True, (255, 255, 255))
        text_quit = font.render(self.button_quit_text, True, (255, 255, 255))

        self.screen.blit(text_restart, (self.button_restart.centerx - text_restart.get_width() // 2, self.button_restart.centery - text_restart.get_height() // 2))
        self.screen.blit(text_quit, (self.button_quit.centerx - text_quit.get_width() // 2, self.button_quit.centery - text_quit.get_height() // 2))

        pygame.display.flip()

    def draw_game_over(self):
        # Заливка полупрозрачным фоном
        self.screen.fill((255, 255, 255))  # Очищаем экран перед отрисовкой

        # Отрисовка текста экрана поражения
        font = pygame.font.Font(None, 36)
        text_game_over = font.render("Игра окончена", True, (255, 0, 0))  # Красный цвет для текста
        text_rect_game_over = text_game_over.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(text_game_over, text_rect_game_over)

        # Отрисовка кнопок
        pygame.draw.rect(self.screen, (0, 128, 255), self.button_restart)
        pygame.draw.rect(self.screen, (0, 128, 255), self.button_quit)

        font = pygame.font.Font(None, 28)
        text_restart = font.render(self.button_restart_text, True, (255, 255, 255))
        text_quit = font.render(self.button_quit_text, True, (255, 255, 255))

        self.screen.blit(text_restart, (self.button_restart.centerx - text_restart.get_width() // 2, self.button_restart.centery - text_restart.get_height() // 2))
        self.screen.blit(text_quit, (self.button_quit.centerx - text_quit.get_width() // 2, self.button_quit.centery - text_quit.get_height() // 2))

        pygame.display.flip()

    def restart_game(self):
        self.game_over = False
        self.game_paused = False
        self.cat.rect.topleft = (100, 100)
        self.mouse.rect.topleft = (500, 500)

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
                            self.restart_game()

                    elif event.key == pygame.K_r and self.game_over:
                        self.restart_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_over:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.button_restart.collidepoint(mouse_pos):
                            self.restart_game()
                        elif self.button_quit.collidepoint(mouse_pos):
                            running = False
                    elif self.game_paused:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.button_restart.collidepoint(mouse_pos):
                            self.restart_game()
                        elif self.button_quit.collidepoint(mouse_pos):
                            running = False

            if not self.game_paused and not self.game_over:
                keys = pygame.key.get_pressed()
                self.cat.update(keys)

                if pygame.sprite.collide_rect(self.cat, self.mouse):
                    self.game_over = True

                self.mouse.update()

                self.screen.fill((255, 255, 255))
                self.cat.draw(self.screen)
                self.mouse.draw(self.screen)
                pygame.display.flip()

                self.clock.tick(30)
            else:
                self.clock.tick(10)

            if self.game_over:
                self.draw_game_over()
            elif self.game_paused:
                self.draw_pause_menu()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
