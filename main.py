import pygame
import os
import glob
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cat and Mouse Game")

# Функция загрузки изображений и их увеличения
def load_images(folder, prefix, scale_factor=2):
    pattern = os.path.join(folder, f'{prefix}*.png')
    image_files = sorted(glob.glob(pattern))
    if not image_files:
        print(f"No images found with pattern: {pattern}")
    images = [pygame.transform.scale(pygame.image.load(img_file), (pygame.image.load(img_file).get_width() * scale_factor, pygame.image.load(img_file).get_height() * scale_factor)) for img_file in image_files]
    return images

# Проверка текущей рабочей директории
current_directory = os.path.dirname(os.path.abspath(__file__))
print(f"Current working directory: {current_directory}")

# Проверка, существует ли общая папка animals
animals_folder = os.path.join(current_directory, 'animals')

print(f"Animals folder exists: {os.path.exists(animals_folder)}")

if not os.path.exists(animals_folder):
    raise FileNotFoundError(f"Animals folder not found: {animals_folder}")

# Проверка содержимого папки animals
print(f"Contents of animals folder: {os.listdir(animals_folder)}")

# Настройки кота
CAT_SPEED = 5
cat_folder = os.path.join(animals_folder, 'cats_1')
cat_images_right = load_images(cat_folder, '0')
if not cat_images_right:
    raise FileNotFoundError("Cat images not found")
cat_images_left = [pygame.transform.flip(img, True, False) for img in cat_images_right]
cat_rect = cat_images_right[0].get_rect()
cat_rect.topleft = (100, 100)
cat_direction = "right"

# Настройки мыши
MOUSE_SPEED = 3
mouse_folder = os.path.join(animals_folder, 'mouse')
mouse_images = {
    "right": load_images(mouse_folder, '0'),
    "left": [pygame.transform.flip(img, True, False) for img in load_images(mouse_folder, '0')],
    "down": load_images(mouse_folder, '1'),
    "up": load_images(mouse_folder, '2')
}
if not mouse_images["right"] or not mouse_images["left"] or not mouse_images["down"] or not mouse_images["up"]:
    raise FileNotFoundError("Mouse images not found")
mouse_direction = "right"
mouse_rect = mouse_images["right"][0].get_rect()
mouse_rect.topleft = (500, 500)

# Вспомогательные функции
def draw_cat(screen, cat_rect, direction, frame):
    if direction == "right":
        screen.blit(cat_images_right[frame % len(cat_images_right)], cat_rect.topleft)
    elif direction == "left":
        screen.blit(cat_images_left[frame % len(cat_images_left)], cat_rect.topleft)

def draw_mouse(screen, mouse_rect, direction, frame):
    screen.blit(mouse_images[direction][frame % len(mouse_images[direction])], mouse_rect.topleft)

def move_cat(keys, cat_rect):
    global cat_direction
    if keys[pygame.K_LEFT]:
        cat_rect.x -= CAT_SPEED
        cat_direction = "left"
    if keys[pygame.K_RIGHT]:
        cat_rect.x += CAT_SPEED
        cat_direction = "right"
    if keys[pygame.K_UP]:
        cat_rect.y -= CAT_SPEED
    if keys[pygame.K_DOWN]:
        cat_rect.y += CAT_SPEED

    # Ограничение движения кота в пределах экрана
    if cat_rect.left < 0:
        cat_rect.left = 0
    if cat_rect.right > SCREEN_WIDTH:
        cat_rect.right = SCREEN_WIDTH
    if cat_rect.top < 0:
        cat_rect.top = 0
    if cat_rect.bottom > SCREEN_HEIGHT:
        cat_rect.bottom = SCREEN_HEIGHT

def move_mouse(mouse_rect, cat_rect):
    global mouse_direction
    if random.randint(0, 100) < 10:  # случайное движение с вероятностью 10% каждый кадр
        mouse_direction = random.choice(["left", "right", "up", "down"])

    if mouse_direction == "left":
        if mouse_rect.x - MOUSE_SPEED >= 0:  # проверка, чтобы мышь не выходила за левую границу экрана
            mouse_rect.x -= MOUSE_SPEED
    elif mouse_direction == "right":
        if mouse_rect.x + MOUSE_SPEED <= SCREEN_WIDTH - mouse_rect.width:  # проверка, чтобы мышь не выходила за правую границу экрана
            mouse_rect.x += MOUSE_SPEED
    elif mouse_direction == "up":
        if mouse_rect.y - MOUSE_SPEED >= 0:  # проверка, чтобы мышь не выходила за верхнюю границу экрана
            mouse_rect.y -= MOUSE_SPEED
    elif mouse_direction == "down":
        if mouse_rect.y + MOUSE_SPEED <= SCREEN_HEIGHT - mouse_rect.height:  # проверка, чтобы мышь не выходила за нижнюю границу экрана
            mouse_rect.y += MOUSE_SPEED

    return mouse_direction

# Основной игровой цикл
running = True
clock = pygame.time.Clock()
frame = 0

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление котом
    keys = pygame.key.get_pressed()
    move_cat(keys, cat_rect)

    # Управление мышью
    mouse_direction = move_mouse(mouse_rect, cat_rect)

    # Отрисовка экрана
    screen.fill((255, 255, 255))  # Заливка экрана белым цветом
    draw_cat(screen, cat_rect, cat_direction, frame)
    draw_mouse(screen, mouse_rect, mouse_direction, frame)
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(30)
    frame += 1

# Завершение работы Pygame
pygame.quit()
