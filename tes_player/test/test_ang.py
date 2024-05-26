# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:53:18 2024

@author: USER
"""

import pygame
import math
#from player import player

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

    img_player1 = pygame.image.load('src/images/player' + str(0) + str(1) + '.png')
    img_player1 = pygame.transform.scale(img_player1, (64, 64))
    #center
    x, y =32, 32
    #move
    a, b = 0, 0
    speed = 2
    ang = 0
    tmp = 0
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
            speed = 5
        else:
            speed = 2
        
        if key[pygame.K_LEFT]:
            if key[pygame.K_UP]:
                tmp = 45
            elif key[pygame.K_DOWN]:
                tmp = 135
            else:
                tmp = 90
        elif key[pygame.K_RIGHT]:
            if key[pygame.K_UP]:
                tmp = 315
            elif key[pygame.K_DOWN]:
                tmp = 225
            else:
                tmp = 270
        elif key[pygame.K_UP]:
            tmp = 0
        elif key[pygame.K_DOWN]:
            tmp = 180

        if ang < tmp and ang + 180 >= tmp:
            ang += 5
        elif ang > tmp and ang - 180 <= tmp:
            ang -= 5
        elif ang < tmp:
            ang += 360
        elif ang > tmp:
            ang -= 360

        a = -speed * math.sin(math.radians(ang))
        b = -speed * math.cos(math.radians(ang))

        x += a
        y += b
        img = pygame.transform.rotate(img_player1, ang)
        #img = pygame.transform.rotozoom(img_player1, ang, 1)
        screen.blit(img, [300 + x - img.get_width() / 2, 300 + y - img.get_height() / 2])

if __name__ == '__main__':
    main()	