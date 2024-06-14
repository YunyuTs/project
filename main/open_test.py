import pygame
import time
from start import start_loop, screen, screen_width, screen_height

# Load the logo image
logo_image = pygame.image.load("src/images/Dora.png")
logo_image = pygame.transform.scale(logo_image, (350, 200))

# Set the logo position
logo_x = (screen_width - logo_image.get_width()) // 2
logo_y = (screen_height - logo_image.get_height()) // 2

# Set the animation duration
animation_duration = 5  # in seconds

# Start time of the animation
start_time = time.time()

def home_page():
    # Main game loop
    running = True
    while running:
        # Clear the screen
        screen.fill((230, 230, 230))

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time

        # Draw the logo if the animation is still running
        if elapsed_time < animation_duration/2:
            alpha = int(255 * (elapsed_time / (animation_duration/2)))
            logo_image.set_alpha(alpha)
            screen.blit(logo_image, (logo_x, logo_y))
        elif elapsed_time < animation_duration:
            alpha = int(255 * (1 - (elapsed_time - animation_duration/2) / (animation_duration/2)))
            logo_image.set_alpha(alpha)
            screen.blit(logo_image, (logo_x, logo_y))

        # Update the display
        pygame.display.flip()

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check for mouse click to skip the animation
            if event.type == pygame.MOUSEBUTTONDOWN and elapsed_time < animation_duration:
                running = False
                
        # Exit the loop if the animation duration has passed
        if elapsed_time >= animation_duration:
            running = False

    # Start the main menu loop
    start_loop()


if __name__ == "__main__":
    home_page()
