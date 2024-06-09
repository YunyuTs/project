import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 設定視窗大小
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('旋轉正方形碰撞並分開')

# 定義顏色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 正方形物體的初始位置、速度、大小
square1 = pygame.Rect(175, 175, 50, 50)
square2 = pygame.Rect(225, 225, 50, 50)
square1_speed = [random.choice([-2, 2]), random.choice([-2, 2])]
square2_speed = [random.choice([-2, 2]), random.choice([-2, 2])]
angle1 = 0
angle2 = 0

# 創建正方形表面
square1_surface = pygame.Surface(square1.size, pygame.SRCALPHA)
square2_surface = pygame.Surface(square2.size, pygame.SRCALPHA)
square1_surface.fill(RED)
square2_surface.fill(BLUE)

# 遊戲主循環
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 更新正方形位置
    square1.move_ip(square1_speed)
    square2.move_ip(square2_speed)

    # 碰撞邊界處理
    if square1.left < 0 or square1.right > 400:
        square1_speed[0] *= -1
    if square1.top < 0 or square1.bottom > 400:
        square1_speed[1] *= -1
    if square2.left < 0 or square2.right > 400:
        square2_speed[0] *= -1
    if square2.top < 0 or square2.bottom > 400:
        square2_speed[1] *= -1

    # 更新旋轉角度
    angle1 += 2
    angle2 += 2

    # 獲取旋轉後的新正方形
    rotated_image1 = pygame.transform.rotate(square1_surface, angle1)
    rotated_image2 = pygame.transform.rotate(square2_surface, angle2)
    rotated_square1 = rotated_image1.get_rect(center=square1.center)
    rotated_square2 = rotated_image2.get_rect(center=square2.center)

    # 檢測碰撞
    collision = rotated_square1.colliderect(rotated_square2)

    # 如果發生碰撞，調整速度方向以90度分開
    if collision:
        #font = pygame.font.SysFont(None, 55)
        #text = font.render('WOW!', True, (0, 128, 0))
        #screen.blit(text, (160, 190))
        square1_speed[0], square1_speed[1] = -square1_speed[1], square1_speed[0]
        square2_speed[0], square2_speed[1] = -square2_speed[1], square2_speed[0]

    # 繪製背景和旋轉正方形物體
    screen.fill(WHITE)
    screen.blit(rotated_image1, rotated_square1.topleft)
    screen.blit(rotated_image2, rotated_square2.topleft)

    # 更新顯示
    pygame.display.flip()
    pygame.time.delay(30)