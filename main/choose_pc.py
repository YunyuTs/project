import pygame
import cv2

pygame.init()

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()
fps = 80

#透明視窗
window = pygame.Surface((screen_width, screen_height))
window.set_alpha(150)
window.fill((0, 0, 0))

color_diff = 30
# text_color = (244,224, 244)
back_color = [(93, 30, 104), (93 - color_diff, 30 - color_diff, 104 - color_diff)]

font =  pygame.font.SysFont("microsoftjhengheimicrosoftjhengheiui", 80)
pvp = [font.render("PvP", True, (93, 30, 104)), font.render("PvP", True, (93 - color_diff, 30 - color_diff, 104 - color_diff))]
pve = [font.render("PvE", True, (93, 30, 104)), font.render("PvE", True, (93 - color_diff, 30 - color_diff, 104 - color_diff))]
pve_hard = [font.render("PvE Hard", True, (93, 30, 104)), font.render("PvE Hard", True, (93 - color_diff, 30 - color_diff, 104 - color_diff))]
distance = 300
dy = 100
tweak = 120
button_width = pvp[0].get_width() + tweak * 2
button_height = pvp[0].get_height() + 30

img = pygame.image.load("src/images/space.png")
img = pygame.transform.scale(img, (button_width, button_height))
img.set_colorkey((0, 0, 0))
img_cv = cv2.imread("src/images/space.png")
b, g, r = cv2.split(img_cv)
img_cv = cv2.merge([b - color_diff, g - color_diff, r - color_diff])
img_cv = pygame.surfarray.make_surface(cv2.rotate(img_cv, cv2.ROTATE_90_CLOCKWISE))
img_cv.set_colorkey((256 - color_diff, 256 - color_diff, 256 - color_diff))
img_cv = pygame.transform.scale(img_cv, (button_width, button_height))

imgs = [img, img_cv]


def choose_pc():

    m_pvp = 0
    m_pve = 0
    m_pve_hard = 0

    screen.blit(window, (0, 0))

    running = True
    while running:
        clock.tick(fps)
        #screen.fill((216, 214, 211))


        #pygame.draw.rect(screen, back_color[m_pvp], (screen_width // 2 - pvp[0].get_width() // 2 - distance - tweak, screen_height // 2 - pvp[0].get_height() // 2 - tweak, pvp[0].get_width() + tweak * 2, pvp[0].get_height() + tweak * 2))
        screen.blit(imgs[m_pvp], (screen_width // 2 - button_width // 2 - distance, screen_height // 2 - button_height // 2))
        screen.blit(pvp[m_pvp], (screen_width // 2 - pvp[0].get_width() // 2 - distance, screen_height // 2 - pvp[0].get_height() // 2))

        #pygame.draw.rect(screen, back_color[m_pve], (screen_width // 2 - pve[0].get_width() // 2 + distance - tweak, screen_height // 2 - pve[0].get_height() // 2 - tweak, pve[0].get_width() + tweak * 2, pve[0].get_height() + tweak * 2))
        screen.blit(imgs[m_pve], (screen_width // 2 - button_width // 2 + distance, screen_height // 2 - button_height // 2 - dy))
        screen.blit(pve[m_pve], (screen_width // 2 - pve[0].get_width() // 2 + distance, screen_height // 2 - pve[0].get_height() // 2 - dy))

        screen.blit(imgs[m_pve_hard], (screen_width // 2 - button_width // 2 + distance, screen_height // 2 - button_height // 2 + dy))
        screen.blit(pve_hard[m_pve_hard], (screen_width // 2 - pve_hard[0].get_width() // 2 + distance, screen_height // 2 - pve_hard[0].get_height() // 2 + dy))

        m_x, m_y = pygame.mouse.get_pos()

        if screen_width // 2 - button_width // 2 - distance < m_x < screen_width // 2 - button_width // 2 - distance + button_width and screen_height // 2 - button_height // 2 < m_y < screen_height // 2 - button_height // 2 + button_height:
            m_pvp = 1
            if pygame.mouse.get_pressed()[0]:
                return "pvp"
        else:
            m_pvp = 0

        if screen_width // 2 - button_width // 2 + distance < m_x < screen_width // 2 - button_width // 2 + distance + button_width and screen_height // 2 - button_height // 2 - dy < m_y < screen_height // 2 - button_height // 2 - dy + button_height:
            m_pve = 1
            if pygame.mouse.get_pressed()[0]:
                return "pve"
        else:
            m_pve = 0

        if screen_width // 2 - button_width // 2 + distance < m_x < screen_width // 2 - button_width // 2 + distance + button_width and screen_height // 2 - button_height // 2 + dy < m_y < screen_height // 2 - button_height // 2 + dy + button_height:
            m_pve_hard = 1
            if pygame.mouse.get_pressed()[0]:
                return "pve_hard"
        else:
            m_pve_hard = 0



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0

        pygame.display.flip()

if __name__ == "__main__":
    print(choose_pc())