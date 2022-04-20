import pygame as p
from random import *

#小型敌机
class SmallEnemy(p.sprite.Sprite):
    def __init__(self, bg_size):
        p.sprite.Sprite.__init__(self)
        
        self.image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.destroy_images=[]
        self.destroy_images.extend([p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy1_down1.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy1_down2.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy1_down3.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy1_down4.png")])
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.mask = p.mask.from_surface(self.image)
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-5 * self.height,0)
    
    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-5 * self.height,0)
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

#中型敌机
class MidEnemy(p.sprite.Sprite):
    energy = 8

    def __init__(self, bg_size):
        p.sprite.Sprite.__init__(self)
        
        self.image = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy2.png").convert_alpha()
        self.image_hit = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy2_hit.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.destroy_images=[]
        self.destroy_images.extend([p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy2_down1.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy2_down2.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy2_down3.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy2_down4.png")])
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.mask = p.mask.from_surface(self.image)
        self.energy = MidEnemy.energy
        self.hit = False
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-10 * self.height,-self.height)
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-10 * self.height,-self.height)

#大型敌机
class BigEnemy(p.sprite.Sprite):
    energy = 20
    def __init__(self, bg_size):
        p.sprite.Sprite.__init__(self)
        
        self.image1 = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_n1.png").convert_alpha()
        self.image2 = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_n2.png").convert_alpha()
        self.image_hit = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_hit.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.destroy_images=[]
        self.destroy_images.extend([p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_down1.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_down2.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_down3.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_down4.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_down5.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\enemy3_down6.png")])
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.mask = p.mask.from_surface(self.image1)
        self.energy = BigEnemy.energy
        self.hit = False
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-15 * self.height,-5 * self.height)
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    def reset(self):
        self.active = True
        self.energy = BigEnemy.energy
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-15 * self.height,-5 * self.height)