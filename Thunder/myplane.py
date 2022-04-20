import pygame as p

class MyPlane(p.sprite.Sprite):
    def __init__(self, bg_size):
        p.sprite.Sprite.__init__(self)

        self.image1 = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\me1.png").convert_alpha()
        self.image2 = p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\me2.png").convert_alpha()
        self.rect = self.image1.get_rect()
        self.destroy_images=[]
        self.destroy_images.extend([p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\me_destroy_1.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\me_destroy_2.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\me_destroy_3.png"),\
                                    p.image.load("C:\\Users\\dell\\Desktop\\python\\Thunder\\images\\me_destroy_4.png")])
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2 ,\
                                        self.height - self.rect.height - 60
        self.speed = 10
        self.active = True
        self.invincible = False
        self.mask = p.mask.from_surface(self.image1)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width
    def reset(self):
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2 ,\
                                        self.height - self.rect.height - 60
        self.active = True
        self.invincible = True