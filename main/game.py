import pygame
import cv2
import math
import random
import time
from player import player
from pause_game import pause_game
from coun_down import count_down

#初始化
pygame.init()
pygame.mixer.init()

#設定顏色
white = (255,255,255)
black = (0, 0, 0)

#background color
b_color_all = [[(244, 224, 244), (93, 29, 104)], #(229, 159, 228), (124, 55, 136)
            [(199, 244, 255), (4, 93, 125)], #(159, 229, 228), (55, 124, 136)
            [(255, 172, 170), (108, 21, 30)], #(229, 228, 159), (124, 136, 55)
            [(224, 244, 224), (29, 93, 29)]] #(159, 229, 159), (55, 124, 55)
s_color_all = [[(93, 29, 104), (255, 226, 251)],
              [(4, 93, 125), (201, 255, 255)],
              [(108, 21, 30), (255, 183, 177)],
              [(29, 93, 29), (226, 255, 226)]] #邊界顏色
rm_back = [(0, 0, 0), (231, 0, 96), (79, 184, 182), (0, 0, 0)]
#------------------------------------------------

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

#重複
repeat = 0

#音量
volume = 0.3
change_volume = volume / 2
attack_volume = 0.3

#效果
effects = 4
st_rate = [1, 1] #換場率 1/4
adsp_rate = [2, 2] #衝刺率 1/4
size_rate = [3, 3] #大小率 1/4
hp_rate = [4, 4] #加生命值率 1/4

#道具效果
or_max_speed = 8 #原始最大速度
or_min_speed = 3 #原始最小速度
pr_max_adsp = 15 #最大速度
pr_min_adsp = 7 #最小速度
adsp_time = 500 #衝次時間
pr_size = 2 #大小
size_time = 1000 #大小變化時間
max_life = 8 #最大生命值

#主程式
def game_play(play_state):

    #設定變數
    color = play_state[0]
    p1_face = play_state[1]
    p2_face = play_state[2]

    #音量設定
    global volume
    global change_volume
    global attack_volume

    #---------背景設定---------
    player_size = 60 #玩家大小
    P1_size = 60 #玩家1大小
    P2_size = 60 #玩家2大小
    sp_size = 40 #衝刺物件大小
    heart_size = 40 #生命值圖片大小
    time_width, time_height = 700, 10 #時間軸大小
    time_y = 30 #時間軸位置
    bg_width, bg_height = 100, 20 #場地大小
    thickness = 40 #邊界寬度
    bg_color = b_color_all[color] #背景顏色
    side_color = s_color_all[color] #邊界顏色
    tweak = 10 #調整位置
    font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", int(player_size * 3 / 5)) #字體
    text_distance = 30 #文字間距
    min_speed = 3 #玩家最小速度
    #--------------------------------

    #---------道具設定---------
    prop_size = 50 #道具大小
    prop_x_min = bg_width + thickness + prop_size // 2
    prop_x_max = screen_width - bg_width - thickness - prop_size // 2
    prop_y_min = bg_height + time_y + thickness + prop_size // 2
    prop_y_max = screen_height - bg_height - thickness - prop_size // 2
    prop_x = 0
    prop_y = 0


    #---------狀態設定---------
    t = 0 #時間
    state = 0 #0:攻擊 1:防禦
    state_flag = 0 #狀態轉換
    flag = [0, 0] #0:未按下 1:按下
    song_flag = 0 #轉換音樂
    t_flag = 0 #0:未碰撞 1:碰撞
    invince_time = 0 #無敵時間
    invince_time_max = 150 #無敵時間上限
    pause_times = 0 #暫停次數
    debounce_time = 0.3 #去抖時間
    last_key_press_time = {} #最後按下時間
    prop_touch = False #道具碰撞
    prop_effect = -1 #道具效果
    pr_adsp = 0 #道具衝刺時間
    pr_size_time = 0 #道具大小時間
    cd = 3 #倒數時間
    count = 0 #倒數
    #--------------------------------


    #---------玩家設定---------
    #設定玩家圖片
    img_player1 = []
    img_player2 = []
    
    #faces img load
    face_P1 = []
    face_P2 = []
    
    #設定衝刺物件圖片
    img_sp = []
    
    #生命值圖片
    Life = []

    #load images
    if color == 0:
        for i in range(2):
            #body
            img = pygame.image.load('src/images/Player' + str(i) + '.png')
            img.set_colorkey(rm_back[color])
            img = pygame.transform.scale(img, (player_size, player_size))
            img_player1.append(img)
            img = pygame.image.load('src/images/Player' + str(i) + '.png')
            img.set_colorkey(rm_back[color])
            img = pygame.transform.scale(img, (player_size, player_size))
            img_player2.append(img)   
            
            #face
            img = pygame.image.load('src/images/face/' + str(p1_face) + str(i) + '.png')
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P1.append(img)
            img = pygame.image.load('src/images/face/' + str(p2_face) + str(i) + '.png')
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P2.append(img)

            #sprint
            img = pygame.image.load('src/images/Sp' + str(i) + '.png')
            img.set_colorkey(rm_back[color])
            img_sp.append(pygame.transform.scale(img, (sp_size, sp_size)))

            #life
            img = pygame.image.load('src/images/Lif' + str(i) + '.png')
            img.set_colorkey(rm_back[color])
            Life.append(pygame.transform.scale(img, (heart_size, heart_size)))

    elif color == 1:
        for i in range(2):
            #body
            img = cv2.imread('src/images/Player' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G - 25, R, G + 96])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            img_player1.append(img)
            img = cv2.imread('src/images/Player' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G - 25, R, G + 96])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            img_player2.append(img)

            #face
            img = cv2.imread('src/images/face/' + str(p1_face) + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G - 25, R, G + 96])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P1.append(img)
            img = cv2.imread('src/images/face/' + str(p2_face) + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G - 25, R, G + 96])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P2.append(img)

            #sprint
            img = cv2.imread('src/images/Sp' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G - 25, R, G + 96])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (sp_size, sp_size))
            img.set_colorkey(rm_back[color])
            img_sp.append(img)

            #life
            img = cv2.imread('src/images/Lif' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G - 25, R, G + 96])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (heart_size, heart_size))
            img.set_colorkey(rm_back[color])
            Life.append(img)

    elif color == 2:
        for i in range(2):
            #body
            img = cv2.imread('src/images/Player' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G + 79, B - 72, R - 74])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            img_player1.append(img)
            img = cv2.imread('src/images/Player' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G + 79, B - 72, R - 74])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            img_player2.append(img)

            #face
            img = cv2.imread('src/images/face/' + str(p1_face) + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G + 79, B - 72, R - 74])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)) 
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P1.append(img)
            img = cv2.imread('src/images/face/' + str(p2_face) + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G + 79, B - 72, R - 74])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P2.append(img)

            #sprint
            img = cv2.imread('src/images/Sp' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G + 79, B - 72, R - 74])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (sp_size, sp_size))
            img.set_colorkey(rm_back[color])
            img_sp.append(img)

            #life
            img = cv2.imread('src/images/Lif' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G + 79, B - 72, R - 74])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (heart_size, heart_size))
            img.set_colorkey(rm_back[color])
            Life.append(img)

    else:
        for i in range(2):
            #body
            img = cv2.imread('src/images/Player' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G, R, G])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            img_player1.append(img)
            img = cv2.imread('src/images/Player' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G, R, G])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            img_player2.append(img)

            #face
            img = cv2.imread('src/images/face/' + str(p1_face) + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G, R, G])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P1.append(img)
            img = cv2.imread('src/images/face/' + str(p2_face) + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G, R, G])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (player_size, player_size))
            img.set_colorkey(rm_back[color])
            face_P2.append(img)

            #sprint
            img = cv2.imread('src/images/Sp' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G, R, G])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (sp_size, sp_size))
            img.set_colorkey(rm_back[color])
            img_sp.append(img)

            #life
            img = cv2.imread('src/images/Lif' + str(i) + '.png')
            B, G, R = cv2.split(img)
            img = cv2.merge([G, R, G])
            img = pygame.surfarray.make_surface(cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            img = pygame.transform.scale(img, (heart_size, heart_size))
            img.set_colorkey(rm_back[color])
            Life.append(img)

    
    #玩家基本設定
    P1 = player(bg_width + thickness + player_size, screen_height / 2 + time_y,
                min_speed, 0, 8, 0, 0, [0, 0, 0])
    P2 = player(screen_width - bg_width - thickness - player_size, screen_height / 2 + time_y,
                min_speed, 0, 8, 1, 0, [0, 0, 0])
    #--------------------------------


    #---------音樂設定---------
    #背景音樂
    song = ['src/sound/song' + str(color) + '/0.wav', 'src/sound/song' + str(color) + '/1.wav']
    #volume = 0.3
    pygame.mixer.music.set_volume(volume)
    len = int(pygame.mixer.Sound(song[0]).get_length() * fps)
    
    #轉場音效
    change = pygame.mixer.Sound('src/sound/change.wav')
    #change_volume = volume / 3
    change.set_volume(change_volume)

    #碰撞音效
    attack = pygame.mixer.Sound('src/sound/attack.wav')
    #attack_volume = 0.3
    attack.set_volume(attack_volume)

    #道具音效
    prop = pygame.mixer.Sound('src/sound/prop.wav')
    prop.set_volume(attack_volume)
    #--------------------------------


    #---------遊戲迴圈---------
    run = True
    while run:

    

        
        #---------基礎設定---------
        #時間揁數
        clock.tick(fps)
        #更新畫面
        pygame.display.flip()
        screen.fill(bg_color[state])

        #繪製玩家
        if state == 0:
            P2.drift(screen, pygame.transform.scale(img_sp[1 - state], (sp_size * P2_size // player_size, sp_size * P2_size // player_size)))
            P1.drift(screen, pygame.transform.scale(img_sp[state], (sp_size * P1_size // player_size, sp_size * P1_size // player_size)))
            P2.draw(screen, img_player2[1 - state], face_P2[1 - state], invince_time, P2_size)
            P1.draw(screen, img_player1[state], face_P1[state], invince_time, P1_size)
        else:
            P1.drift(screen, pygame.transform.scale(img_sp[state], (sp_size * P1_size // player_size, sp_size * P1_size // player_size)))
            P2.drift(screen, pygame.transform.scale(img_sp[1 - state], (sp_size * P2_size // player_size, sp_size * P2_size // player_size)))
            P1.draw(screen, img_player1[state], face_P1[state], invince_time, P1_size)
            P2.draw(screen, img_player2[1 - state], face_P2[1 - state], invince_time, P2_size)
        #--------------------------------------------------


        #------------draw border--------
        pygame.draw.rect(screen, side_color[state], (bg_width, bg_height + time_y, screen_width - 2 * bg_width, screen_height - 2 * bg_height - time_y), thickness)
        pygame.draw.rect(screen, side_color[1 - state], (0, 0, screen_width, bg_height + time_y))
        pygame.draw.rect(screen, side_color[1 - state], (0, 0, bg_width, screen_height))
        pygame.draw.rect(screen, side_color[1 - state], (0, screen_height - bg_height, screen_width, bg_height))
        pygame.draw.rect(screen, side_color[1 - state], (screen_width - bg_width, 0, bg_width, screen_height))
        #--------------------------------
        
        
        #------------draw life--------
        p1_pos = (bg_width - player_size - tweak, screen_height - player_size - tweak)
        screen.blit(img_player1[state], p1_pos)
        screen.blit(face_P1[state], p1_pos)
        for i in range(P1.life):
            screen.blit(Life[state], (p1_pos[0] + (player_size - heart_size) / 2, p1_pos[1] - heart_size * (i + 1)))
        
        p2_pos = (screen_width - bg_width + tweak, screen_height - player_size - tweak)
        screen.blit(img_player2[1 - state], p2_pos)
        screen.blit(face_P2[1 - state], p2_pos)
        for i in range(P2.life):
            screen.blit(Life[1 - state], (p2_pos[0] + (player_size - heart_size) / 2, p1_pos[1] - heart_size * (i + 1)))
        #--------------------------------


        #------繪製名字-------
        p1_text = font.render("P1", True, bg_color[1 - state])
        p2_text = font.render("P2", True, bg_color[1 - state])
        if state == 0:
            screen.blit(p2_text, (P2.x - (player_size // 5), P2.y - P2_size // 2 - text_distance))
            #screen.blit(p1_text, (P1.x - (P1_size / 5), P1.y - P1_size))
            screen.blit(p1_text, (P1.x - (player_size // 5), P1.y - P1_size // 2 - text_distance))
        else:
            screen.blit(p1_text, (P1.x - (player_size // 5), P1.y - P1_size // 2 - text_distance))
            screen.blit(p2_text, (P2.x - (player_size // 5), P2.y - P2_size // 2 - text_distance))
        #--------------------------------

        #------繪製時間軸-------
        if state == 0:
            pygame.draw.rect(screen, bg_color[1 - state], [(screen_width - time_width) / 2, time_y, time_width * t / len, time_height], 0)
            pygame.draw.rect(screen, bg_color[1 - state], [(screen_width - time_width) / 2, time_y, time_width, time_height], int(time_height / 5))
            pygame.draw.circle(screen, bg_color[state], ((screen_width - time_width) / 2 + time_width * t / len, time_y + time_height / 2), time_height)
            pygame.draw.circle(screen, bg_color[1 - state], ((screen_width - time_width) / 2 + time_width * t / len, time_y + time_height / 2), time_height, int(time_height / 5))
        else:
            pygame.draw.rect(screen, bg_color[1 - state], [(screen_width - time_width) / 2, time_y, time_width * (1 - t / len), time_height], 0)
            pygame.draw.rect(screen, bg_color[1 - state], [(screen_width - time_width) / 2, time_y, time_width, time_height], int(time_height / 5))
            pygame.draw.circle(screen, bg_color[state], ((screen_width - time_width) / 2 + time_width * (1 - t / len), time_y + time_height / 2), time_height)
            pygame.draw.circle(screen, bg_color[1 - state], ((screen_width - time_width) / 2 + time_width * (1 - t / len), time_y + time_height / 2), time_height, int(time_height / 5))
        #--------------------------------

        if cd >= 0:
            count = count_down(cd, color, volume, count)
            if count == 60:
                cd -= 1
                count = 0
            continue

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    run = False
                current_time = time.time()
                key_space = event.key
                # 檢查按鍵是否在去抖時間間隔內
                if key_space in last_key_press_time:
                    if current_time - last_key_press_time[key_space] < debounce_time:
                        continue  # 如果在去抖時間內，跳過這個按鍵事件
                
                # 記錄按鍵按下的時間
                last_key_press_time[key_space] = current_time
                
                # 處理按鍵事件
                if key_space == pygame.K_SPACE or key_space == pygame.K_RETURN:
                    pygame.mixer.music.pause()
                    pause_times += 1
                    repeat, volume, attack_volume = pause_game(screen, volume, attack_volume, state)
                    change_volume = volume / 2
                    if repeat == 1:
                        pygame.mixer.music.stop()
                        return repeat
                    elif repeat == 2:
                        pygame.mixer.music.stop()
                        return repeat
                    else:
                        pygame.mixer.music.set_volume(volume)
                        change.set_volume(volume / 3)
                        attack.set_volume(attack_volume)
                        pygame.mixer.music.unpause()
                        if pause_times < 50: #避免延遲
                            t -= 1
        #--------------------------------

        
        if st_rate[0] <= prop_effect <= st_rate[1]:
            t = 0
            pygame.mixer.music.stop()

        #-------音樂播放、狀態轉換-------
        if t % 2 == 0:
            if pygame.mixer.music.get_busy():
                song_flag = 0
            else:
                #print(pygame.mixer.Channel(0).get_busy())
                if song_flag == 0:
                    #pygame.mixer.music.stop()
                    t = 0
                    change.play()
                    if not cd == -1:
                        state = 1 - state
                    else:
                        cd -= 1
                    P1.state = state
                    P2.state = 1 - state    
                    pygame.mixer.music.load(song[state])
                    pygame.mixer.music.play()
                    song_flag = 1
                    pause_times = 0
                    prop_touch = 0
                    prop_effect = -1
                    prop_x = random.randint(prop_x_min, prop_x_max) #道具位置 中心
                    prop_y = random.randint(prop_y_min, prop_y_max) #道具位置 中心
        #--------------------------------



        #---------道具生成---------

        if not prop_touch:
            if abs(P1.x - prop_x) < (P1_size + prop_size) // 2 and abs(P1.y - prop_y) < (P1_size + prop_size) // 2:
                prop.play()
                prop_effect = random.randint(1, effects)
                print(prop_effect)
                prop_touch = 1
            if abs(P2.x - prop_x) < (P2_size + prop_size) // 2 and abs(P2.y - prop_y) < (P2_size + prop_size) // 2:
                prop.play()
                prop_effect = random.randint(1, effects)
                print(prop_effect)
            pygame.draw.rect(screen, (0, 0, 0), (prop_x - prop_size // 2, prop_y - prop_size // 2, prop_size, prop_size))


        if adsp_rate[0] <= prop_effect <= adsp_rate[1]:
            pr_adsp = adsp_time
            prop_effect = -1
        
        if size_rate[0] <= prop_effect <= size_rate[1]:
            pr_size_time = size_time
            prop_effect = -1
            prop_effect = -1

        if hp_rate[0] <= prop_effect <= hp_rate[1]:
            if prop_touch == 1 and P1.life < max_life:
                P1.life += 1
            elif prop_touch == 2 and P2.life < max_life:
                P2.life += 1
            prop_effect = -1

        if pr_adsp > 0:
            pr_adsp -= 1
            if prop_touch == 1:
                circle_surface = pygame.Surface((P1_size * 3 // 2, P1_size * 3 // 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 245, 223, 160), (P1_size * 3 // 4, P1_size * 3 // 4), P1_size * 3 // 4)
                screen.blit(circle_surface, (P1.x - P1_size * 3 // 4, P1.y - P1_size * 3 // 4))
                circle_surface = pygame.Surface((P1_size * 5 // 4, P1_size * 5 // 4), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 193, 128, 160), (P1_size * 5 // 8, P1_size * 5 // 8), P1_size * 5 // 8)
                screen.blit(circle_surface, (P1.x - P1_size * 5 // 8, P1.y - P1_size * 5 // 8))
                P1.max_speed = pr_max_adsp
                P1.min_speed = pr_min_adsp
            elif prop_touch == 2:
                circle_surface = pygame.Surface((P2_size * 3 // 2, P2_size * 3 // 2), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 245, 223, 160), (P2_size * 3 // 4, P2_size * 3 // 4), P2_size * 3 // 4)
                screen.blit(circle_surface, (P2.x - P2_size * 3 // 4, P2.y - P2_size * 3 // 4))
                circle_surface = pygame.Surface((P2_size * 5 // 4, P2_size * 5 // 4), pygame.SRCALPHA)
                pygame.draw.circle(circle_surface, (255, 193, 128, 160), (P2_size * 5 // 8, P2_size * 5 // 8), P2_size * 5 // 8)
                screen.blit(circle_surface, (P2.x - P2_size * 5 // 8, P2.y - P2_size * 5 // 8))
                P2.max_speed = pr_max_adsp
                P2.min_speed = pr_min_adsp
        else:
            P1.max_speed = or_max_speed
            P1.min_speed = or_min_speed
            P2.max_speed = or_max_speed
            P2.min_speed = or_min_speed

        if pr_size_time > 0:
            pr_size_time -= 1
            if prop_touch == 1:
                if state == 0:
                    P1_size = int(player_size * pr_size)
                else:
                    P1_size = int(player_size / pr_size)
            elif prop_touch == 2:
                if state == 1:
                    P2_size = int(player_size * pr_size)
                else:
                    P2_size = int(player_size / pr_size)
        else:
            P1_size = player_size
            P2_size = player_size


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
        if abs(P1.x - P2.x) < (P1_size + P2_size) // 2 and abs(P1.y - P2.y) < (P1_size + P2_size) // 2 and invince_time <= 0:
            if t_flag == 0:
                t_flag = 1
                attack.play()
                invince_time = invince_time_max
                if state == 0:
                    P2.life -= 1
                    if P2.life <= 0:
                        pygame.mixer.music.stop()
                        return 3
                        run = False
                else:
                    P1.life -= 1
                    if P1.life <= 0:
                        pygame.mixer.music.stop()
                        return 4
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
        if P1.x - P1_size / 2 < bg_width:
            P1.x = screen_width - bg_width - P1_size / 2
        elif P1.x + P1_size / 2 > screen_width - bg_width:
            P1.x = bg_width + P1_size / 2
        if P1.y - P1_size / 2 < bg_height + time_y:
            P1.y = screen_height - bg_height - P1_size / 2
        elif P1.y + P1_size / 2 > screen_height - bg_height:
            P1.y = bg_height + time_y + P1_size / 2
        #P2碰撞邊界
        if P2.x - P2_size / 2 < bg_width:
            P2.x = screen_width - bg_width - P2_size / 2
        elif P2.x + P2_size / 2 > screen_width - bg_width:
            P2.x = bg_width + P2_size / 2
        if P2.y - P2_size / 2 < bg_height + time_y:
            P2.y = screen_height - bg_height - P2_size / 2
        elif P2.y + P2_size / 2 > screen_height - bg_height:
            P2.y = bg_height + time_y + P2_size / 2




        #更新時間
        t += 1
        #----------------------

        #藏起滑鼠
        pygame.mouse.set_visible(False)

    pygame.mixer.music.stop()
    return 0

if __name__ == '__main__':
    repeat = 1
    while repeat:
        repeat = 0
        repeat = game_play((1, 0, 3))
        if repeat == 3:
            print("P1 win")
        elif repeat == 4:
            print("P2 win")
        if repeat > 1:
            break