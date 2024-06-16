import pygame
import time
import math

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

#time rate
max_size = 120
min_size = 80
time_rate = 80

def count_down(n, color, volume, count):

    #screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    # Set volume
    cd_num.set_volume(volume)
    
    # Countdown from 3 to 1
    if n > 0:
        # Play the countdown sound
        if count == 0:
            cd_num.play()
        
        # Render the countdown number
        countdown_text = font.render(str(n), True, bg_color[color])
        cd_x, cd_y = countdown_text.get_size()
        
        # Scale the countdown number from big to small
        scale = max_size - (max_size - min_size) * math.sin(count / time_rate * math.pi / 2)

        scaled_text = pygame.transform.scale(countdown_text, (scale * cd_x // cd_y, scale))
        scaled_text.set_alpha(255 * (max_size - scale) / (max_size - min_size))
        scaled_rect = scaled_text.get_rect(center=(screen_width/2, screen_height/2))
                
        # Draw the scaled countdown number
        screen.blit(scaled_text, scaled_rect)
                
        # Update the screen
        pygame.display.flip()
                
        # Wait for the given time
        time.sleep(0.25 / time_rate)

    else:
        # Play the "GO!" sound
        if count == 0:
            cd_go.play()

        # Show the word "GO!"
        go_text = font.render("GO!", True, bg_color[color])
        gt_x, gt_y = go_text.get_size()

        scale = max_size - (max_size - min_size) * math.sin(count / (time_rate * 2) * math.pi / 2)

        scaled_text = pygame.transform.scale(go_text, (scale * gt_x // gt_y, scale))
        scaled_text.set_alpha(255 * (max_size - scale) / (max_size - min_size))
        scaled_rect = scaled_text.get_rect(center=(screen_width/2, screen_height/2))


        # Draw the scaled "GO!"
        screen.blit(scaled_text, scaled_rect)

        # Update the screen
        pygame.display.flip()

        # Wait for the given time
        time.sleep(0.25 / (time_rate * 2))
        
    if n == 0 and count + 1 ==time_rate:
        time.sleep(30 / time_rate)

    return count + 1


a = 3
b = 0
if __name__ == "__main__":
    while a >= 0:
        b = count_down(a, 0, 1, b)
        if b == 80:
            a -= 1
            b = 0