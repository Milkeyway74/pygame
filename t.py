import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мышь убегает от кота")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Размеры спрайтов
MOUSE_SIZE = 20
CAT_SIZE = 30

# Скорость движения
MOUSE_SPEED = 5
CAT_SPEED = 3

# Класс мыши
class Mouse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((MOUSE_SIZE, MOUSE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, cat_x, cat_y):
        # Вычисляем расстояние по осям X и Y
        dx = self.rect.x - cat_x
        dy = self.rect.y - cat_y

        # Определяем направление движения
        if abs(dx) > abs(dy):
            # Движение по оси X
            if dx > 0:
                self.rect.x -= MOUSE_SPEED
            else:
                self.rect.x += MOUSE_SPEED
        else:
            # Движение по оси Y
            if dy > 0:
                self.rect.y -= MOUSE_SPEED
            else:
                self.rect.y += MOUSE_SPEED

        # Ограничение движения по краям экрана
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(WIDTH - MOUSE_SIZE, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(HEIGHT - MOUSE_SIZE, self.rect.y)

# Класс кота
class Cat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CAT_SIZE, CAT_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, mouse_x, mouse_y):
        # Определяем направление движения
        if mouse_x > self.rect.x:
            self.rect.x += CAT_SPEED
        elif mouse_x < self.rect.x:
            self.rect.x -= CAT_SPEED

        if mouse_y > self.rect.y:
            self.rect.y += CAT_SPEED
        elif mouse_y < self.rect.y:
            self.rect.y -= CAT_SPEED

        # Ограничение движения по краям экрана
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(WIDTH - CAT_SIZE, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(HEIGHT - CAT_SIZE, self.rect.y)

# Создание спрайтов
mouse = Mouse(random.randint(0, WIDTH - MOUSE_SIZE), random.randint(0, HEIGHT - MOUSE_SIZE))
cat = Cat(random.randint(0, WIDTH - CAT_SIZE), random.randint(0, HEIGHT - CAT_SIZE))

# Главный цикл игры
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обновление спрайтов
    mouse.update(cat.rect.x, cat.rect.y)
    cat.update(mouse.rect.x, mouse.rect.y)

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка спрайтов
    screen.blit(mouse.image, mouse.rect)
    screen.blit(cat.image, cat.rect)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(30)  # 30 кадров в секунду

pygame.quit()





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
      
    def update(self, cat_x, cat_y):
        # Вычисляем расстояние по осям X и Y
        dx = self.rect.x - cat_x
        dy = self.rect.y - cat_y
        speed = self.speed

        # Определяем направление движения
        if abs(dx) > abs(dy):
            if dx > 0:
                self.rect.x -= speed
            else:
                self.rect.x += speed
        else:
            if dy > 0:
                self.rect.y -= speed
            else:
                self.rect.y += speed

        # Ограничение движения по краям экрана
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(800 - self.rect.x, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(600 - self.rect.y, self.rect.y)
        
    def draw(self, screen):
        screen.blit(self.images[self.direction][self.frame % len(self.images[self.direction])], self.rect.topleft)