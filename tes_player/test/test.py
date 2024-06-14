import pygame
import time

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the font and size
font = pygame.font.Font(None, 100)

# Set the colors
black = (0, 0, 0)
white = (255, 255, 255)
bg_color = [(93, 29, 104), (4, 93, 125), (108, 21, 30), (29, 93, 29)]

#conntdown sound
pygame.mixer.init()
cd_num = pygame.mixer.Sound("src/sound/cd0.wav")
cd_go = pygame.mixer.Sound("src/sound/cd1.wav")

def count_down(n, color, volume):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    #set volume
    cd_num.set_volume(volume)
    # Countdown from 3 to 1
    if n > 0:
        # Play the countdown sound
        cd_num.play()
        
        # Render the countdown number
        countdown_text = font.render(str(i), True, bg_color[color])
        countdown_rect = countdown_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(countdown_text, countdown_rect)
        
        # Update the screen
        pygame.display.flip()
        
        # Wait for 1 second
        time.sleep(1)

    else:
        # Play the "GO!" sound
        cd_go.play()

        # Show the word "GO!"
        go_text = font.render("GO!", True, bg_color[color])
        go_rect = go_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(go_text, go_rect)
        pygame.display.flip()

        # Wait for 2 seconds
        time.sleep(2)

if __name__ == "__main__":
    for i in range(3, -1, -1):
        count_down(i, 1, 0.5)