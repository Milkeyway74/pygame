import pygame

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Построение комнаты")

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

# Функция для построения комнаты
def build_room(x, y, width, height):
    # Отрисовка стен
    screen.blit(wall_top_left, (x, y))
    screen.blit(wall_top_right, (x + width - wall_top_right.get_width(), y))
    screen.blit(wall_bottom_left, (x, y + height - wall_bottom_left.get_height()))
    screen.blit(wall_bottom_right, (x + width - wall_bottom_right.get_width(), y + height - wall_bottom_right.get_height()))

    # Отрисовка горизонтальных стен
    for i in range(x + wall_top_left.get_width(), x + width - wall_top_right.get_width(), wall_horizontal.get_width()):
        screen.blit(wall_horizontal, (i, y))
        screen.blit(wall_horizontal, (i, y + height - wall_horizontal.get_height()))

    # Отрисовка вертикальных стен
    for i in range(y + wall_top_left.get_height(), y + height - wall_bottom_left.get_height(), wall_vertical.get_height()):
        screen.blit(wall_vertical, (x, i))
        screen.blit(wall_vertical, (x + width - wall_vertical.get_width(), i))
    # Отрисовка задней стены
    screen.blit(floor, (x, y + wall_top_left.get_height()))  # Начинаем с верха левой стены
    back_wall_width = floor.get_width()
    back_wall_height = floor.get_height()
    for i in range(x, x + width - back_wall_width):
        screen.blit(floor, (i, y + wall_top_left.get_height()))

    # Отрисовка нижней стены
    for i in range(x, x + width, wall_low.get_width()):
        screen.blit(wall_low, (i, y + height - wall_low.get_height()))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill((0, 0, 0))

    # Построение комнаты
    build_room(100, 100, 500, 300)

    # Обновление экрана
    pygame.display.flip()

pygame.quit()

