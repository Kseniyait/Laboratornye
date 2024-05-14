import math
from random import choice, randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 10
        self.time = 0
        self.isCollisionDown = False
        self.is_dead = False

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        if self.time >= self.live:
            self.is_dead = True
            return

        self.time += .1
        self.x += self.vx
        if not self.isCollisionDown:
            vy = - self.r + -self.vy + 9.81 * self.time * self.time / 2
        else:
            vy = self.r + +self.vy - 9.81 * \
            abs(self.live - self.time) / 2
        self.y += vy

        if self.x <= 0 or self.x >= WIDTH:
            self.vx = -self.vx
            
        if self.y <= 0 and self.isCollisionDown:
            self.vy = -self.vy
            self.isCollisionDown = False
        if self.y >= HEIGHT and not self.isCollisionDown:
            self.vy = -self.vy
            self.isCollisionDown = True

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        v1 = pygame.math.Vector2(self.x, self.y)
        v2 = pygame.math.Vector2(obj.x, obj.y)
        if v1.distance_to(v2) < self.r + obj.r:
            self.time = self.live
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = (200,200,200,200)#GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0]-20) != 0:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
            else:
                return
        if self.f2_on:
            self.color = (255,0,0,255)#RED
        else:
            self.color = (200,200,200,200)#GREY

    def draw(self):
        # FIXIT don't know how to do it
        x = 40
        y = 450
        w = self.f2_power
        h = 5
        self.an = math.atan2((pygame.mouse.get_pos()[1]-y),
                             (pygame.mouse.get_pos()[0]-x))
        gun = pygame.Surface((w, h), pygame.SRCALPHA)
        gun.fill(self.color)
        rotated_gun = pygame.transform.rotate(gun, -self.an * 180 / math.pi)
        gun_rect = rotated_gun.get_rect(center = (x, y))    
        self.screen.blit(rotated_gun, gun_rect)
        

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = (255,0,0,255)#RED
        else:
            self.color = (200,200,200,200)#GREY


class Target:
    # self.points = 0
    # self.live = 1
    # FIXME: don't work!!! How to call this functions when object is created?
    # self.new_target()

    def __init__(self, screen, text_offset_pos):
        self.live = 1
        self.points = 0
        self.screen = screen
        self.old_bullets =  0
        self.alive = True
        self.DELAY = 2000
        self.last_time = pygame.time.get_ticks()
        self.text_offset_pos = text_offset_pos

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        self.direction = randint(0,1)
        self.speedX = randint(1,10)
        self.speedY = randint(1,10)
        color = self.color = RED
        self.live = 1
        

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.alive = False
        self.last_time = pygame.time.get_ticks()
        self.points += points
        self.text_surface = my_font.render("Цель поражена за " +
                                      str(bullet - self.old_bullets) +
                                      " попаданий",
                                      False, (0, 0, 0))
        self.size = self.text_surface.get_size()
        self.old_bullets = bullet

    def draw(self):
        if self.alive:
            pygame.draw.circle(
                self.screen,
                self.color,
                (self.x, self.y),
                self.r
            )
        
        if not self.alive:
            self.screen.blit(self.text_surface,
                             ((WIDTH - self.size[0]) / 2,
                              (HEIGHT - self.size[1]) / 2 + self.text_offset_pos))
        
    def update(self):
        
        time_now = pygame.time.get_ticks()
        if self.direction == 0:
            self.x += self.speedX
            if self.x < 0 or self.x > WIDTH:
                self.speedX =-self.speedX
        else:
            self.y += self.speedY
            if self.y < 0 or self.y > HEIGHT:
                self.speedY =-self.speedY

        if time_now - self.last_time >= self.DELAY:
            self.alive = True


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen, 0)
target.new_target()

target2 = Target(screen, 50)
target2.new_target()

finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.update()
    target2.update()

    target.draw()
    target2.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        if b.is_dead:
            balls.remove(b)
        b.move()
        if b.hittest(target) and target.live:
            target.live = 0
            target.hit()
            target.new_target()
        if b.hittest(target2) and target2.live:
            target2.live = 0
            target2.hit()
            target2.new_target()
    gun.power_up()

pygame.quit()
