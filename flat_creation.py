import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Генерация комнат")

# Загрузка изображений
wall_left = pygame.image.load("images/furniture/walls/left.png").convert_alpha()
wall_right = pygame.image.load("images/furniture/walls/right.png").convert_alpha()
wall_top_right = pygame.image.load("images/furniture/walls/right_high_corner.png").convert_alpha()
wall_top_left = pygame.image.load("images/furniture/walls/left_high_corner.png").convert_alpha()
wall_bottom_right = pygame.image.load("images/furniture/walls/right_low_corner.png").convert_alpha()
wall_bottom_left = pygame.image.load("images/furniture/walls/left_low_corner.png").convert_alpha()
wall_horizontal = pygame.image.load("images/furniture/walls/high.png").convert_alpha()
wall_vertical = pygame.image.load("images/furniture/walls/low.png").convert_alpha()
wall_low = pygame.image.load("images/furniture/walls/middle.png").convert_alpha()
floor = pygame.image.load("images/furniture/walls/middle.png").convert_alpha()

# Функция для отрисовки комнаты в проекции
def draw_room_projection(x, y, width, height):
    # Отрисовка пола (задняя стена)
    for i in range(x, x + width, floor.get_width()):
        screen.blit(floor, (i, y))  # Рисуем пол сверху

    # Отрисовка левой стены
    wall_left_height = wall_left.get_height()
    for i in range(y, y + height - wall_left_height, wall_vertical.get_height()):
        screen.blit(wall_vertical, (x, i))  # Рисуем вертикальные части левой стены
    screen.blit(wall_left, (x, y + height - wall_left_height))  # Рисуем нижнюю часть левой стены

    # Отрисовка правой стены
    wall_right_height = wall_right.get_height()
    for i in range(y, y + height - wall_right_height, wall_vertical.get_height()):
        screen.blit(wall_vertical, (x + width - wall_vertical.get_width(), i))  # Рисуем вертикальные части правой стены
    screen.blit(wall_right, (x + width - wall_right.get_width(), y + height - wall_right_height))  # Рисуем нижнюю часть правой стены

    # Отрисовка верхней стены
    for i in range(x + wall_top_left.get_width(), x + width - wall_top_right.get_width(), wall_horizontal.get_width()):
        screen.blit(wall_horizontal, (i, y))  # Рисуем горизонтальные части верхней стены

    # Отрисовка углов
    screen.blit(wall_top_left, (x, y))
    screen.blit(wall_top_right, (x + width - wall_top_right.get_width(), y))
    screen.blit(wall_bottom_left, (x, y + height - wall_bottom_left.get_height()))
    screen.blit(wall_bottom_right, (x + width - wall_bottom_right.get_width(), y + height - wall_bottom_right.get_height()))


# Функция для генерации коридора
def generate_corridor(room1_x, room1_y, room2_x, room2_y):
    # Определение направления коридора
    if room1_x == room2_x:
        # Горизонтальный коридор
        corridor_x = room1_x
        corridor_y = min(room1_y, room2_y) + 100
        corridor_width = 100
        corridor_height = abs(room1_y - room2_y) - 100
    else:
        # Вертикальный коридор
        corridor_x = min(room1_x, room2_x) + 100
        corridor_y = room1_y
        corridor_width = abs(room1_x - room2_x) - 100
        corridor_height = 100

    # Отрисовка коридора
    draw_room_projection(corridor_x, corridor_y, corridor_width, corridor_height)

# Функция для генерации комнат
def generate_rooms():
    # Генерация комнат
    rooms = []
    for i in range(3):
        room_width = random.randint(200, 400)
        room_height = random.randint(150, 300)
        if i == 0:
            room_x = 100
            room_y = 100
        else:
            room_x = rooms[i - 1]["x"] + rooms[i - 1]["width"] + 100
            room_y = random.randint(100, HEIGHT - room_height - 100)
        rooms.append({
            "x": room_x,
            "y": room_y,
            "width": room_width,
            "height": room_height
        })

    # Создание коридоров
    for i in range(2):
        generate_corridor(rooms[i]["x"], rooms[i]["y"], rooms[i + 1]["x"], rooms[i + 1]["y"])

    # Отрисовка комнат
    for room in rooms:
        draw_room_projection(room["x"], room["y"], room["width"], room["height"])

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Генерация комнат и коридоров
    generate_rooms()

    # Обновление экрана
    pygame.display.flip()

pygame.quit()
