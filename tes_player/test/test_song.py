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
    pygame.display.set_caption('test_song')

    #------------------
    screen.fill(black)
    #------------------


    #建立時鐘物件
    clock = pygame.time.Clock()
    fps = 80

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

if __name__ == '__main__':
    main()	