import pygame as p

class Bullet1(p.sprite.Sprite):
    def __init__(self, position):
        p.sprite.Sprite.__init__(self)

        self.image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 15
        self.active = False
        self.mask = p.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

class Bullet2(p.sprite.Sprite):
    def __init__(self, position):
        p.sprite.Sprite.__init__(self)

        self.image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\bullet2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 30
        self.active = False
        self.mask = p.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True
