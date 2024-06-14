import pygame
import cv2
import numpy as np

# 初始化Pygame
pygame.init()

# 設定視窗大小
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("YUYU大作戰")
width = 500  # 按鈕置中

# 設定遊戲幀率
fps = 60
clock = pygame.time.Clock()

# 設定背景顏色
background_color = (70, 10, 80)

# 設定遊戲標題圖片
title_img = pygame.image.load("src/images/Dora.png")
title_img = pygame.transform.scale(title_img, (500, 200))
title_img_rect = title_img.get_rect()
title_img_rect.center = (screen_width // 2, 180)

# 設定教學圖片
teach_img = pygame.image.load("src/images/teaching.JPG")
teach_img = pygame.transform.scale(teach_img, (1284, 720))
teach_img_rect = teach_img.get_rect()
teach_img_rect.center = (screen_width // 2, screen_height // 2)

# 使用 OpenCV 處理按鈕圖片
def load_and_process_image(path, size, color_diff=30):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, size)
    processed_images = []
    for i in range(2):
        adjusted_img = np.clip(img - color_diff * i, 0, 255).astype(np.uint8)
        processed_images.append(adjusted_img)
    return processed_images

# 設定按鈕圖片處理
button_size = (300, 80)
img_button = load_and_process_image("src/images/Space.png", button_size)

# 將 OpenCV 圖片轉換為 Pygame 表面
def convert_to_pygame_surface(images):
    return [pygame.surfarray.make_surface(np.rot90(img)) for img in images]

button_surfaces = convert_to_pygame_surface(img_button)

# 設定按鈕位置
start_img_rect = button_surfaces[0].get_rect()
start_img_rect.topleft = (width, 350)

teaching_img_rect = button_surfaces[0].get_rect()
teaching_img_rect.topleft = (width, 450)

quit_img_rect = button_surfaces[0].get_rect()
quit_img_rect.topleft = (width, 550)

# 設定按鈕文字
font = pygame.font.Font(None, 50)
start_text = font.render("Start", True, (70, 10, 80))
teaching_text = font.render("Teaching", True, (70, 10, 80))
quit_text = font.render("Quit", True, (70, 10, 80))

# 設定按鈕文字位置
start_text_rect = start_text.get_rect()
start_text_rect.center = start_img_rect.center
teaching_text_rect = teaching_text.get_rect()
teaching_text_rect.center = teaching_img_rect.center
quit_text_rect = quit_text.get_rect()
quit_text_rect.center = quit_img_rect.center

def teaching():
    while True:
        screen.fill(background_color)
        screen.blit(teach_img, teach_img_rect)
        font = pygame.font.Font(None, 50)
        click_text = font.render("Click anywhere to return home", True, (255, 255, 255))
        click_text_rect = click_text.get_rect()
        click_text_rect.center = (screen_width // 2, 200)
        screen.blit(click_text, click_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return


def start_loop():
    # 遊戲迴圈
    running = True
    while running:
        
        # 更新遊戲畫面
        screen.fill(background_color)
        screen.blit(title_img, title_img_rect)

        # 檢測鼠標懸停事件
        mouse_pos = pygame.mouse.get_pos()
        if start_img_rect.collidepoint(mouse_pos):
            screen.blit(button_surfaces[1], start_img_rect.topleft)
        else:
            button_surfaces[0].set_colorkey((0, 0, 0))
            screen.blit(button_surfaces[0], start_img_rect.topleft)

        if teaching_img_rect.collidepoint(mouse_pos):
            screen.blit(button_surfaces[1], teaching_img_rect.topleft)
        else:
            button_surfaces[0].set_colorkey((0, 0, 0))
            screen.blit(button_surfaces[0], teaching_img_rect.topleft)

        if quit_img_rect.collidepoint(mouse_pos):
            screen.blit(button_surfaces[1], quit_img_rect.topleft)
        else:
            button_surfaces[0].set_colorkey((0, 0, 0))
            screen.blit(button_surfaces[0], quit_img_rect.topleft)

        screen.blit(start_text, start_text_rect)
        screen.blit(teaching_text, teaching_text_rect)
        screen.blit(quit_text, quit_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_img_rect.collidepoint(mouse_pos):
                    return "YUYU"
                elif teaching_img_rect.collidepoint(mouse_pos):
                    teaching()
                elif quit_img_rect.collidepoint(mouse_pos):
                    running = False

        pygame.display.flip()
        clock.tick(fps)




