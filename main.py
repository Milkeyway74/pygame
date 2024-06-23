import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MAP_WIDTH = 1600
MAP_HEIGHT = 1200
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CAT_SIZE = 20
MOUSE_SIZE = 10
CAT_SPEED = 5
MOUSE_SPEED = 3

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat and Mouse Game")

# Позиции кота и мыши
cat_pos = [MAP_WIDTH // 2, MAP_HEIGHT // 2]
mouse_pos = [random.randint(60, MAP_WIDTH - 60), random.randint(60, MAP_HEIGHT - 60)]

# Списки стен
walls = [
    pygame.Rect(50, 50, MAP_WIDTH - 100, 5),   # Верхняя стена
    pygame.Rect(50, MAP_HEIGHT - 55, MAP_WIDTH - 100, 5),  # Нижняя стена
    pygame.Rect(50, 50, 5, MAP_HEIGHT - 100),   # Левая стена
    pygame.Rect(MAP_WIDTH - 55, 50, 5, MAP_HEIGHT - 100),  # Правая стена
    pygame.Rect(400, 300, 100, 5), # Внутренняя стена 1 верх
    pygame.Rect(400, 300, 5, 300), # Внутренняя стена 1 левая
    pygame.Rect(400, 600, 100, 5), # Внутренняя стена 1 низ
    pygame.Rect(500, 300, 5, 305), # Внутренняя стена 1 правая
    pygame.Rect(800, 200, 150, 5), # Внутренняя стена 2 верх
    pygame.Rect(800, 200, 5, 100), # Внутренняя стена 2 левая
    pygame.Rect(800, 300, 150, 5), # Внутренняя стена 2 низ
    pygame.Rect(950, 200, 5, 105), # Внутренняя стена 2 правая
    pygame.Rect(1200, 400, 150, 5), # Внутренняя стена 3 верх
    pygame.Rect(1200, 400, 5, 100), # Внутренняя стена 3 левая
    pygame.Rect(1200, 500, 150, 5), # Внутренняя стена 3 низ
    pygame.Rect(1350, 400, 5, 105)  # Внутренняя стена 3 правая
]

def check_collision(rect, walls):
    for wall in walls:
        if rect.colliderect(wall):
            return True
    return False

def move_mouse(mouse_pos, cat_pos):
    if mouse_pos[0] < cat_pos[0]:
        mouse_pos[0] -= MOUSE_SPEED
    else:
        mouse_pos[0] += MOUSE_SPEED
    if mouse_pos[1] < cat_pos[1]:
        mouse_pos[1] -= MOUSE_SPEED
    else:
        mouse_pos[1] += MOUSE_SPEED

# Основной игровой цикл
running = True
camera_x = 0
camera_y = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Движение кота
    keys = pygame.key.get_pressed()
    initial_cat_pos = cat_pos.copy()
    if keys[pygame.K_LEFT]:
        cat_pos[0] -= CAT_SPEED
    if keys[pygame.K_RIGHT]:
        cat_pos[0] += CAT_SPEED
    if keys[pygame.K_UP]:
        cat_pos[1] -= CAT_SPEED
    if keys[pygame.K_DOWN]:
        cat_pos[1] += CAT_SPEED

    # Проверка границ для кота и стен
    cat_rect = pygame.Rect(*cat_pos, CAT_SIZE, CAT_SIZE)
    if check_collision(cat_rect, walls):
        cat_pos = initial_cat_pos

    # Движение мыши
    initial_mouse_pos = mouse_pos.copy()
    move_mouse(mouse_pos, cat_pos)
    mouse_rect = pygame.Rect(*mouse_pos, MOUSE_SIZE, MOUSE_SIZE)
    if check_collision(mouse_rect, walls) or mouse_pos[0] < 50 or mouse_pos[0] > MAP_WIDTH - 50 - MOUSE_SIZE or mouse_pos[1] < 50 or mouse_pos[1] > MAP_HEIGHT - 50 - MOUSE_SIZE:
        mouse_pos = initial_mouse_pos

    # Проверка столкновения
    if cat_rect.colliderect(mouse_rect):
        running = False
        print("Cat caught the mouse! Game Over!")

    # Центрирование камеры на коте
    camera_x = cat_pos[0] - SCREEN_WIDTH // 2
    camera_y = cat_pos[1] - SCREEN_HEIGHT // 2

    # Ограничение камеры границами карты
    if camera_x < 0:
        camera_x = 0
    if camera_y < 0:
        camera_y = 0
    if camera_x > MAP_WIDTH - SCREEN_WIDTH:
        camera_x = MAP_WIDTH - SCREEN_WIDTH
    if camera_y > MAP_HEIGHT - SCREEN_HEIGHT:
        camera_y = MAP_HEIGHT - SCREEN_HEIGHT

    # Отрисовка
    screen.fill(WHITE)

    # Отрисовка стен с учетом камеры
    for wall in walls:
        pygame.draw.rect(screen, BLACK, pygame.Rect(wall.x - camera_x, wall.y - camera_y, wall.width, wall.height))
    
    # Отрисовка кота и мыши с учетом камеры
    pygame.draw.rect(screen, RED, pygame.Rect(cat_rect.x - camera_x, cat_rect.y - camera_y, CAT_SIZE, CAT_SIZE))
    pygame.draw.rect(screen, BLUE, pygame.Rect(mouse_rect.x - camera_x, mouse_rect.y - camera_y, MOUSE_SIZE, MOUSE_SIZE))
    
    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
