import pygame
import math
import random
from module import *

pygame.init()

class sprint():
    def __init__(self, x, y, direction = 0, speed = 0, o_speed = 0, ang = 0):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.o_speed = o_speed
        self.ang = ang
    
    def drift(self):
        self.x += self.speed * math.sin(math.radians(self.ang))
        self.y += self.speed * math.cos(math.radians(self.ang))
        self.direction -= 2

    def setsp(self, t):
        self.speed = o_speed * math.cos((100 - t) / 30)
    
    def draw(self, screen, img):
        if self.speed > 0:
            blitRotate(screen, img, (self.x, self.y), (img.get_width() / 2, img.get_height() / 2), self.direction)

            
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Drift Test')

white = (255, 255, 255)

img = pygame.image.load('src/images/Sprint0.png')
img = pygame.transform.scale(img, (32, 32))

x, y = screen_width/2, screen_height/2
s = [0, 0, 0]
k = sprint(x, y)
t = 0
flag = 0

#建立時鐘物件
clock = pygame.time.Clock()
fps = 60
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    screen.fill((0, 0, 0))


    key = pygame.key.get_pressed()

    
    if key[pygame.K_SPACE]:
        if flag == 0:
            t = 100
            flag = 1
            for i in range(3):
                o_speed = random.randint(2, 5)
                ang = random.randint(0, 360)
                s[i] = sprint(x, y, 0, o_speed, o_speed, ang)
    else:
        flag = 0

    if s[0]:
        if t > 0 and s[0].speed > 1:
            t -= 1
            for i in range(3):
                s[i].setsp(t)
                s[i].drift()
                s[i].draw(screen, img)
        else:
            for i in range(3):
                s[i].x, s[i].y = x, y
                s[i].direction = 0
    '''
    if key[pygame.K_SPACE]:
        if flag == 0:
            t = 100
            flag = 1
            o_speed = random.randint(2, 5)
            ang = random.randint(0, 360)
            k = sprint(x, y, 0, o_speed, o_speed, ang)
    else:
        flag = 0

    if t > 0 and k.speed > 1:
        t -= 1
        k.setsp(t)
        k.drift()
        k.draw(screen, img)
    else:
        k.x, k.y = x, y
        k.direction = 0
    '''

    pygame.draw.circle(screen, white, (int(screen_width/2), int(screen_height/2)), 20)

    #播放速度控制
    clock.tick(fps)
    #更新畫面
    pygame.display.flip()

pygame.quit()