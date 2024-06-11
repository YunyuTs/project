import pygame

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
button_width = 100
button_distance = 150
button_y = 600

# Font
text_size = 60
font = pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", text_size) #字體

#讀取圖片
home_img = pygame.image.load('src/images/Home.png')
return_img = pygame.image.load('src/images/return.png')

#設定圖大小
size = (100, 100)
home_img = pygame.transform.scale(home_img, size)
return_img = pygame.transform.scale(return_img, size)

#設定圖片位置
home_img_rect = home_img.get_rect()
home_img_rect.center = (screen_width // 2 - button_width // 2 - button_distance, button_y)
return_img_rect = return_img.get_rect()
return_img_rect.center = (screen_width // 2 + button_width // 2 + button_distance, button_y)

#誰贏了
p1_win = False

#設定畫面
screen = pygame.display.set_mode(screen_size)



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

    #顯示按鈕
    screen.blit(home_img, home_img_rect)
    screen.blit(return_img, return_img_rect)

    #顯示誰贏了
    if p1_win:
        text = font.render('Battle Finish !! Player 1 Wins!', True, text_color)
    else:
        text = font.render('Battle Finish !! Player 2 Wins!', True, text_color)
    text_rect = text.get_rect()
    text_rect.center = (screen_width // 2, screen_height // 2 - 200)
    screen.blit(text, text_rect)

    #檢測按鈕點擊事件
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if home_img_rect.collidepoint(mouse_pos):
            run = False
            #這邊要成接回home畫面
        elif return_img_rect.collidepoint(mouse_pos):
            run = False
            #這邊要改成再來一局
    #更新畫面
    pygame.display.update()

pygame.quit()