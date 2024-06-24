import pygame
import random
from pygame.transform import scale

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мебель в комнате")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Размеры комнаты
ROOM_WIDTH = 600
ROOM_HEIGHT = 400

# Загрузка изображений мебели
sofa = pygame.image.load(f"images/furniture/sofa/{random.randint(1,5)}.png").convert_alpha()
table = pygame.image.load(f"images/furniture/table/{random.randint(1,14)}.png").convert_alpha()
chair = pygame.image.load(f"images/furniture/chair/{random.randint(1,8)}.png").convert_alpha()
bed = pygame.image.load(f"images/furniture/bed/{random.randint(1,11)}.png").convert_alpha()
plant = pygame.image.load(f"images/furniture/plant/{random.randint(1,2)}.png").convert_alpha()
picture = pygame.image.load(f"images/furniture/picture/{random.randint(1,14)}.png").convert_alpha()

# Функция для рандомного размещения мебели
def place_furniture(room_x, room_y, room_width, room_height):
    # Список мебели для размещения
    furniture = [sofa, table, chair, bed, plant, picture]

    # Цикл размещения мебели
    for i in furniture: #range(1, 7):
        #furniture_item = random.choice(furniture)
        furniture_width = i.get_width() #.get_width()
        furniture_height = i.get_height() #furniture_item.get_height()

        # Генерируем случайные координаты для мебели
        furniture_x = random.randint(room_x, room_x + room_width - furniture_width)
        furniture_y = random.randint(room_y, room_y + room_height - furniture_height)

        # Отрисовка мебели
        screen.blit(i, (furniture_x, furniture_y))

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка комнаты (прямоугольник)
    pygame.draw.rect(screen, GRAY, (100, 100, ROOM_WIDTH, ROOM_HEIGHT), 2)

    # Размещение мебели в комнате
    place_furniture(100, 100, ROOM_WIDTH, ROOM_HEIGHT)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
