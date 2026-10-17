import pygame as pg
import math

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("images/godSup.png").convert_alpha()
        self.image = pg.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topright=pos)
        self.speed = 7

    def update(self):
        self.rect.x += self.speed

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        # картинка персонажа
        self.image = pg.image.load("images/MainCharacter.png").convert_alpha()
        self.image = pg.transform.smoothscale(self.image, (75,75))
        # создание хитбокса и расположение персонажа
        self.rect = self.image.get_rect()
        self.rect.midleft = (0, 300)
        self.speed = 3

    # передвижение персонажа
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rect.y-=self.speed

        elif keys[pg.K_s]:
            self.rect.y+=self.speed

        elif keys[pg.K_d]:
            self.rect.x+=self.speed
        elif keys[pg.K_a]:
            self.rect.x-=self.speed
