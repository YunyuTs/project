import pygame
import random

# 初始化 Pygame
pygame.init()

# 设置屏幕尺寸
screen = pygame.display.set_mode((800, 600))

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 游戏循环标志
running = True

# # 随机生成一个矩形的位置
# rect_x = random.randint(0, 800)
# rect_y = random.randint(0, 600)

time = 0
touch = False

# 游戏主循环
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景
    screen.fill(WHITE)

    #滑鼠位置
    m_x, m_y = pygame.mouse.get_pos()

    # 绘制随机位置的矩形
    if time % 4000 == 0:
        touch = False
        rect_x = random.randint(0, 800)
        rect_y = random.randint(0, 600)

    #碰撞
    if m_x > rect_x and m_x < rect_x + 50 and m_y > rect_y and m_y < rect_y + 50:
        touch = True

    if not touch:
        pygame.draw.rect(screen, RED, (rect_x, rect_y, 50, 50))


    # 更新时间
    time += 1


    # 更新屏幕
    pygame.display.flip()

# 退出 Pygame
pygame.quit()