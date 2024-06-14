import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 创建一个带有 alpha 通道的 Surface
def draw_transparent_circle(surface, color, center, radius, alpha):
    # 创建一个新的 Surface，设置 flags 为 SRCALPHA 以支持透明度
    circle_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    
    # 在新的 Surface 上绘制圆形
    pygame.draw.circle(circle_surface, color + (alpha,), (radius, radius), radius)
    
    # 将圆形 Surface 绘制到目标 Surface 上
    surface.blit(circle_surface, (center[0] - radius, center[1] - radius))

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 填充背景
    screen.fill(WHITE)
    
    # 绘制半透明圆形
    draw_transparent_circle(screen, RED, (400, 300), 100, 128)  # 半透明度值在0到255之间，128是半透明

    # 更新显示
    pygame.display.flip()

# 退出 Pygame
pygame.quit()
sys.exit()