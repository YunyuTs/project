import pygame
import cv2
import numpy as np

# 初始化Pygame
pygame.init()

# 設定視窗大小
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tag you're it!")
width = 500  # 按鈕置中

# 設定遊戲幀率
fps = 60
clock = pygame.time.Clock()

# 設定背景
background = pygame.image.load("src/images/background.png")
background = pygame.transform.scale(background, (screen_width * 2, screen_height))
speed = 0.5

#透明視窗
window = pygame.Surface((screen_width, screen_height))
window.set_alpha(150)
window.fill((0, 0, 0))

# 設定遊戲標題圖片
title_img = pygame.image.load("src/images/Tag.png")
title_img = pygame.transform.scale(title_img, (720, 430))
title_img_rect = title_img.get_rect()
title_img_rect.center = (700, 200)

# 設定教學圖片
teach_img = pygame.image.load("src/images/teaching.jpg")
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
    global x
    while True:
        screen.blit(teach_img, teach_img_rect)
        font = pygame.font.Font(None, 50)
        click_text = font.render("\"Click anywhere to return home\"", True, (255, 255, 255))
        click_text_rect = click_text.get_rect()
        click_text_rect.center = (screen_width // 2, 180)
        screen.blit(click_text, click_text_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return


color_diff = 30

font =  pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 80)
pvp = [font.render("PvP", True, (93, 30, 104)), font.render("PvP", True, (93 - color_diff, 30 - color_diff, 104 - color_diff))]
pve = [font.render("PvE", True, (93, 30, 104)), font.render("PvE", True, (93 - color_diff, 30 - color_diff, 104 - color_diff))]
pve_hard = [font.render("PvE Hard", True, (93, 30, 104)), font.render("PvE Hard", True, (93 - color_diff, 30 - color_diff, 104 - color_diff))]
distance = 300
dy = 100
tweak = 120
button_width = pvp[0].get_width() + tweak * 2
button_height = pvp[0].get_height() + 30

img = pygame.image.load("src/images/space.png")
img = pygame.transform.scale(img, (button_width, button_height))
img.set_colorkey((0, 0, 0))
img_cv = cv2.imread("src/images/space.png")
b, g, r = cv2.split(img_cv)
img_cv = cv2.merge([b - color_diff, g - color_diff, r - color_diff])
img_cv = pygame.surfarray.make_surface(cv2.rotate(img_cv, cv2.ROTATE_90_CLOCKWISE))
img_cv.set_colorkey((256 - color_diff, 256 - color_diff, 256 - color_diff))
img_cv = pygame.transform.scale(img_cv, (button_width, button_height))

imgs = [img, img_cv]


def start_loop():
    #背景音樂
    pygame.mixer.init()
    pygame.mixer.music.load("src/sound/opening_sound//Sinya_no_hotcocoa.mpga")
    pygame.mixer.music.play(-1, start=5.0)
    x = 0 # 背景滾動
    s = 0 # 選擇模式
    
    m_pvp = 0 # 選擇模式
    m_pve = 0 # 選擇模式
    m_pve_hard = 0 # 選擇模式

    # 遊戲迴圈
    running = True
    while running:
        #繪製背景
        screen.blit(background.subsurface(x, 0, screen_width, screen_height), (0, 0))
        x += speed
        if x >= screen_width: x = 0
        #繪製透明視窗
        screen.blit(window, (0, 0))
        
        if s == 0:
            # 繪製遊戲標題
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
                    return 0
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_img_rect.collidepoint(mouse_pos):
                        s = 1
                    elif teaching_img_rect.collidepoint(mouse_pos):
                        teaching()
                    elif quit_img_rect.collidepoint(mouse_pos):
                        return 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
        else:
            screen.blit(imgs[m_pvp], (screen_width // 2 - button_width // 2 - distance, screen_height // 2 - button_height // 2))
            screen.blit(pvp[m_pvp], (screen_width // 2 - pvp[0].get_width() // 2 - distance, screen_height // 2 - pvp[0].get_height() // 2))

            screen.blit(imgs[m_pve], (screen_width // 2 - button_width // 2 + distance, screen_height // 2 - button_height // 2 - dy))
            screen.blit(pve[m_pve], (screen_width // 2 - pve[0].get_width() // 2 + distance, screen_height // 2 - pve[0].get_height() // 2 - dy))

            screen.blit(imgs[m_pve_hard], (screen_width // 2 - button_width // 2 + distance, screen_height // 2 - button_height // 2 + dy))
            screen.blit(pve_hard[m_pve_hard], (screen_width // 2 - pve_hard[0].get_width() // 2 + distance, screen_height // 2 - pve_hard[0].get_height() // 2 + dy))

            m_x, m_y = pygame.mouse.get_pos()

            if screen_width // 2 - button_width // 2 - distance < m_x < screen_width // 2 - button_width // 2 - distance + button_width and screen_height // 2 - button_height // 2 < m_y < screen_height // 2 - button_height // 2 + button_height:
                m_pvp = 1
                if pygame.mouse.get_pressed()[0]:
                    return 1
            else:
                m_pvp = 0

            if screen_width // 2 - button_width // 2 + distance < m_x < screen_width // 2 - button_width // 2 + distance + button_width and screen_height // 2 - button_height // 2 - dy < m_y < screen_height // 2 - button_height // 2 - dy + button_height:
                m_pve = 1
                if pygame.mouse.get_pressed()[0]:
                    return 2
            else:
                m_pve = 0

            if screen_width // 2 - button_width // 2 + distance < m_x < screen_width // 2 - button_width // 2 + distance + button_width and screen_height // 2 - button_height // 2 + dy < m_y < screen_height // 2 - button_height // 2 + dy + button_height:
                m_pve_hard = 1
                if pygame.mouse.get_pressed()[0]:
                    return 3
            else:
                m_pve_hard = 0



            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0


        # 更新遊戲畫面
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    print(start_loop())


