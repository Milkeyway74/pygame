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

        pygame.display.flip()

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

        pygame.display.flip()

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
                            self.game_over = False
                            self.cat.rect.topleft = (100, 100)
                            self.mouse.rect.topleft = (500, 500)

                    elif event.key == pygame.K_r and self.game_over:
                        self.game_over = False
                        self.cat.rect.topleft = (100, 100)
                        self.mouse.rect.topleft = (500, 500)

            if not self.game_paused:
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

                while self.game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.game_over = False
                                self.cat.rect.topleft = (100, 100)
                                self.mouse.rect.topleft = (500, 500)
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            self.game_over = False
                            self.cat.rect.topleft = (100, 100)
                            self.mouse.rect.topleft = (500, 500)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
