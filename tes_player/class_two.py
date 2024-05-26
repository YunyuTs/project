# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:53:18 2024

@author: USER
"""

import pygame
import math
import random
#from test_player import player
from player import *
from module import load_music

pygame.init()

song1 = 'src/sound/background.ogg'
load_music(song1)

#設定顏色
white = (255,255,255)
black = (0, 0, 0)
pink = (244, 224, 244)

img_player1 = []
img_player2 = []
max_speed = 8
min_speed = 3

#load images
for i in range(2):
    img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
    img_player1.append(pygame.transform.scale(img, (50, 50)))
    img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
    img_player2.append(pygame.transform.scale(img, (50, 50)))




def main():

    #設定畫面大小
    screen_width = 1280
    screen_height = 720
    screen_size = (screen_width, screen_height)
    #設定主畫布與標題
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('class_test')

    #------------------
    screen.fill(black)
    #------------------


    #建立時鐘物件
    clock = pygame.time.Clock()
    fps = 80

    #center
    #move
    flag = 0
    p = player(600, 600)
    img = img_player1[0]
    s = [0, 0, 0]
    img_sp = pygame.image.load('src/images/Sprint0.png')
    img_sp = pygame.transform.scale(img_sp, (23, 23))

    #迴圈控制變數
    run = True
    while run:
        
        #播放速度控制
        clock.tick(fps)
        #更新畫面
        pygame.display.flip()
        screen.fill(black)
        
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN : #鍵盤按下事件
                if event.key == pygame.K_ESCAPE:
                    run = False

        #key handler
        key = pygame.key.get_pressed()

        #player speed control
        if key[pygame.K_SPACE]:
            if flag == 0:
                p.time = 100
                p.speed = max_speed
                for i in range(3):
                    o_speed = random.randint(2, 3)
                    ang = random.randint(0, 360)
                    s[i] = sprint(p.x, p.y, 0, o_speed, o_speed, ang, p.time)
                flag = 1
        else:
            flag = 0

        #速度控制
        p.sp()

        if s[0]:
            if s[0].time > 0 and s[0].speed > 1:
                for i in range(3):
                    s[i].setsp()
                    s[i].drift()
                    s[i].draw(screen, img_sp)
                    s[i].time -= 1
            else:
                for i in range(3):
                    s[i] = 0


        #player move control
        #p.ang = pos(p, key, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT)
        p.pos(key, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT)

        #turn from center
        p.draw(screen, img)

        ms_x, ms_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, pink, (ms_x, ms_y), 5)
        
if __name__ == '__main__':
    main()	