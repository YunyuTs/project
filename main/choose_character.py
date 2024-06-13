import pygame
import cv2
import time

#pygame初始化
pygame.init()
#------------------------------------------------


#screen size
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
#------------------------------------------------


#colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
#------------------------------------------------


#fps、clock
clock = pygame.time.Clock()
fps = 80
#------------------------------------------------


#text
font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 100) #字體
direct_font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 50) #字體
#------------------------------------------------


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
#------------------------------------------------


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
#------------------------------------------------

#選表情大小
face_size = 120
face_tweack = 20
face_distance = 130
faces = 7
rate = 2

#方向圖片
color_differece = 30
direction_size = 120
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

#方向音效
direct = pygame.mixer.Sound('src/sound/direct.wav')
direct.set_volume(0.5)

#------------------------------------------------


def choose_color():
    bg_choice = 0 #背景選擇
    choosed = 0 #選擇完成
    bg_width, bg_height = 100, 20 #場地大小
    time_y = 30 #時間軸位置
    thickness = 40 #邊界寬度
    state = 0 #狀態
    t = 0 #時間
    left = 0
    right = 0
    enter = 0
    determine = 0

    P1_face = 0
    P2_face = 0

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

    #music
    music = pygame.mixer.music.load('src/sound/background.ogg')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    run = True
    while run:

        clock.tick(fps)
        pygame.display.flip()
        screen.fill(bg_color[bg_choice][state])

        #選擇場地
        if choosed == 0:
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
                

            #畫邊界
            pygame.draw.rect(screen, side_color[bg_choice][state], (bg_width, bg_height + time_y, screen_width - 2 * bg_width, screen_height - 2 * bg_height - time_y), thickness)
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, 0, screen_width, bg_height + time_y))
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, 0, bg_width, screen_height))
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, screen_height - bg_height, screen_width, bg_height))
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (screen_width - bg_width, 0, bg_width, screen_height))
            
            #透視視窗
            if state == 0:
                window.set_alpha(150)
                screen.blit(window, (0, 0))
                text = font.render("Choose your court", True, bg_color[bg_choice][1])
                pygame.draw.rect(screen, bg_color[bg_choice][0], (screen_width // 2 - text.get_width() // 2, time_y * 2, text.get_width(), text.get_height()))
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, time_y * 2))
            else:
                window.set_alpha(100)
                screen.blit(window, (0, 0))
                text = font.render("Choose your court", True, bg_color[bg_choice][0])
                pygame.draw.rect(screen, bg_color[bg_choice][1], (screen_width // 2 - text.get_width() // 2, time_y * 2, text.get_width(), text.get_height()))
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
                        direct.play()
                        bg_choice -= 1
                        if bg_choice < 0:
                            bg_choice = 3
                    if key == pygame.K_RIGHT or key == pygame.K_d:
                        direct.play()
                        bg_choice += 1
                        if bg_choice > 3:
                            bg_choice = 0
                    elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                        direct.play()
                        choosed = 1
                    # 可以在這裡添加其他按鍵處理
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    current_time = time.time()
                    if current_time - last_click_time >= debounce_time:
                        if left >= 1:
                            direct.play()
                            left = 2
                            bg_choice -= 1
                            if bg_choice < 0:
                                bg_choice = 3
                            pygame.time.delay(300)
                        elif right >= 1:
                            direct.play()
                            right = 2
                            bg_choice += 1
                            if bg_choice > 3:
                                bg_choice = 0
                            pygame.time.delay(300)
                        if enter:
                            direct.play()
                            choosed = 1

                        last_click_time = current_time

            #時間
            if t % 250 == 0:
                state = 1 - state
            t += 1


        #選擇表情
        else:
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
                    if key == pygame.K_SPACE or key == pygame.K_RETURN:
                        direct.play()
                        pygame.mixer.music.stop()
                        return bg_choice, P1_face, P2_face
                    
                    if key == pygame.K_LEFT or key == pygame.K_DOWN:
                        direct.play()
                        P2_face -= 1
                        if P2_face < 0:
                            P2_face = faces - 1
                    if key == pygame.K_RIGHT or key == pygame.K_UP:
                        direct.play()
                        P2_face += 1
                        if P2_face >= faces:
                            P2_face = 0

                    if key == pygame.K_a or key == pygame.K_s:
                        direct.play()
                        P1_face -= 1
                        if P1_face < 0:
                            P1_face = faces - 1
                    if key == pygame.K_d or key == pygame.K_w:
                        direct.play()
                        P1_face += 1
                        if P1_face > faces - 1:
                            P1_face = 0

                    if key == pygame.K_SPACE or key == pygame.K_RETURN:
                        direct.play()
                        pygame.mixer.music.stop()
                        return bg_choice, P1_face, P2_face
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    current_time = time.time()
                    if current_time - last_click_time >= debounce_time:
                        if determine:
                            direct.play()
                            pygame.mixer.music.stop()
                            return bg_choice, P1_face, P2_face
                        last_click_time = current_time
                    
            
            #畫邊界
            pygame.draw.rect(screen, side_color[bg_choice][state], (bg_width, bg_height + time_y, screen_width - 2 * bg_width, screen_height - 2 * bg_height - time_y), thickness)
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, 0, screen_width, bg_height + time_y))
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, 0, bg_width, screen_height))
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (0, screen_height - bg_height, screen_width, bg_height))
            pygame.draw.rect(screen, side_color[bg_choice][1 - state], (screen_width - bg_width, 0, bg_width, screen_height))
            
            #透視視窗
            if state == 0:
                window.set_alpha(150)
                screen.blit(window, (0, 0))
                text = font.render("Choose your faces", True, bg_color[bg_choice][1])
                pygame.draw.rect(screen, bg_color[bg_choice][0], (screen_width // 2 - text.get_width() // 2, time_y * 2, text.get_width(), text.get_height()))
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, time_y * 2))
                d_text_p1 = direct_font.render("P1 controls", True, bg_color[bg_choice][1])
                pygame.draw.rect(screen, bg_color[bg_choice][0], (face_size, face_size * 5 // 2, d_text_p1.get_width(), d_text_p1.get_height()))
                screen.blit(d_text_p1, (face_size, face_size * 5 // 2))
                d_text_p2 = direct_font.render("P2 controls", True, bg_color[bg_choice][1])
                pygame.draw.rect(screen, bg_color[bg_choice][0], (screen_width - face_size - d_text_p2.get_width(), face_size * 5 // 2, d_text_p2.get_width(), d_text_p2.get_height()))
                screen.blit(d_text_p2, (screen_width - face_size - d_text_p2.get_width(), face_size * 5 // 2))
            else:
                window.set_alpha(100)
                screen.blit(window, (0, 0))
                text = font.render("Choose your faces", True, bg_color[bg_choice][0])
                pygame.draw.rect(screen, bg_color[bg_choice][1], (screen_width // 2 - text.get_width() // 2, time_y * 2, text.get_width(), text.get_height()))
                screen.blit(text, (screen_width // 2 - text.get_width() // 2, time_y * 2))
                d_text_p1 = direct_font.render("P1 controls", True, bg_color[bg_choice][0])
                pygame.draw.rect(screen, bg_color[bg_choice][1], (face_size, face_size * 5 // 2, d_text_p1.get_width(), d_text_p1.get_height()))
                screen.blit(d_text_p1, (face_size, face_size * 5 // 2))
                d_text_p2 = direct_font.render("P2 controls", True, bg_color[bg_choice][0])
                pygame.draw.rect(screen, bg_color[bg_choice][1], (screen_width - face_size - d_text_p2.get_width(), face_size * 5 // 2, d_text_p2.get_width(), d_text_p2.get_height()))
                screen.blit(d_text_p2, (screen_width - face_size - d_text_p2.get_width(), face_size * 5 // 2))

                
            #字體
            # text = font.render("Choose your faces", True, white)
            # screen.blit(text, (screen_width // 2 - text.get_width() // 2, time_y * 2))

            P1_img0 = cv2.imread('src/images/face/' + str(P1_face) + '0.png')
            B10, G10, R10 = cv2.split(P1_img0)
            P1_img1 = cv2.imread('src/images/face/' + str(P1_face) + '1.png')
            B11, G11, R11 = cv2.split(P1_img1)
            P2_img0 = cv2.imread('src/images/face/' + str(P2_face) + '0.png')
            B20, G20, R20 = cv2.split(P2_img0)
            P2_img1 = cv2.imread('src/images/face/' + str(P2_face) + '1.png')
            B21, G21, R21 = cv2.split(P2_img1)
            P1_direct = cv2.imread('src/images/P1direct.png')
            B1, G1, R1 = cv2.split(P1_direct)
            P2_direct = cv2.imread('src/images/P2direct.png')
            B2, G2, R2 = cv2.split(P2_direct)
            space_img = cv2.imread('src/images/space.png')
            B3, G3, R3 = cv2.split(space_img)

            if bg_choice == 0:
                img0_P1 = cv2.merge([B10, G10, R10])
                img0_P1 = pygame.surfarray.make_surface(cv2.rotate(img0_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P1 = cv2.merge([B11, G11, R11])
                img1_P1 = pygame.surfarray.make_surface(cv2.rotate(img1_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img0_P2 = cv2.merge([B20, G20, R20])
                img0_P2 = pygame.surfarray.make_surface(cv2.rotate(img0_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P2 = cv2.merge([B21, G21, R21])
                img1_P2 = pygame.surfarray.make_surface(cv2.rotate(img1_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P1 = cv2.merge([B1, G1, R1])
                d_P1 = pygame.surfarray.make_surface(cv2.rotate(d_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P2 = cv2.merge([B2, G2, R2])
                d_P2 = pygame.surfarray.make_surface(cv2.rotate(d_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                space_img = cv2.merge([B3, G3, R3])
                space_img = pygame.surfarray.make_surface(cv2.rotate(space_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            elif bg_choice == 1:
                #G0 - 25, R0, G0 + 96
                img0_P1 = cv2.merge([G10 - 25, R10, G10 + 96])
                img0_P1 = pygame.surfarray.make_surface(cv2.rotate(img0_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P1 = cv2.merge([G11 - 25, R11, G11 + 96])
                img1_P1 = pygame.surfarray.make_surface(cv2.rotate(img1_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img0_P2 = cv2.merge([G20 - 25, R20, G20 + 96])
                img0_P2 = pygame.surfarray.make_surface(cv2.rotate(img0_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P2 = cv2.merge([G21 - 25, R21, G21 + 96])
                img1_P2 = pygame.surfarray.make_surface(cv2.rotate(img1_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P1 = cv2.merge([G1 - 25, R1, G1 + 96])
                d_P1 = pygame.surfarray.make_surface(cv2.rotate(d_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P2 = cv2.merge([G2 - 25, R2, G2 + 96])
                d_P2 = pygame.surfarray.make_surface(cv2.rotate(d_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                space_img = cv2.merge([G3 - 25, R3, G3 + 96])
                space_img = pygame.surfarray.make_surface(cv2.rotate(space_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            elif bg_choice == 2:
                #G0 + 79, B0 - 72, R0 - 74
                img0_P1 = cv2.merge([G10 + 79, B10 - 72, R10 - 74])
                img0_P1 = pygame.surfarray.make_surface(cv2.rotate(img0_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P1 = cv2.merge([G11 + 79, B11 - 72, R11 - 74])
                img1_P1 = pygame.surfarray.make_surface(cv2.rotate(img1_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img0_P2 = cv2.merge([G20 + 79, B20 - 72, R20 - 74])
                img0_P2 = pygame.surfarray.make_surface(cv2.rotate(img0_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P2 = cv2.merge([G21 + 79, B21 - 72, R21 - 74])
                img1_P2 = pygame.surfarray.make_surface(cv2.rotate(img1_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P1 = cv2.merge([G1 + 79, B1 - 72, R1 - 74])
                d_P1 = pygame.surfarray.make_surface(cv2.rotate(d_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P2 = cv2.merge([G2 + 79, B2 - 72, R2 - 74])
                d_P2 = pygame.surfarray.make_surface(cv2.rotate(d_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                space_img = cv2.merge([G3 + 79, B3 - 72, R3 - 74])
                space_img = pygame.surfarray.make_surface(cv2.rotate(space_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
            else:
                #G0, R0, G0
                img0_P1 = cv2.merge([G10, R10, G10])
                img0_P1 = pygame.surfarray.make_surface(cv2.rotate(img0_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P1 = cv2.merge([G11, R11, G11])
                img1_P1 = pygame.surfarray.make_surface(cv2.rotate(img1_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img0_P2 = cv2.merge([G20, R20, G20])
                img0_P2 = pygame.surfarray.make_surface(cv2.rotate(img0_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                img1_P2 = cv2.merge([G21, R21, G21])
                img1_P2 = pygame.surfarray.make_surface(cv2.rotate(img1_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P1 = cv2.merge([G1, R1, G1])
                d_P1 = pygame.surfarray.make_surface(cv2.rotate(d_P1, cv2.ROTATE_90_COUNTERCLOCKWISE))
                d_P2 = cv2.merge([G2, R2, G2])
                d_P2 = pygame.surfarray.make_surface(cv2.rotate(d_P2, cv2.ROTATE_90_COUNTERCLOCKWISE))
                space_img = cv2.merge([G3, R3, G3])
                space_img = pygame.surfarray.make_surface(cv2.rotate(space_img, cv2.ROTATE_90_COUNTERCLOCKWISE))


            img0_P1.set_colorkey(rm_back[bg_choice])
            img0_P1 = pygame.transform.scale(img0_P1, (face_size, face_size))
            img1_P1.set_colorkey(rm_back[bg_choice])
            img1_P1 = pygame.transform.scale(img1_P1, (face_size, face_size))
            img0_P2.set_colorkey(rm_back[bg_choice])
            img0_P2 = pygame.transform.scale(img0_P2, (face_size, face_size))
            img1_P2.set_colorkey(rm_back[bg_choice])
            img1_P2 = pygame.transform.scale(img1_P2, (face_size, face_size))
            d_P1.set_colorkey(rm_back[bg_choice])
            d_P1 = pygame.transform.scale(d_P1, (face_size * 3 // rate, face_size * 4 // rate))
            d_P2.set_colorkey(rm_back[bg_choice])
            d_P2 = pygame.transform.scale(d_P2, (face_size * 3 // rate, face_size * 4 // rate))
            space_img.set_colorkey(rm_back[bg_choice])
            space_img = pygame.transform.scale(space_img, (face_size * 6 // rate, face_size // rate))

            #操作
            screen.blit(pygame.transform.flip(d_P1, True, False), (face_size, screen_height - face_size * 6 // rate))
            screen.blit(pygame.transform.flip(d_P2, True, False), (screen_width - face_size * 5 // rate, screen_height - face_size * 6 // rate))    
            screen.blit(space_img, (screen_width // 2 - face_size * 6 // rate // 2, screen_height - face_size * 3 // rate))    
            
            
            spce_text = direct_font.render("Space to determine", True, bg_color[bg_choice][1])
            screen.blit(spce_text, (screen_width // 2 - spce_text.get_width() // 2, screen_height - face_size * 5 // rate // 2 - spce_text.get_height() // 2))
                

            #選擇表情
            screen.blit(pygame.transform.scale(body_img[bg_choice][0], (face_size, face_size)), (screen_width // 2 - face_size - face_distance, screen_height // 2 - face_size))
            screen.blit(pygame.transform.scale(body_img[bg_choice][1], (face_size, face_size)), (screen_width // 2 - face_size - face_distance, screen_height // 2 + face_tweack))
            screen.blit(pygame.transform.scale(body_img[bg_choice][0], (face_size, face_size)), (screen_width // 2 + face_distance, screen_height // 2 - face_size))
            screen.blit(pygame.transform.scale(body_img[bg_choice][1], (face_size, face_size)), (screen_width // 2 + face_distance, screen_height // 2 + face_tweack))
            
            screen.blit(img0_P1, (screen_width // 2 - face_size - face_distance, screen_height // 2 - face_size))
            screen.blit(img1_P1, (screen_width // 2 - face_size - face_distance, screen_height // 2 + face_tweack))
            screen.blit(img0_P2, (screen_width // 2 + face_distance, screen_height // 2 - face_size))
            screen.blit(img1_P2, (screen_width // 2 + face_distance, screen_height // 2 + face_tweack))


            if t % 100 == 0:
                state = 1 - state
            t += 1


if __name__ == "__main__":
    print(choose_color())
    #choose_face()