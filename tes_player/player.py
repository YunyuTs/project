import pygame
import math
from module import blitRotate


#衝刺物件
class sprint():
    def __init__(self, x, y, direction = 0, speed = 0, o_speed = 0, ang = 0, time = 0):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.o_speed = o_speed
        self.ang = ang
        self.time = time
    
    def drift(self):
        self.x += self.speed * math.sin(math.radians(self.ang))
        self.y += self.speed * math.cos(math.radians(self.ang))
        self.direction -= 2

    def setsp(self):
        self.speed = self.o_speed * math.cos((100 - self.time) / 30)
    
    def draw(self, screen, img):
        if self.speed > 0 and self.time > 0:
            blitRotate(screen, img, (self.x, self.y), (img.get_width() / 2, img.get_height() / 2), self.direction)


#設定最大最小速度
max_speed = 8
min_speed = 3


#玩家基本屬性
class player():
    def __init__(self, x = 300, y = 300, speed = min_speed, ang = 0, life = 8, state = 0, time = 0):
        self.x = x
        self.y = y
        self.speed = speed
        self.ang = ang
        self.life = life
        self.state = state
        self.time = time

    def move(self):
        self.x -= self.speed * math.sin(math.radians(self.ang))
        self.y -= self.speed * math.cos(math.radians(self.ang))

    def sp(self):
        if self.time > 0 and self.speed > min_speed:
            self.speed = max_speed + (max_speed + 1 - min_speed) * math.sin(100 - self.time / 10)
            self.time -= 1
        else:
            self.speed = min_speed
    
    def touch(self):
        if self.state == 1:
            self.life -= 1

    def draw(self, screen, img):
        blitRotate(screen, img, (self.x, self.y), (img.get_width() / 2, img.get_height() / 2), self.ang)
        
    def pos(self, key, a, w, s, d):
        if key[a]:
            self.move()
            if key[w]:
                tmp = 45
            elif key[s]:
                tmp = 135
            else:
                tmp = 90
        elif key[d]:
            self.move()
            if key[w]:
                tmp = 315
            elif key[s]:
                tmp = 225
            else:
                tmp = 270
        elif key[w]:
            self.move()
            tmp = 0
        elif key[s]:
            self.move()
            tmp = 180
        else:
            tmp = self.ang
        
        if abs(self.ang - tmp) == 180 or abs(self.ang - tmp) == 90:
            self.ang = tmp
        elif self.ang < tmp and self.ang + 180 > tmp:
            self.ang += 5
        elif self.ang > tmp and self.ang - 180 < tmp:
            self.ang -= 5
        elif self.ang < tmp:
            self.ang += 360
        elif self.ang > tmp:
            self.ang -= 360
