import pygame
import cv2
import numpy as np
def finish(p1_win):
    
    #初始化
    pygame.init()

    #設定顏色
    white = (255,255,255)
    black = (0, 0, 0)
    gray = (128, 128, 128)
    background_color = (70, 10, 80)
    text_color = (244, 224, 244)

    #設定畫面大小   
    screen_width = 1280
    screen_height = 720
    screen_size = (screen_width, screen_height)
    clock = pygame.time.Clock()
    fps = 80

    #設定顏色差異、按鈕寬度、按鈕間距
    color_differece = 45
    button_width = 100
    button_distance = 150
    button_y = 600

    # Font
    text_size = 60
    font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", text_size) #字體

    #讀取圖片
    home_img = cv2.imread('src/images/Home.png')
    return_img = cv2.imread('src/images/return.png')
    quit_img = cv2.imread('src/images/Quit.png')

    # Create copies of the original images
    modified_home_img = np.copy(home_img)
    modified_return_img = np.copy(return_img)
    modified_quit_img = np.copy(quit_img)

    # Modify the picture's RGB using color_difference
    modified_home_img[:, :, 0] -= color_differece  # Increase the blue channel
    modified_home_img[:, :, 1] -= color_differece  # Decrease the green channel
    modified_home_img[:, :, 2] -= color_differece  # Increase the red channel

    modified_return_img[:, :, 0] -= color_differece  # Increase the blue channel
    modified_return_img[:, :, 1] -= color_differece  # Decrease the green channel
    modified_return_img[:, :, 2] -= color_differece  # Increase the red channel

    modified_quit_img[:, :, 0] -= color_differece  # Increase the blue channel
    modified_quit_img[:, :, 1] -= color_differece  # Decrease the green channel
    modified_quit_img[:, :, 2] -= color_differece  # Increase the red channel

    #設定圖大小以及方向
    size = (100, 100)
    home_img = pygame.surfarray.make_surface(home_img)
    return_img = pygame.surfarray.make_surface(return_img)
    quit_img = pygame.surfarray.make_surface(quit_img)

    modified_home_img = pygame.surfarray.make_surface(modified_home_img)
    modified_return_img = pygame.surfarray.make_surface(modified_return_img)
    modified_quit_img = pygame.surfarray.make_surface(modified_quit_img)

    home_img = pygame.transform.scale(home_img, size)
    return_img = pygame.transform.scale(return_img, size)
    quit_img = pygame.transform.scale(quit_img, size)

    modified_home_img = pygame.transform.scale(modified_home_img, size)
    modified_return_img = pygame.transform.scale(modified_return_img, size)
    modified_quit_img = pygame.transform.scale(modified_quit_img, size)

    home_img = pygame.transform.rotate(home_img, -90)
    modified_home_img = pygame.transform.rotate(modified_home_img, -90)

    #設定圖片位置
    home_img_rect = home_img.get_rect()
    home_img_rect.center = (screen_width // 2 - button_width // 2 - button_distance, button_y)
    return_img_rect = return_img.get_rect()
    return_img_rect.center = (screen_width // 2 + button_width // 2 + button_distance, button_y)
    quit_img_rect = quit_img.get_rect()
    quit_img_rect.center = (screen_width // 2, button_y)

    #設定畫面
    screen = pygame.display.set_mode(screen_size)

    #誰贏了
    P1_Win = p1_win

    #回首頁、再來一局參數
    home = 0
    replay = 0

    #迴圈
    run = True
    while run:

        #設定背景
        screen.fill((background_color))

        #時間揁數
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #顯示誰贏了
        if P1_Win:
            text = font.render('Battle Finish !! Player 1 Wins!', True, text_color)
        else:
            text = font.render('Battle Finish !! Player 2 Wins!', True, text_color)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2 - 200)
        screen.blit(text, text_rect)

        #檢測按鈕點擊事件
        mouse_pos = pygame.mouse.get_pos()
        if home_img_rect.collidepoint(mouse_pos):
            screen.blit(modified_home_img, home_img_rect)
            screen.blit(return_img, return_img_rect)
            screen.blit(quit_img, quit_img_rect)
        elif return_img_rect.collidepoint(mouse_pos):
            screen.blit(modified_return_img, return_img_rect)
            screen.blit(home_img, home_img_rect)
            screen.blit(quit_img, quit_img_rect)
        elif quit_img_rect.collidepoint(mouse_pos):
            screen.blit(modified_quit_img, quit_img_rect)
            screen.blit(home_img, home_img_rect)
            screen.blit(return_img, return_img_rect)
        else:
            screen.blit(home_img, home_img_rect)
            screen.blit(return_img, return_img_rect)
            screen.blit(quit_img, quit_img_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if home_img_rect.collidepoint(mouse_pos):
                home = 1
                return home
                run = False
                #這邊要成接回home畫面
            elif return_img_rect.collidepoint(mouse_pos):
                replay = 1
                return replay
                run = False
                #這邊要改成再來一局
            elif quit_img_rect.collidepoint(mouse_pos):
                run = False
                #這邊要改成離開遊戲
        #更新畫面
        pygame.display.update()

    pygame.quit()