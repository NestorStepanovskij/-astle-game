import pygame as pg
import random

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1020


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/godSup.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(midleft=pos)
        self.speed = 7

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class MainCharacter(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
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


class Peasant(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/MainCharacter.png").convert_alpha()
        size = random.randint(70, 150)
        self.image = pg.transform.scale(self.image, (size, size))
        self.image = pg.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()
        self.rect.midbottom = (random.randint(size, SCREEN_WIDTH - size), 0)

        self.speedx = random.choice([-1, 1]) * random.randint(1, 2)
        self.speedy = random.randint(1, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
