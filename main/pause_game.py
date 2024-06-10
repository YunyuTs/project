import pygame

pygame.init()
    
screen_width = 1280
screen_height = 720
screen_size = (screen_width, screen_height)
clock = pygame.time.Clock()
fps = 80

def pause_game(screen, volume, change_volume, attack_volume):
    window = pygame.Surface(screen_size)
    window.fill((255, 255, 255))
    window.set_alpha(128)
    screen.blit(window, (0, 0))
    run = True
    while run:

        #---------基礎設定---------
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
        
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            return 0

