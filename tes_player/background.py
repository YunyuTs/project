# -*- coding: utf-8 -*-
"""
Created on Sat May 18 14:53:18 2024

@author: USER
"""

import pygame
import math
import random
#from test_player import player

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

#background color
back = [(244, 224, 244), (70, 10, 80)]

#設定畫面大小
screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)

#設定主畫布與標題
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('background_test')

#設定場地大小
squar_x, squar_y = 100, 20
thickness = 30
side_color = [(93, 29, 104), (255, 226, 251)]
tweak = 10#調整位置


#設定玩家圖片
img_player1 = []
img_player2 = []
player_size = 50

#背景玩家圖片
img_p1 = []
img_p2 = []
p_size = 40

#生命值圖片
Life = []
p1_life = 8
p2_life = 8
heart_size = 30

for i in range(2):
    img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
    img_player1.append(pygame.transform.scale(img, (player_size, player_size)))
    img_p1.append(pygame.transform.scale(img, (p_size, p_size)))

    img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
    img_player2.append(pygame.transform.scale(img, (player_size, player_size)))
    img_p2.append(pygame.transform.scale(img, (p_size, p_size)))

    img = pygame.image.load('src/images/Life' + str(i) + '.png')
    Life.append(pygame.transform.scale(img, (heart_size, heart_size)))


def main():


    #建立時鐘物件
    clock = pygame.time.Clock()
    fps = 80

    #計數
    time = 0

    #狀態
    state = 1

    #迴圈控制變數
    run = True
    while run:
        
        #播放速度控制
        clock.tick(fps)
        #更新畫面
        pygame.display.flip()
        screen.fill(back[state])
        
        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN : #鍵盤按下事件
                if event.key == pygame.K_ESCAPE:
                    run = False

        
        #draw background
        pygame.draw.rect(screen, side_color[state], (squar_x, squar_y, screen_width - 2 * squar_x, screen_height - 2 * squar_y), thickness)
        p1_pos = (squar_x - p_size - tweak, screen_height - p_size - tweak)
        screen.blit(img_p1[state], p1_pos)
        for i in range(p1_life):
            screen.blit(Life[state], (p1_pos[0] + (p_size - heart_size) / 2, p1_pos[1] - heart_size * (i + 1)))

        p2_pos = (screen_width - squar_x + tweak, tweak)
        screen.blit(img_p2[1 - state], p2_pos)
        for i in range(p2_life):
            screen.blit(Life[1 - state], (p2_pos[0] + (p_size - heart_size) / 2, p2_pos[1] * 2 + heart_size * (i + 1) + tweak))

        #設定時間
        time += 1
        if time % 250 == 0:
            state = 1 - state
        
if __name__ == '__main__':
    main()	