import pygame
import math
from player import player

#初始化
pygame.init()
pygame.mixer.init()

#設定顏色
white = (255,255,255)
black = (0, 0, 0)

#background color
bg_color = [(244, 224, 244), (70, 10, 80)]

#設定畫面大小
screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)

#設定主畫布與標題
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('game')

#建立時鐘物件
clock = pygame.time.Clock()
fps = 80

#主程式
def game_play():

    #---------背景設定---------
    player_size = 50 #玩家大小
    sp_size = 32 #衝刺物件大小
    heart_size = 40 #生命值圖片大小
    time_width, time_height = 700, 10 #時間軸大小
    time_y = 30 #時間軸位置
    bg_width, bg_height = 100, 20 #場地大小
    thickness = 30 #邊界寬度
    side_color = [(93, 29, 104), (255, 226, 251)] #邊界顏色
    tweak = 10 #調整位置
    #--------------------------------


    #---------狀態設定---------
    time = 0 #時間
    state = 1 #0:攻擊 1:防禦
    state_flag = 0 #狀態轉換
    flag = [0, 0] #0:未按下 1:按下
    song_flag = 0 #轉換音樂
    t_flage = 0 #0:未碰撞 1:碰撞
    invince_time = 0 #無敵時間
    #--------------------------------


    #---------玩家設定---------
    #設定玩家圖片
    img_player1 = []
    img_player2 = []

    #load images
    for i in range(2):
        img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
        img_player1.append(pygame.transform.scale(img, (player_size, player_size)))
        img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
        img_player2.append(pygame.transform.scale(img, (player_size, player_size)))

    #設定衝刺物件圖片
    img_sp = []

    #load images
    for i in range(2):
        img = pygame.image.load('src/images/sprint' + str(i) + '.png')
        img_sp.append(pygame.transform.scale(img, (sp_size, sp_size)))

    #生命值圖片
    Life = []

    #load images
    for i in range(2):
        img = pygame.image.load('src/images/Life' + str(i) + '.png')
        Life.append(pygame.transform.scale(img, (heart_size, heart_size)))

    #玩家基本設定
    P1 = player(bg_width + thickness + player_size, screen_height / 2 + time_y)
    P2 = player(screen_width - bg_width - thickness - player_size, screen_height / 2 + time_y, 3, 0, 8, 1)

    #字體
    font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 30)
    #--------------------------------


    #---------音樂設定---------
    #背景音樂
    song = ['src/sound/state0.wav', 'src/sound/state1.wav']
    volume = 0.3
    pygame.mixer.music.set_volume(volume)
    len = int(pygame.mixer.Sound(song[0]).get_length() * fps)
    
    #轉場音效
    change = pygame.mixer.Sound('src/sound/change.wav')
    change_volume = volume / 3
    change.set_volume(change_volume)

    #音效
    attack = pygame.mixer.Sound('src/sound/attack.ogg')
    attack_volume = volume / 3
    attack.set_volume(attack_volume)
    #--------------------------------


    #---------遊戲迴圈---------
    run = True
    while run:
        #-------音樂播放、狀態轉換-------
        if time % 2 == 0:
            if pygame.mixer.music.get_busy():
                song_flag = 0
            else:
                #print(pygame.mixer.Channel(0).get_busy())
                if song_flag == 0:
                    #pygame.mixer.music.stop()
                    time = 0
                    change.play()
                    state = 1 - state
                    P1.state = state
                    P2.state = 1 - state    
                    pygame.mixer.music.load(song[state])
                    pygame.mixer.music.play()
                    song_flag = 1
        #--------------------------------

        
        #---------基礎設定---------
        #時間揁數
        clock.tick(fps)
        #更新畫面
        pygame.display.flip()
        screen.fill(bg_color[state])

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    run = False
        #--------------------------------


        #-------game play------
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
        if abs(P1.x - P2.x) < player_size and abs(P1.y - P2.y) < player_size and invince_time <= 0:
            if t_flag == 0:
                t_flag = 1
                attack.play()
                invince_time = 200
                if state == 0:
                    P2.life -= 1
                    if P2.life <= 0:
                        print("P1 win")
                        run = False
                else:
                    P1.life -= 1
                    if P1.life <= 0:
                        print("P2 win")
                        run = False
        else:
            t_flag = 0

        #無敵時間
        if invince_time > 0:
            invince_time -= 1
        if state != state_flag:
            invince_time = 0
            state_flag = state

        #玩家速度控制
        P1.setspeed()
        P2.setspeed()

        #玩家移動
        P1.turn_move(key, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d)
        P2.turn_move(key, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT)
        #P1碰撞邊界
        if P1.x - player_size / 2 < bg_width:
            P1.x = screen_width - bg_width - player_size / 2
        elif P1.x + player_size / 2 > screen_width - bg_width:
            P1.x = bg_width + player_size / 2
        if P1.y - player_size / 2 < bg_height:
            P1.y = screen_height - bg_height - player_size / 2
        elif P1.y + player_size / 2 > screen_height - bg_height:
            P1.y = bg_height + player_size / 2
        #P2碰撞邊界
        if P2.x - player_size / 2 < bg_width:
            P2.x = screen_width - bg_width - player_size / 2
        elif P2.x + player_size / 2 > screen_width - bg_width:
            P2.x = bg_width + player_size / 2
        if P2.y - player_size / 2 < bg_height:
            P2.y = screen_height - bg_height - player_size / 2
        elif P2.y + player_size / 2 > screen_height - bg_height:
            P2.y = bg_height + player_size / 2


        #繪製玩家
        if state == 0:
            P2.drift(screen, img_sp[1 - state])
            P2.draw(screen, img_player2[1 - state], invince_time)
            P1.drift(screen, img_sp[state])
            P1.draw(screen, img_player1[state], invince_time)
        else:
            P1.drift(screen, img_sp[state])
            P1.draw(screen, img_player1[state], invince_time)
            P2.drift(screen, img_sp[1 - state])
            P2.draw(screen, img_player2[1 - state], invince_time)
        #--------------------------------------------------


        #------------draw border--------
        pygame.draw.rect(screen, side_color[state], (bg_width, bg_height + time_y, screen_width - 2 * bg_width, screen_height - 2 * bg_height - time_y), thickness)
        pygame.draw.rect(screen, side_color[1 - state], (0, 0, screen_width, bg_height + time_y))
        pygame.draw.rect(screen, side_color[1 - state], (0, 0, bg_width, screen_height))
        pygame.draw.rect(screen, side_color[1 - state], (0, screen_height - bg_height, screen_width, bg_height))
        pygame.draw.rect(screen, side_color[1 - state], (screen_width - bg_width, 0, bg_width, screen_height))
        p1_pos = (bg_width - player_size - tweak, screen_height - player_size - tweak)
        screen.blit(img_player1[state], p1_pos)
        for i in range(P1.life):
            screen.blit(Life[state], (p1_pos[0] + (player_size - heart_size) / 2, p1_pos[1] - heart_size * (i + 1)))
        p2_pos = (screen_width - bg_width + tweak, screen_height - player_size - tweak)
        screen.blit(img_player2[1 - state], p2_pos)
        for i in range(P2.life):
            screen.blit(Life[1 - state], (p2_pos[0] + (player_size - heart_size) / 2, p1_pos[1] - heart_size * (i + 1)))
        #--------------------------------


        #------繪製名字-------
        p1_text = font.render("P1", True, bg_color[1 - state])
        p2_text = font.render("P2", True, bg_color[1 - state])
        if state == 0:
            screen.blit(p2_text, (P2.x - (player_size / 5), P2.y - player_size))
            screen.blit(p1_text, (P1.x - (player_size / 5), P1.y - player_size))
        else:
            screen.blit(p1_text, (P1.x - (player_size / 5), P1.y - player_size))
            screen.blit(p2_text, (P2.x - (player_size / 5), P2.y - player_size))
        #--------------------------------

        #更新時間
        time += 1
        pygame.draw.rect(screen, bg_color[1 - state], [(screen_width - time_width) / 2, time_y, time_width * time / len, time_height], 0)
        pygame.draw.rect(screen, bg_color[1 - state], [(screen_width - time_width) / 2, time_y, time_width, time_height], int(time_height / 5))
        #----------------------

if __name__ == '__main__':
    game_play()	