# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:53:18 2024

@author: USER
"""

import pygame
import math
from test_player import player

pygame.init()

#background music
def load_music():
    """Load the music"""
    song1 = 'src/sound/background.ogg'
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)
    
load_music()



#設定顏色
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)
img_player1 = []
img_player2 = []

for i in range(2):
    img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
    img_player1.append(pygame.transform.scale(img, (64, 64)))
    img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
    img_player2.append(pygame.transform.scale(img, (64, 64)))


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
    ang = 0
    #------------------


    #建立時鐘物件
    clock = pygame.time.Clock()
    fps = 80

    #center
    #move
    tmp = 0
    p = player()
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

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            p.setspeed(5)
        else:
            p.setspeed(2)
        
        if key[pygame.K_LEFT]:
            p.move()
            if key[pygame.K_UP]:
                tmp = 45
            elif key[pygame.K_DOWN]:
                tmp = 135
            else:
                tmp = 90
        elif key[pygame.K_RIGHT]:
            p.move()
            if key[pygame.K_UP]:
                tmp = 315
            elif key[pygame.K_DOWN]:
                tmp = 225
            else:
                tmp = 270
        elif key[pygame.K_UP]:
            p.move()
            tmp = 0
        elif key[pygame.K_DOWN]:
            p.move()
            tmp = 180

        if p.ang < tmp and p.ang + 180 >= tmp:
            p.ang += 5
        elif p.ang > tmp and p.ang - 180 <= tmp:
            p.ang -= 5
        elif p.ang < tmp:
            p.ang += 360
        elif p.ang > tmp:
            p.ang -= 360
        
        #p.move()

        img = pygame.transform.rotate(img_player1[0], p.ang)
        #img = pygame.transform.rotozoom(img_player1, ang, 1)
        screen.blit(img, [300 + p.x - img.get_width() / 2, 300 + p.y - img.get_height() / 2])
        
        
if __name__ == '__main__':
    main()	