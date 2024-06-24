import pygame
import os
import glob
#import random

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

    def update(self, keys, walls):
        old_rect = self.rect.copy()
        
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
        self.rect.x = max(0, min(self.rect.x, 800 - self.rect.width + 10))
        self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height + 10))

        # Проверка коллизии с непроходимыми стенами
        for wall in walls:
            if wall.blocking and self.rect.colliderect(wall.rect):
                self.rect = old_rect
                break

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

    '''def update(self, cat_rect, walls):
        old_rect = self.rect.copy()

        if random.randint(0, 100) < 10:  # случайное движение с вероятностью 10% каждый кадр
            self.direction = random.choice(["left", "right", "up", "down"])

        if self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed

        # Проверка коллизии с непроходимыми стенами
        for wall in walls:
            if wall.blocking and self.rect.colliderect(wall.rect):
                self.rect = old_rect
                break

        self.frame += 1'''
      
    def update(self, cat_x, cat_y, walls):
        # Вычисляем расстояние по осям X и Y
        dx = self.rect.x - cat_x
        dy = self.rect.y - cat_y
        speed = self.speed
        old_rect = self.rect.copy()

        for wall in walls:
            if wall.blocking and self.rect.colliderect(wall.rect):
                self.rect = old_rect
                break

        #if (self.rect.x == 0 or self.rect.x == 800 - self.rect.width - 10) and (
        #    self.rect.y == 0 or self.rect.y == 600 - self.rect.height - 10):
        #    dx = - dx
        #    dy = -dy

        # Разворачиваем при попадании в угол
        if self.rect.right + speed >= 800:
            speed = -speed
        if self.rect.left + speed <= 0:
            speed = -speed
        if self.rect.bottom + speed >= 600:
            speed = -speed
        if self.rect.top + speed <= 0:
            speed = -speed


        # Определяем направление движения
        if abs(dx) > abs(dy):
            if dx < 0:
                self.rect.x -= speed
            else:
                self.rect.x += speed
        else:
            if dy < 0:
                self.rect.y -= speed
            else:
                self.rect.y += speed
        
        self.frame += 1
        
        # Ограничение движения по краям экрана
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(800 - self.rect.width, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(600 - self.rect.height, self.rect.y)
        
    def draw(self, screen):
        screen.blit(self.images[self.direction][self.frame % len(self.images[self.direction])], self.rect.topleft)


class Wall(pygame.sprite.Sprite):
    def __init__(self, position, image, blocking=True):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=position)
        self.blocking = blocking


class Game:
    def __init__(self):
        pygame.init()

        # Настройки экрана
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Catch me if you can")

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

        # Создание стен и пола
        self.create_walls_and_floor()


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

        walls_folder = os.path.join(current_directory, 'images', 'furniture', 'walls')
        self.wall_images = {
            "high": pygame.image.load(os.path.join(walls_folder, 'high.png')),
            "left_high_corner": pygame.image.load(os.path.join(walls_folder, 'left_high_corner.png')),
            "left_low_corner": pygame.image.load(os.path.join(walls_folder, 'left_low_corner.png')),
            "left": pygame.image.load(os.path.join(walls_folder, 'left.png')),
            "low": pygame.image.load(os.path.join(walls_folder, 'low.png')),
            "right_high_corner": pygame.image.load(os.path.join(walls_folder, 'right_high_corner.png')),
            "right_low_corner": pygame.image.load(os.path.join(walls_folder, 'right_low_corner.png')),
            "right": pygame.image.load(os.path.join(walls_folder, 'right.png')),
            "middle": pygame.image.load(os.path.join(walls_folder, 'middle.png'))
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

    def create_walls_and_floor(self):
        self.walls = []
        tile_size = self.wall_images["middle"].get_width()

        # Создаем границы стен
        for y in range(0, self.screen_height, tile_size):
            self.walls.append(Wall((0, y), self.wall_images["left"]))
            self.walls.append(Wall((self.screen_width - tile_size, y), self.wall_images["right"]))

        for x in range(0, self.screen_width, tile_size):
            self.walls.append(Wall((x, 0), self.wall_images["high"]))
            self.walls.append(Wall((x, self.screen_height - tile_size), self.wall_images["low"]))

        # Углы стен
        self.walls.append(Wall((0, 0), self.wall_images["left_high_corner"]))
        self.walls.append(Wall((0, self.screen_height - tile_size), self.wall_images["left_low_corner"]))
        self.walls.append(Wall((self.screen_width - tile_size, 0), self.wall_images["right_high_corner"]))
        self.walls.append(Wall((self.screen_width - tile_size, self.screen_height - tile_size), self.wall_images["right_low_corner"]))

        # Создаем пол
        for x in range(tile_size, self.screen_width - tile_size, tile_size):
            for y in range(tile_size, self.screen_height - tile_size, tile_size):
                self.walls.append(Wall((x, y), self.wall_images["middle"], blocking=False))

    def draw_pause_menu(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Пауза", True, (255, 255, 255))
        self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - text.get_height() // 2))

        pygame.draw.rect(self.screen, (0, 0, 0), self.button_restart)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_quit)

        text_restart = font.render(self.button_restart_text, True, (255, 255, 255))
        text_quit = font.render(self.button_quit_text, True, (255, 255, 255))

        self.screen.blit(text_restart, (self.button_restart.x + (self.button_restart.width - text_restart.get_width()) // 2,
                                        self.button_restart.y + (self.button_restart.height - text_restart.get_height()) // 2))
        self.screen.blit(text_quit, (self.button_quit.x + (self.button_quit.width - text_quit.get_width()) // 2,
                                     self.button_quit.y + (self.button_quit.height - text_quit.get_height()) // 2))

    def draw_game_over_menu(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Игра окончена!", True, (255, 0, 0))
        self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, self.screen_height // 2 - text.get_height() // 2))

        pygame.draw.rect(self.screen, (0, 0, 0), self.button_restart)
        pygame.draw.rect(self.screen, (0, 0, 0), self.button_quit)

        text_restart = font.render(self.button_restart_text, True, (255, 255, 255))
        text_quit = font.render(self.button_quit_text, True, (255, 255, 255))

        self.screen.blit(text_restart, (self.button_restart.x + (self.button_restart.width - text_restart.get_width()) // 2,
                                        self.button_restart.y + (self.button_restart.height - text_restart.get_height()) // 2))
        self.screen.blit(text_quit, (self.button_quit.x + (self.button_quit.width - text_quit.get_width()) // 2,
                                     self.button_quit.y + (self.button_quit.height - text_quit.get_height()) // 2))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.game_over:
                    self.game_paused = not self.game_paused
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_paused:
                    if self.button_restart.collidepoint(event.pos):
                        self.reset_game()
                    elif self.button_quit.collidepoint(event.pos):
                        pygame.quit()
                        quit()
                elif self.game_over:
                    if self.button_restart.collidepoint(event.pos):
                        self.reset_game()
                    elif self.button_quit.collidepoint(event.pos):
                        pygame.quit()
                        quit()

    def reset_game(self):
        self.cat = Cat((100, 100), self.cat_images_right, self.cat_images_left)
        self.mouse = Mouse((500, 500), self.mouse_images)
        self.game_paused = False
        self.game_over = False

    def run_game(self):
        while True:
            self.handle_events()

            if not self.game_paused and not self.game_over:
                keys = pygame.key.get_pressed()
                self.cat.update(keys, self.walls)
                #self.mouse.update(self.cat.rect, self.walls)
                self.mouse.update(self.cat.rect.x, self.cat.rect.y, self.walls)

                self.screen.fill((255, 255, 255))

                for wall in self.walls:
                    self.screen.blit(wall.image, wall.rect.topleft)

                self.cat.draw(self.screen)
                self.mouse.draw(self.screen)

                # Проверка на столкновение кота и мыши
                if self.cat.rect.colliderect(self.mouse.rect):
                    self.game_over = True

            if self.game_paused:
                self.draw_pause_menu()

            if self.game_over:
                self.draw_game_over_menu()

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == "__main__":
    game = Game()
    game.run_game()
