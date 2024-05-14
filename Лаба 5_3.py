import pygame
from pygame.draw import *
from random import randint
pygame.init()
pygame.font.init() 

FPS = 60
TIME_LIFE = 1000
last_time = pygame.time.get_ticks()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

points = 0
points_font = pygame.font.SysFont('Comic Sans MS', 30)

MAX_BALLS = 5
BALL_SPEED_MIN = -10
BALL_SPEED_MAX = 10

BORDER_LEFT = SCREEN_WIDTH // 4
BORDER_RIGHT = SCREEN_WIDTH // 1.5
BORDER_TOP = 0
BORDER_BOTTOM = SCREEN_HEIGHT

balls_x = []
balls_y = []
balls_x_speed = []
balls_y_speed = []
balls_r = []
balls_color = []

def new_ball(coords_x, coords_y, radius):
    '''
    Создает и возвращает параметры нового шар на экране
    в случайных координатах и случайного цвета.
    coords_x - кортеж из координат начала и конца по оси Х,
    coords_y - кортеж из координат начала и конца по оси Y,
    radius - кортеж из диапазона радиусов.
    '''
    x_start, x_end = coords_x
    y_start, y_end = coords_y
    r_start, r_end = radius

    r = randint(r_start, r_end)
    x = randint(x_start + r, x_end - r)
    y = randint(y_start + r, y_end - r)
    
    color = COLORS[randint(0, 5)]

    speed_x = randint(BALL_SPEED_MIN, BALL_SPEED_MAX) / 5
    speed_y = randint(BALL_SPEED_MIN, BALL_SPEED_MAX) / 5
    
    return color, x, y, r, speed_x, speed_y

def click(event):
    '''
    Функция обработки нажатия мыши.
    Проверяет, находятся ли координаты мыши в каком-либо круге,
    если да, то начисляется 1 очко
    '''
    global points
    mouse_x = event.pos[0]
    mouse_y = event.pos[1]
    for i in range(MAX_BALLS):
        # Вычисляем расстояние между центром круга и координатами мыши
        evklid_r = ((balls_x[i] - mouse_x) ** 2 +
                    (balls_y[i] - mouse_y) ** 2) ** 0.5
        # Если расстояние меньше радиуса круга, значит мы попали в круг
        if evklid_r <= balls_r[i]:
            points += 1
            

def move_circles():
    '''
    Функция перемещения шаров по экрану с проверкой столкновения с краями
    '''
    for i in range(MAX_BALLS):
        # Перемещение шара
        balls_x[i] += balls_x_speed[i]
        balls_y[i] += balls_y_speed[i]
        # Проверка столкновений
        # Левая граница
        if balls_x[i] - balls_r[i] <= BORDER_LEFT:
            balls_x_speed[i] = - balls_x_speed[i]
        # Правая граница
        if balls_x[i] + balls_r[i] >= BORDER_RIGHT:
            balls_x_speed[i] = - balls_x_speed[i]
        # Верхняя граница
        if balls_y[i] - balls_r[i] <= BORDER_TOP:
            balls_y_speed[i] = - balls_y_speed[i]
        # Нижняя граница
        if balls_y[i] + balls_r[i] >= BORDER_BOTTOM:
            balls_y_speed[i] = - balls_y_speed[i]
        

def draw_circle(screen, color, x, y, r):
    '''
    Функция прорисовки шаров на экране
    '''
    circle(screen, color, (x, y), r)

# Создание первой партии шаров
for i in range(MAX_BALLS):
    ball_color, ball_x, ball_y, ball_r, ball_speed_x, ball_speed_y = \
    new_ball((BORDER_LEFT, BORDER_RIGHT),
             (BORDER_TOP, BORDER_BOTTOM), (20, 100))
    balls_x.append(ball_x)
    balls_y.append(ball_y)
    balls_x_speed.append(ball_speed_x)
    balls_y_speed.append(ball_speed_y)
    balls_r.append(ball_r)
    balls_color.append(ball_color)

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    time_now = pygame.time.get_ticks()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)

    # Передвижение шаров
    for i in range(MAX_BALLS):
        move_circles()
    
    # Заливка черным цветом всего экрана
    screen.fill(BLACK)

    # Прорисовка очков
    text_points = points_font.render("Очки: " + str(points), False, (200, 200, 0))
    screen.blit(text_points, [SCREEN_WIDTH - text_points.get_size()[0] - 10, 0])

    # Создание шаров
    # Происходит с периодичностью раз в TIME_LIFE милисекунд
    if time_now - last_time >= TIME_LIFE:
        last_time = time_now
        for i in range(MAX_BALLS):
            balls_color[i], balls_x[i], balls_y[i], balls_r[i],balls_x_speed[i], balls_y_speed[i] = \
            new_ball((BORDER_LEFT, BORDER_RIGHT),
             (BORDER_TOP, BORDER_BOTTOM), (20, 100))

    # Прорисовка шаров
    for i in range(MAX_BALLS):
        draw_circle(screen, balls_color[i], balls_x[i], balls_y[i], balls_r[i])
    
    pygame.display.update()
    

pygame.quit()
