import pygame
import math
import random
from player import *
from module import load_music

pygame.init()

#設定顏色
white = (255,255,255)
black = (0, 0, 0)
pink = (244, 224, 244)



#主程式
def main():

    #background music
    song1 = 'src/sound/state0.wav'
    load_music(song1)

    #attack music
    attack_sound = pygame.mixer.Sound('src/sound/attack.ogg')


    #設定畫面大小
    screen_width = 1280
    screen_height = 720
    screen_size = (screen_width, screen_height)

    #設定主畫布與標題
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('class_test')

    #背景顏色
    screen.fill(black)

    #建立時鐘物件
    clock = pygame.time.Clock()

    #畫面更新速度
    fps = 80

    #--------------------------------------------------


    #設定玩家圖片
    img_player1 = []
    img_player2 = []

    #玩家大小
    player_size = 50

    #load images
    for i in range(2):
        img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
        img_player1.append(pygame.transform.scale(img, (player_size, player_size)))
        img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
        img_player2.append(pygame.transform.scale(img, (player_size, player_size)))

    #設定衝刺物件圖片
    img_sp = []

    #衝刺物件大小
    sp_size = 32

    #load images
    for i in range(2):
        img = pygame.image.load('src/images/sprint' + str(i) + '.png')
        img_sp.append(pygame.transform.scale(img, (sp_size, sp_size)))

    #玩家基本設定
    P1 = player(0, 0)
    P2 = player(screen_width / 2, screen_height / 2, 3, 0, 8, 1)

    #狀態
    time = 0 #時間
    STATE = 0 #0:攻擊, 1:防禦
    flag = [0, 0] #0:未按下, 1:按下
    t_flag = 0 #0:未碰撞, 1:碰撞
    dx, dy = 0, 0
    
    #字體
    font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 30)
    p1_text = font.render("P1", True, (255, 255, 255))
    p2_text = font.render("P2", True, (255, 255, 255))

    #--------------------------------------------------------------


    #迴圈控制變數
    run = True
    while run:
        
        
        #更新畫面
        clock.tick(fps)
        pygame.display.flip()
        screen.fill(black)

        #--------------------------------------------------
        
        #按下ESC, X鍵結束遊戲
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN : #鍵盤按下事件
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        #--------------------------------------------------

        #偵測鍵盤按鍵
        key = pygame.key.get_pressed()

        if key[pygame.K_v]: #"v":衝刺
            if flag[0] == 0:
                if P1.sprint_time <= 0:
                    P1.setdrift()
                flag[0] = 1
        else:
            flag[0] = 0
        
        if key[pygame.K_COMMA]: #",":衝刺
            if flag[1] == 0:
                if P2.sprint_time <= 0:
                    P2.setdrift()
                flag[1] = 1
        else:
            flag[1] = 0

        #--------------------------------------------------

        #碰撞偵測s
        if abs(P1.x - P2.x) < player_size and abs(P1.y - P2.y) < player_size:
            if t_flag == 0:
                t_flag = 1
                attack_sound.play()
                P1.settouch()
                P2.settouch()
                dx = P1.x - P2.x
                dy = P1.y - P2.y
        else:
            t_flag = 0
        
        if t_flag == 1:
            if abs(dx) > abs(dy):
                P1.x += dx / abs(dx) * 2
                P2.x -= dx / abs(dx) * 2
            else:
                P1.y += dy / abs(dy) * 2
                P2.y -= dy / abs(dy) * 2 

        #玩家速度控制
        P1.setspeed()
        P2.setspeed()

        #玩家移動
        P1.turn_move(key, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d)
        P2.turn_move(key, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT)

        #繪製玩家
        P1.drift(screen, img_sp[STATE])
        P2.drift(screen, img_sp[1 - STATE])
        P1.draw(screen, img_player1[STATE])
        P2.draw(screen, img_player2[1 - STATE])
        screen.blit(p1_text, (P1.x - 10, P1.y - 50))
        screen.blit(p2_text, (P2.x - 10, P2.y - 50))

        #--------------------------------------------------

        #狀態切換
        time += 1
        if time % 250 == 0:
            STATE = 1 - STATE
            P1.state = STATE
            P2.state = 1 - STATE

        pygame.mouse.set_visible(0)
        ms_x, ms_y = pygame.mouse.get_pos()
        pygame.draw.circle(screen, pink, (ms_x, ms_y), 5)
        
#--------------------------------------------------------------


if __name__ == '__main__':
    main()	