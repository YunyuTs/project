import pygame
import math
import random
#from test_player import player
from player import player
from module import *

pygame.init()

#load music
song1 = 'src/sound/background.ogg'
load_music(song1)
attack = pygame.mixer.Sound('src/sound/attack.ogg')

#設定顏色
white = (255,255,255)
black = (0, 0, 0)
pink = (244, 224, 244)

img_player1 = []
img_player2 = []

#load images
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

    #建立時鐘物件
    clock = pygame.time.Clock()
    fps = 80

    #衝刺計時
    t1, t2 = 0, 0

    #建立玩家
    p1 = player()
    p2 = player(700, 300, 2, 0, 8, 1)
    img_p1 = img_player1[p1.state]
    img_p2 = img_player2[p2.state]

    #attack
    isattack = 0
    
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
        if key[pygame.K_COMMA]:
            p1.setspeed(sp(t1))
            if sp(t1) > 3:
                t1 += 1
        else:
            t1 = 0
            p1.setspeed(3)
        
        if key[pygame.K_v]:
            p2.setspeed(sp(t2))
            if sp(t2) > 3:
                t2 += 1
        else:
            t2 = 0
            p2.setspeed(3)

        #attack control
        if abs(p1.x - p2.x) < 64 and abs(p1.y - p2.y) < 64:
            if isattack == 0:
                attack.play(0)
                p2.touch()
                isattack = 1
        else:
            isattack = 0

        #player move control
        p1.ang = pos(p1, key, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT)
        p2.ang = pos(p2, key, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d)

        #turn from center
        blitRotate(screen, img_p1, (p1.x, p1.y), (img_p1.get_width() / 2, img_p1.get_height() / 2), p1.ang)
        blitRotate(screen, img_p2, (p2.x, p2.y), (img_p2.get_width() / 2, img_p2.get_height() / 2), p2.ang)
        
        font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 48)
        imgText = font.render(str(p1.life) + "  " + str(p2.life), True, white)
        screen.blit(imgText, (5, 5))

        #mx, my = pygame.mouse.get_pos()
        #pygame.draw.circle(screen, pink, (mx, my), 5)

if __name__ == '__main__':
    main()	