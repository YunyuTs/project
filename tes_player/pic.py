import cv2
import pygame

img = cv2.imread('src/images/player01.png')
blue, green, red = cv2.split(img)
bgr_img = cv2.merge([blue, green, red])
cv2.imshow("B -> G -> R", bgr_img)

rgb_img = cv2.merge([green - 25, red, green + 96])
cv2.imshow("R -> G -> B", rgb_img)
#yellow
#(159, 229, 159), (55, 124, 55)
#(255, 237, 148), (179, 149, 0)
#(-96, -8, 11), (-124, -25, 55)

rgb_img2 = cv2.merge([green + 79, blue - 72, red - 74])
cv2.imshow("R -> G", rgb_img2)
#blue
#(229, 228, 159), (124, 136, 55)
#(155, 156, 238), (65, 52, 139)
#(74, 72, -79), (59, 84, -84)

rgb_img3 = cv2.merge([green, red, green])
cv2.imshow("G -> B", rgb_img3)
#green


# cv2.waitKey(0)
# cv2.destroyAllWindows()

img = cv2.imread('src/images/Player0.png')
blue, green, red = cv2.split(img)
body_img = cv2.merge([blue, green, red])

img = cv2.imread('src/images/Player_face10.png')
blue, green, red = cv2.split(img)
face_img = cv2.merge([blue, green, red])


screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

while True:
    clock.tick(60)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    screen.fill((244, 224, 244))

    body_surface = pygame.surfarray.make_surface(cv2.rotate(body_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    body_surface.set_colorkey((0, 0, 0))
    screen.blit(body_surface, (0, 0))

    face_surface = pygame.surfarray.make_surface(cv2.rotate(face_img, cv2.ROTATE_90_COUNTERCLOCKWISE))
    face_surface.set_colorkey((0, 0, 0))
    screen.blit(face_surface, (0, 0))

      