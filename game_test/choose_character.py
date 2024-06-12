import pygame
import cv2
import time

#pygame初始化
pygame.init()

#screen size
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

#colors
white = (255, 255, 255)
black = (0, 0, 0)


#fps、clock
clock = pygame.time.Clock()
fps = 80

#text
font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 100) #字體
    

#background color
bg_color = [[(244, 224, 244), (93, 29, 104)], #(229, 159, 228), (124, 55, 136)
            [(199, 244, 255), (4, 93, 125)], #(159, 229, 228), (55, 124, 136)
            [(255, 172, 170), (108, 21, 30)], #(229, 228, 159), (124, 136, 55)
            [(224, 244, 224), (29, 93, 29)]] #(159, 229, 159), (55, 124, 55)
side_color = [[(93, 29, 104), (255, 226, 251)],
              [(4, 93, 125), (201, 255, 255)],
              [(108, 21, 30), (255, 183, 177)],
              [(29, 93, 29), (226, 255, 226)]] #邊界顏色
rm_back = [(0, 0, 0), (231, 0, 96), (79, 184, 182), (0, 0, 0)]


#img load
img_size = 200
distance = 300
tweak = 60
img0 = cv2.imread('src/images/Player0.png')
img1 = cv2.imread('src/images/Player1.png')
B0, G0, R0 = cv2.split(img0)
B1, G1, R1 = cv2.split(img1)
body_img = [[cv2.merge([B0, G0, R0]), cv2.merge([B1, G1, R1])], #original
            [cv2.merge([G0 - 25, R0, G0 + 96]), cv2.merge([G1 - 25, R1, G1 + 96])], #yellow
            [cv2.merge([G0 + 79, B0 - 72, R0 - 74]), cv2.merge([G1 + 79, B1 - 72, R1 - 74])], #blue
            [cv2.merge([G0, R0, G0]), cv2.merge([G1, R1, G1])]] #green
for i in range(4):
    for j in range(2):
        body_surface = pygame.surfarray.make_surface(cv2.rotate(body_img[i][j], cv2.ROTATE_90_COUNTERCLOCKWISE))
        body_surface.set_colorkey(rm_back[i])
        body_img[i][j] = pygame.transform.scale(body_surface, (img_size, img_size))

#方向圖片
color_differece = 30
direction_size = 160
direction_img = cv2.imread('src/images/Direction.png')
B, G, R = cv2.split(direction_img)

img_direction = [[],[]]
tmp = pygame.surfarray.make_surface(cv2.rotate(cv2.merge([B, B, B]), cv2.ROTATE_90_COUNTERCLOCKWISE))
tmp.set_colorkey((0, 0, 0))
tmp = pygame.transform.scale(tmp, (direction_size // 2, direction_size))
img_direction[0].append(tmp)

tmp = pygame.surfarray.make_surface(cv2.rotate(cv2.merge([B - color_differece, B - color_differece, B - color_differece]), cv2.ROTATE_90_COUNTERCLOCKWISE))
tmp.set_colorkey((256 - color_differece, 256 - color_differece, 256 - color_differece))
tmp = pygame.transform.scale(tmp, (direction_size // 2, direction_size))
img_direction[0].append(tmp)

tmp = pygame.surfarray.make_surface(cv2.rotate(cv2.merge([B - color_differece * 2, B - color_differece * 2, B - color_differece * 2]), cv2.ROTATE_90_COUNTERCLOCKWISE))
tmp.set_colorkey((256 - color_differece * 2, 256 - color_differece * 2, 256 - color_differece * 2))
tmp = pygame.transform.scale(tmp, (direction_size // 2, direction_size))
img_direction[0].append(tmp)


tmp = pygame.surfarray.make_surface(cv2.rotate(cv2.merge([B, B, B]), cv2.ROTATE_90_CLOCKWISE))
tmp.set_colorkey((0, 0, 0))
tmp = pygame.transform.scale(tmp, (direction_size // 2, direction_size))
img_direction[1].append(tmp)

tmp = pygame.surfarray.make_surface(cv2.rotate(cv2.merge([B - color_differece, B - color_differece, B - color_differece]), cv2.ROTATE_90_CLOCKWISE))
tmp.set_colorkey((256 - color_differece, 256 - color_differece, 256 - color_differece))
tmp = pygame.transform.scale(tmp, (direction_size // 2, direction_size))
img_direction[1].append(tmp)

tmp = pygame.surfarray.make_surface(cv2.rotate(cv2.merge([B - color_differece * 2, B - color_differece * 2, B - color_differece * 2]), cv2.ROTATE_90_CLOCKWISE))
tmp.set_colorkey((256 - color_differece * 2, 256 - color_differece * 2, 256 - color_differece * 2))
tmp = pygame.transform.scale(tmp, (direction_size // 2, direction_size))
img_direction[1].append(tmp)


def choose_color():
    bg_choice = 0 #背景選擇
    bg_width, bg_height = 100, 20 #場地大小
    time_y = 30 #時間軸位置
    thickness = 40 #邊界寬度
    state = 0 #狀態
    t = 0 #時間
    left = 0
    right = 0
    enter = 0

    #設定透視視窗
    window = pygame.Surface((screen_width, screen_height))
    window.fill((0, 0, 0))
    window.set_alpha(100)

    # 設置按鍵去抖的時間間隔（以秒為單位）
    debounce_time = 0.3

    # 記錄按鍵最後按下的時間
    last_key_press_time = {}

    # Initialize the last click time
    last_click_time = 0

    run = True
    while run:
        
        #滑鼠事件
        m_x, m_y = pygame.mouse.get_pos()
        if distance <= m_x <= distance + direction_size // 2 and distance <= m_y <= distance + direction_size:
            left = 1
        else:
            left = 0
        
        if screen_width - distance - direction_size // 2 <= m_x <= screen_width - distance and distance <= m_y <= distance + direction_size:
            right = 1
        else:
            right = 0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
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
                
                # 處理按鍵事件
                if key == pygame.K_LEFT or key == pygame.K_a:
                    bg_choice -= 1
                    if bg_choice < 0:
                        bg_choice = 3
                if key == pygame.K_RIGHT or key == pygame.K_d:
                    bg_choice += 1
                    if bg_choice > 3:
                        bg_choice = 0
                elif key == pygame.K_SPACE or key == pygame.K_KP_ENTER:
                    return bg_choice
                # 可以在這裡添加其他按鍵處理
            elif event.type == pygame.MOUSEBUTTONDOWN:
                current_time = time.time()
                if current_time - last_click_time >= debounce_time:
                    if left >= 1:
                        left = 2
                        bg_choice -= 1
                        if bg_choice < 0:
                            bg_choice = 3
                        pygame.time.delay(300)
                    elif right >= 1:
                        right = 2
                        bg_choice += 1
                        if bg_choice > 3:
                            bg_choice = 0
                        pygame.time.delay(300)
                    if enter:
                        return bg_choice

                    last_click_time = current_time

        clock.tick(fps)
        pygame.display.flip()
        screen.fill(bg_color[bg_choice][state])

        #畫邊界
        pygame.draw.rect(screen, side_color[bg_choice][state], (bg_width, bg_height + time_y, screen_width - 2 * bg_width, screen_height - 2 * bg_height - time_y), thickness)
        pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, 0, screen_width, bg_height + time_y))
        pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, 0, bg_width, screen_height))
        pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, screen_height - bg_height, screen_width, bg_height))
        pygame.draw.rect(screen, side_color[bg_choice][1 - state], (screen_width - bg_width, 0, bg_width, screen_height))
        
        #透視視窗
        if state == 0:
            window.set_alpha(150)
        else:
            window.set_alpha(100)
        screen.blit(window, (0, 0))

        #字體
        text = font.render("Choose your court", True, white)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, time_y * 2))

        #選擇顏色
        rotated_img0 = pygame.transform.rotate(body_img[bg_choice][0], 20)
        rotated_img1 = pygame.transform.rotate(body_img[bg_choice][1], -20)
        if screen_width // 2 - img_size + tweak <= m_x <= screen_width // 2 - img_size // 2 + rotated_img1.get_width() and screen_height // 2 - img_size // 2 - bg_height <= m_y <= screen_height // 2 + bg_height + rotated_img1.get_height():
            enter = 1
            rotated_img0.set_alpha(180)
            rotated_img1.set_alpha(180)

        else:
            enter = 0
            rotated_img0.set_alpha(255)
            rotated_img1.set_alpha(255)
        screen.blit(rotated_img0, (screen_width // 2 - img_size + tweak, screen_height // 2 - img_size // 2 - bg_height))
        screen.blit(rotated_img1, (screen_width // 2 - img_size // 2, screen_height // 2 + bg_height))
        

        #方向
        screen.blit(img_direction[0][left], (distance, distance))
        screen.blit(img_direction[1][right], (screen_width - distance - direction_size // 2, distance))

        if t % 250 == 0:
            state = 1 - state
        
        t += 1


if __name__ == "__main__":
    print(choose_color())
    #choose_face()