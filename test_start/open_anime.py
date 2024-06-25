import pygame
import time
from start import start_loop, screen, screen_width, screen_height
import os

# Load the logo images
logo1_image = pygame.image.load("src/images/yuyu.png")
logo1_image = pygame.transform.scale(logo1_image, (450, 450))
logo2_image = pygame.image.load("src/images/soga.png")
logo2_image = pygame.transform.scale(logo2_image, (350, 300))

# Set the animation duration
animation_duration = 3  # in seconds

# 動畫音效
pygame.mixer.init()

# Start time of the animation
start_time = time.time()

def animate_logo(logo_image, logo_x, logo_y, start_time, animation_duration):
    # logo_x = (screen_width - logo_image.get_width()) // 2
    # logo_y = (screen_height - logo_image.get_height()) // 2
    elapsed_time = time.time() - start_time
    # Draw the logo if the animation is still running
    if elapsed_time < animation_duration / 2:
        alpha = int(255 * (elapsed_time / (animation_duration / 2)))
        logo_image.set_alpha(alpha)
        screen.blit(logo_image, (logo_x, logo_y))
    elif elapsed_time < animation_duration:
        alpha = int(255 * (1 - (elapsed_time - animation_duration / 2) / (animation_duration / 2)))
        logo_image.set_alpha(alpha)
        screen.blit(logo_image, (logo_x, logo_y))

# Main game loop
running = True
played_sound_soga = False
played_sound_cat = False
while running:
    # Clear the screen
    screen.fill((216, 214, 211))

    # Calculate the total elapsed time
    total_elapsed_time = time.time() - start_time

    # Determine which logo to display
    if total_elapsed_time < animation_duration:
        if not played_sound_soga:
            pygame.mixer.music.load('src/sound/opening_sound/soga.mp3')
            pygame.mixer.music.set_volume(1.0)  # Set volume to maximum (1.0)
            pygame.mixer.music.play()
            played_sound_soga = True
        animate_logo(logo2_image, 480, 190, start_time, animation_duration)
    elif total_elapsed_time < 2 * animation_duration:
        if not played_sound_cat:
            pygame.mixer.music.load('src/sound/opening_sound/cat_sweet_voice1.mp3')
            pygame.mixer.music.set_volume(0.5)  # Set volume to default (0.5)
            pygame.mixer.music.play()
            played_sound_cat = True
        animate_logo(logo1_image, 420, 100, start_time + animation_duration, animation_duration)
    else:
        # Exit the loop if the total animation duration has passed
        running = False

    # Update the display
    pygame.display.flip()

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        # Check for mouse click to skip the animation
        if event.type == pygame.MOUSEBUTTONDOWN:
            running = False

# Start the main menu loop
start_loop()
