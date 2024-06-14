import pygame
import cv2
import time

pygame.init()

#設定顏色
white = (255,255,255)
black = (0, 0, 0)
gray = (128, 128, 128)


#設定畫面大小   
screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)
clock = pygame.time.Clock()
fps = 80
window_width = 800


#設定顏色差異、按鈕寬度、按鈕間距
color_differece = 30
button_width = 100
button_distance = 150
button_y = 420

volume_width, volume_height = 500, 15 #音量條寬高
volume_y = 160 #音量條y座標

attack_volume_width, attack_volume_height = 500, 15 #攻擊音量條寬高
attack_volume_y = 320 #攻擊音量條y座標

text_size = 60
font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", text_size) #字體
volume_text = font.render('Volume', True, gray) #設定音量文字
attack_volume_text = font.render('Attack Volume', True, gray) #設定攻擊音量文字


#讀取圖片
pause_img = cv2.imread('src/images/pause.png')
pause_B, pause_G, pause_R = cv2.split(pause_img)
img_pause = []
return_img = cv2.imread('src/images/return.png')
return_B, return_G, return_R = cv2.split(return_img)
img_return = []
home_img = cv2.imread('src/images/home.png')
home_B, home_G, home_R = cv2.split(home_img)
img_home = []
for i in range(2):
    img_pause.append(cv2.merge([pause_B - color_differece * i, pause_B - color_differece * i, pause_B - color_differece * i]))
    img_return.append(cv2.merge([return_B - color_differece * i, return_B - color_differece * i, return_B - color_differece * i]))
    img_home.append(cv2.merge([home_B - color_differece * i, home_B - color_differece * i, home_B - color_differece * i]))
background_color = [(0, 0, 0), (256 - color_differece, 256 - color_differece, 256 - color_differece)]

#設定變數
p = 0
r = 0
h = 0


def pause_game(screen, volume, attack_volume, state):

    #設定透視視窗
    window = pygame.Surface((window_width, screen_height))
    window.fill((255, 255, 255))
    if state == 0:
        window.set_alpha(128)
    else:
        window.set_alpha(200)
    screen.blit(window, ((screen_width - window_width) // 2, 0))
    
    debounce_time = 0.3 #按鍵去抖的時間間隔（以秒為單位）
    last_key_press_time = {} #記錄按鍵最後按下的時間
    
    run = True
    while run:

        #時間揁數
        clock.tick(fps)
        #更新畫面
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE:
                    run = False
                current_time = time.time()
                key = event.key
                # 檢查按鍵是否在去抖時間間隔內
                if key in last_key_press_time:
                    if current_time - last_key_press_time[key] < debounce_time:
                        continue  # 如果在去抖時間內，跳過這個按鍵事件
                
                # 記錄按鍵按下的時間
                last_key_press_time[key] = current_time

                #處理按鍵事件
                if key == pygame.K_SPACE or key == pygame.K_RETURN:
                    return 0, volume, attack_volume
        
        
        
        #滑鼠事件
        m_x, m_y = pygame.mouse.get_pos()
        if m_x >= screen_width // 2 - button_distance - button_width // 2 and m_x <= screen_width // 2 - button_distance + button_width // 2 and button_y <= m_y <= button_y + button_width:
            p = 1
            if pygame.mouse.get_pressed()[0]:
                return 0, volume, attack_volume
        else:
            p = 0

        if screen_width // 2 - button_width // 2 <= m_x <= screen_width // 2 + button_width // 2 and button_y <= m_y <= button_y + button_width:
            r = 1
            if pygame.mouse.get_pressed()[0]:
                return 1, volume, attack_volume
        else:
            r = 0

        if screen_width // 2 + button_distance - button_width // 2 <= m_x <= screen_width // 2 + button_distance + button_width // 2 and button_y <= m_y <= button_y + button_width:
            h = 1
            if pygame.mouse.get_pressed()[0]:
                return 2, volume, attack_volume
        else:
            h = 0
        #------------------------------------------------


        #滑鼠控制音量
        #screen_width - volume_width) // 2, volume_y, volume_width, volume_height
        if screen_width // 2 - volume_width // 2 < m_x < screen_width // 2 + volume_width // 2 and volume_y < m_y < volume_y + volume_height and pygame.mouse.get_pressed()[0]:
            volume = (m_x - (screen_width - volume_width) // 2) / volume_width
        if screen_width // 2 - attack_volume_width // 2 < m_x < screen_width // 2 + attack_volume_width // 2 and attack_volume_y < m_y < attack_volume_y + attack_volume_height and pygame.mouse.get_pressed()[0]:
            attack_volume = (m_x - (screen_width - attack_volume_width) // 2) / attack_volume_width


        #畫出按鈕
        pause_surface = pygame.surfarray.make_surface(cv2.rotate(img_pause[p], cv2.ROTATE_90_CLOCKWISE))
        if p == 0:
            pause_surface.set_colorkey(background_color[0])
        else:
            pause_surface.set_colorkey(background_color[1])
        pause_surface = pygame.transform.scale(pause_surface, (button_width, button_width))
        screen.blit(pause_surface, (screen_width // 2 - button_distance - button_width // 2, button_y))
        
        return_surface = pygame.surfarray.make_surface(cv2.flip(img_return[r], 1))
        if r == 0:
            return_surface.set_colorkey(background_color[0])
        else:
            return_surface.set_colorkey(background_color[1])
        return_surface = pygame.transform.scale(return_surface, (button_width, button_width))
        screen.blit(return_surface, (screen_width // 2 - button_width // 2, button_y))

        home_surface = pygame.surfarray.make_surface(cv2.rotate(img_home[h], cv2.ROTATE_90_COUNTERCLOCKWISE))
        if h == 0:
            home_surface.set_colorkey(background_color[0])
        else:
            home_surface.set_colorkey(background_color[1])
        home_surface = pygame.transform.scale(home_surface, (button_width, button_width))
        screen.blit(home_surface, (screen_width // 2 + button_distance - button_width // 2, button_y))
        #------------------------------------------------


        #畫出音量條
        #畫出音量文字
        volume_text_rect = volume_text.get_rect(center=(screen_width // 2, volume_y - text_size // 2))
        screen.blit(volume_text, volume_text_rect)
        pygame.draw.rect(screen, white, [(screen_width - volume_width) // 2, volume_y, volume_width, volume_height], 0)
        pygame.draw.rect(screen, gray, [(screen_width - volume_width) // 2, volume_y, volume_width * volume, volume_height], 0)
        pygame.draw.circle(screen, gray, (int((screen_width - volume_width) // 2 + volume_width * volume), volume_y + volume_height // 2), volume_height // 2)
        pygame.draw.rect(screen, gray, [(screen_width - volume_width) // 2, volume_y, volume_width, volume_height], volume_height // 5)
        
        #畫出攻擊音量條
        attack_volume_text_rect = attack_volume_text.get_rect(center=(screen_width // 2, attack_volume_y - text_size // 2))
        screen.blit(attack_volume_text, attack_volume_text_rect)
        pygame.draw.rect(screen, white, [(screen_width - attack_volume_width) // 2, attack_volume_y, attack_volume_width, attack_volume_height], 0)
        pygame.draw.rect(screen, gray, [(screen_width - attack_volume_width) // 2, attack_volume_y, attack_volume_width * attack_volume, attack_volume_height], 0)
        pygame.draw.circle(screen, gray, (int((screen_width - attack_volume_width) // 2 + attack_volume_width * attack_volume), attack_volume_y + attack_volume_height // 2), attack_volume_height // 2)
        pygame.draw.rect(screen, gray, [(screen_width - attack_volume_width) // 2, attack_volume_y, attack_volume_width, attack_volume_height], attack_volume_height // 5)
        

        #滑鼠顯示
        pygame.mouse.set_visible(True)
        
    return 0, volume, attack_volume