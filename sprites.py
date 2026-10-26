import pygame as pg
import random
import math
from pygame.math import Vector2

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020


def get_aim(origin):
    """
    Единая точка расчёта направления на курсор.

    Возвращает кортеж (dir_x, dir_y, angle_deg):
      - dir_x, dir_y — нормализованный вектор от origin к курсору
                       (используется пулями и любым движением «в сторону курсора»);
      - angle_deg    — угол в градусах для pg.transform.rotate
                       (пригодится для поворота спрайта оружия).

    origin — (x, y) точка, откуда «смотрим» (центр игрока, плечо, дуло и т.д.).
    """
    mouse_x, mouse_y = pg.mouse.get_pos()
    dx = mouse_x - origin[0]
    dy = mouse_y - origin[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 1.0, 0.0, 0.0
    return dx / dist, dy / dist, math.degrees(math.atan2(-dy, dx))


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, direction):
        super().__init__()
        self.image = pg.image.load("images/godSup.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))

        # Позиция в float, чтобы диагональное движение не «дёргалось» из-за int()
        self.pos = pg.math.Vector2(pos)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))

        # direction — уже нормализованный вектор из get_aim()
        self.direction = pg.math.Vector2(direction)
        if self.direction.length_squared() == 0:
            self.direction = pg.math.Vector2(1, 0)
        else:
            self.direction = self.direction.normalize()

        self.speed = 7

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        # Удаляем, когда пуля ушла за экран (по любой стороне)
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()


class MainCharacter(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/ГГ_шаг1_лево.png").convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.midleft = (0, 300)
        self.speed = 3

    def update(self):
        keys = pg.key.get_pressed()
        dx = dy = 0
        if keys[pg.K_w]: dy -= self.speed
        if keys[pg.K_s]: dy += self.speed
        if keys[pg.K_d]: dx += self.speed
        if keys[pg.K_a]: dx -= self.speed

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self.rect.x += int(dx)
        self.rect.y += int(dy)
        self.rect.clamp_ip(pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class EnemyBullet(pg.sprite.Sprite):
    def __init__(self, origin, target):
        super().__init__()
        self.image = pg.Surface((12, 12), pg.SRCALPHA)
        pg.draw.circle(self.image, "orange", (6, 6), 6)

        self.pos = Vector2(origin)
        self.rect = self.image.get_rect(center=origin)

        direction = Vector2(target) - self.pos
        if direction.length_squared() == 0:
            direction = Vector2(1, 0)

        # Random error makes their shots less accurate.
        self.velocity = direction.normalize().rotate(
            random.uniform(-20, 20)
        ) * 2

    def update(self):
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not self.rect.colliderect(
            pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        ):
            self.kill()


class Peasant(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("images/heal_potion.png").convert_alpha()
        size = random.randint(70, 150)
        self.image = pg.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.randint(size, SCREEN_WIDTH - size), 0)

        self.speedx = random.choice([-1, 1]) * random.randint(1, 2)
        self.speedy = random.randint(1, 2)
        self.next_shot_time = pg.time.get_ticks() + random.randint(2000, 4000)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    def shoot(self, target, current_time):
        if current_time < self.next_shot_time:
            return None

        if not self.rect.colliderect(
            pg.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        ):
            return None

        self.next_shot_time = current_time + random.randint(3000, 5000)
        return EnemyBullet(self.rect.center, target)


class Gun(pg.sprite.Sprite):
    def __init__(self, target, image, offset=40, follow=0.35):
        super().__init__()
        # чистый спрайт — от него и только от него поворачиваем
        self.base_image = image.convert_alpha()
        self.image = self.base_image
        self.rect = self.image.get_rect()

        self.target = target
        self.offset = offset      # насколько далеко от центра игрока «висит» оружие
        self.follow = follow      # 0..1: 1.0 — жёстко прикреплено, 0.3 — плавное следование

        self.pos = Vector2(target.rect.center)   # позиция в float
        self.angle = 0.0

    def update(self, aim_x=1.0, aim_y=0.0, aim_angle=0.0):
        # 1) Куда оружие должно «хотеть» попасть: центр игрока + смещение по прицелу
        target_pos = Vector2(self.target.rect.center) + Vector2(aim_x, aim_y) * self.offset

        # 2) Плавно (или мгновенно, если follow=1) приближаемся
        self.pos = self.pos.lerp(target_pos, self.follow)

        # 3) Поворачиваем из чистого изображения
        self.angle = aim_angle
        self.image = pg.transform.rotate(self.base_image, self.angle)
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
