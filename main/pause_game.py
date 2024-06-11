import pygame
import cv2

pygame.init()

#設定畫面大小   
screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)
clock = pygame.time.Clock()
fps = 80

#設定顏色差異、按鈕寬度、按鈕間距
color_differece = 20
button_width = 200
button_distance = 150

volume_width, volume_height = 700, 10 #音量條寬高
volume_y = 50 #音量條y座標

attack_volume_width, attack_volume_height = 700, 10 #攻擊音量條寬高
attack_volume_y = 100 #攻擊音量條y座標

#讀取圖片
pause_img = cv2.imread('src/images/pause.png')
pause_B, pause_G, pause_R = cv2.split(pause_img)
img_pause = []
return_img = cv2.imread('src/images/return.png')
return_B, return_G, return_R = cv2.split(return_img)
img_return = []
for i in range(2):
    img_pause.append(cv2.merge([pause_B - color_differece * i, pause_B - color_differece * i, pause_B - color_differece * i]))
    img_return.append(cv2.merge([return_B - color_differece * i, return_B - color_differece * i, return_B - color_differece * i]))

#設定變數
p = 0
r = 0

def pause_game(screen, volume, attack_volume):
    window = pygame.Surface(screen_size)
    window.fill((255, 255, 255))
    window.set_alpha(128)
    screen.blit(window, (0, 0))
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
        
        #鍵盤事件
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            return 0, volume, attack_volume
        
        #滑鼠事件
        m_x, m_y = pygame.mouse.get_pos()
        if screen_width // 2 - button_distance - button_width // 2 < m_x < screen_width // 2 - button_distance + button_width // 2 and screen_height // 2 < m_y < screen_height // 2 + button_width:
            p = 1
            if pygame.mouse.get_pressed()[0]:
                return 0, volume, attack_volume
        else:
            p = 0
        if screen_width // 2 + button_distance - button_width // 2 < m_x < screen_width // 2 + button_distance + button_width // 2 and screen_height // 2 < m_y < screen_height // 2 + button_width:
            r = 1
            if pygame.mouse.get_pressed()[0]:
                return 1, volume, attack_volume
        else:
            r = 0
        
        
        #畫出按鈕
        pause_surface = pygame.surfarray.make_surface(cv2.rotate(img_pause[p], cv2.ROTATE_90_CLOCKWISE))
        if p == 0:
            pause_surface.set_colorkey((0, 0, 0))
        else:
            pause_surface.set_colorkey((236, 236, 236))
        pause_surface = pygame.transform.scale(pause_surface, (button_width, button_width))
        screen.blit(pause_surface, (screen_width // 2 - button_distance - button_width // 2, screen_height // 2))
        
        return_surface = pygame.surfarray.make_surface(cv2.flip(img_return[r], 1))
        if r == 0:
            return_surface.set_colorkey((0, 0, 0))
        else:
            return_surface.set_colorkey((236, 236, 236))
        return_surface = pygame.transform.scale(return_surface, (button_width, button_width))
        screen.blit(return_surface, (screen_width // 2 + button_distance - button_width // 2, screen_height // 2))

        #畫出音量條
        pygame.draw.rect(screen, (255, 255, 255), [(screen_width - volume_width) // 2, volume_y, volume_width, volume_height], 0)
        pygame.draw.rect(screen, (0, 0, 0), [(screen_width - volume_width) // 2, volume_y, volume_width * volume, volume_height], 0)
        pygame.draw.rect(screen, (0, 0, 0), [(screen_width - volume_width) // 2, volume_y, volume_width, volume_height], 2)
        
        #畫出攻擊音量條
        pygame.draw.rect(screen, (255, 255, 255), [(screen_width - attack_volume_width) // 2, attack_volume_y, attack_volume_width, attack_volume_height], 0)
        pygame.draw.rect(screen, (0, 0, 0), [(screen_width - attack_volume_width) // 2, attack_volume_y, attack_volume_width * attack_volume, attack_volume_height], 0)
        pygame.draw.rect(screen, (0, 0, 0), [(screen_width - attack_volume_width) // 2, attack_volume_y, attack_volume_width, attack_volume_height], 2)
        

    return 0, volume, attack_volume