import pygame
import math
#from player import player

pygame.init()
#background music
# def load_music():
#     """Load the music"""
#     song1 = 'src/sound/background.ogg'
#     pygame.mixer.music.load(song1)
#     pygame.mixer.music.play(-1)
    
# load_music()



#設定顏色
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)

width = 700
height = 70

klick_width = 50
klick_height = 100

def main():

    song = ['src/sound/state0.wav', 'src/sound/state1.wav']
    volume = 0.3
    change_volume = volume / 3
    pygame.mixer.music.set_volume(volume)
    a = int(pygame.mixer.Sound(song[0]).get_length() * 81)
    change = pygame.mixer.Sound('src/sound/change.wav')
    change.set_volume(change_volume)
    print(a)
    x = 1

    #設定畫面大小
    screen_width = 1280
    screen_height = 720
    screen_size = (screen_width, screen_height)
    #設定主畫布與標題
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('test_song')

    #------------------
    screen.fill(black)
    #------------------


    #建立時鐘物件
    clock = pygame.time.Clock()
    fps = 80

    flag = 0
    time = 0

    run = True
    while run:
        
        #播放速度控制
        clock.tick(fps)
        #更新畫面
        pygame.display.flip()
        screen.fill(black)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN : #鍵盤按下事件
                if event.key == pygame.K_ESCAPE:
                    run = False

        if time % a == 0:
            if flag == 0:
                #pygame.mixer.music.stop()
                if time != 0:
                    change.play()
                x = 1 - x
                pygame.mixer.music.load(song[x])
                pygame.mixer.music.play()
                flag = 1
        else:
            flag = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
            time += 1
        

        pygame.draw.rect(screen, white, [(screen_width - width) / 2, 50, width * (time % a) / a, height], 0)
        pygame.draw.rect(screen, red, [(screen_width - width) / 2, 50, width, height], 10)
            
        pygame.draw.rect(screen, white, [(screen_width - width) / 2, 150, width * volume, height], 0)
        pygame.draw.rect(screen, red, [(screen_width - width) / 2, 150, width, height], 10)
        
        pygame.draw.rect(screen, white, [(screen_width - width - klick_width) / 2 + width * volume, 150  + (height - klick_height) / 2, klick_width, klick_height], 0)
        pygame.draw.rect(screen, red, [(screen_width - width - klick_width) / 2 + width * volume, 150  + (height - klick_height) / 2, klick_width, klick_height], 10)
           
        if pygame.mouse.get_pressed()[0]:
            m_x, m_y = pygame.mouse.get_pos()
            if m_x >= (screen_width - width) / 2 and m_x <= (screen_width + width) / 2 and m_y >=  150  + (height - klick_height) / 2 and m_y <=  150  + (height + klick_height) / 2:
                volume = (m_x - (screen_width - width) / 2) / width
                pygame.mixer.music.set_volume(volume)
                change_volume = volume / 3
                change.set_volume(change_volume)

if __name__ == '__main__':
    main()	