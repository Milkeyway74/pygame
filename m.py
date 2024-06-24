import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Выбор кота")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

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
            if dx > 0:
                self.rect.x -= MOUSE_SPEED
            else:
                self.rect.x += MOUSE_SPEED
        else:
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
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
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
        self.rect.x = min(WIDTH - self.rect.width, self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(HEIGHT - self.rect.height, self.rect.y)

# Функция для выбора кота
def choose_cat():
    # Загрузка изображений котов
    cat_images = [
        pygame.image.load("cat1.png").convert_alpha(),
        pygame.image.load("cat2.png").convert_alpha(),
        pygame.image.load("cat3.png").convert_alpha()
    ]

    # Вывод котов на экран
    for i, cat_image in enumerate(cat_images):
        cat_x = 100 + i * (cat_image.get_width() + 50)
        cat_y = 100
        screen.blit(cat_image, (cat_x, cat_y))

    # Цикл ожидания выбора кота
    selected_cat = None
    while selected_cat is None:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, cat_image in enumerate(cat_images):
                    cat_x = 100 + i * (cat_image.get_width() + 50)
                    cat_y = 100
                    if cat_x <= event.pos[0] <= cat_x + cat_image.get_width() and \
                       cat_y <= event.pos[1] <= cat_y + cat_image.get_height():
                        selected_cat = cat_image

        # Отрисовка выбранного кота (с рамкой)
        if selected_cat is not None:
            cat_rect = selected_cat.get_rect()
            pygame.draw.rect(screen, GRAY, (cat_rect.x - 5, cat_rect.y - 5, cat_rect.width + 10, cat_rect.height + 10), 3)
            screen.blit(selected_cat, (cat_rect.x, cat_rect.y))
# Обновление экрана
        pygame.display.flip()

    return selected_cat

# Создание спрайтов
selected_cat_image = choose_cat()  # Выбор кота пользователем
cat = Cat(random.randint(0, WIDTH - CAT_SIZE), random.randint(0, HEIGHT - CAT_SIZE), selected_cat_image)
mouse = Mouse(random.randint(0, WIDTH - MOUSE_SIZE), random.randint(0, HEIGHT - MOUSE_SIZE))

# Главный цикл игры
running = True
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

pygame.quit()
