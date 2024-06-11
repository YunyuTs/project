import cv2
import pygame

# img = cv2.imread('src/images/player01.png')
# blue, green, red = cv2.split(img)
# bgr_img = cv2.merge([blue, green, red])
# cv2.imshow("B -> G -> R", bgr_img)

# rgb_img = cv2.merge([green, blue, red])
# cv2.imshow("R -> G -> B", rgb_img)
#blue

# rgb_img2 = cv2.merge([blue, red, green])
# cv2.imshow("R -> G", rgb_img2)
#yellow

# rgb_img3 = cv2.merge([green, red, green])
# cv2.imshow("G -> B", rgb_img3)
#green


# cv2.waitKey(0)
# cv2.destroyAllWindows()

img = cv2.imread('src/images/Player0.png')
blue, green, red = cv2.split(img)
body_img = cv2.merge([blue, red, green])

img = cv2.imread('src/images/Player_face10.png')
blue, green, red = cv2.split(img)
face_img = cv2.merge([blue, red, green])


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill((255, 255, 255))

    body_surface = pygame.surfarray.make_surface(cv2.rotate(body_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    body_surface.set_colorkey((0, 0, 0))
    screen.blit(body_surface, (0, 0))

    face_surface = pygame.surfarray.make_surface(cv2.rotate(face_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    face_surface.set_colorkey((0, 0, 0))
    screen.blit(face_surface, (0, 0))

      