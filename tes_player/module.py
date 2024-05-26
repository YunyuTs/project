import pygame
import math
import random

#turn from center
def blitRotate(surf, image, origin, pivot, angle):
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


#background music
def load_music(song1):
    """Load the music"""
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)


'''
#player move control
def pos(p, key, a, w, s, d):
    if key[a]:
        p.move()
        if key[w]:
            tmp = 45
        elif key[s]:
            tmp = 135
        else:
            tmp = 90
    elif key[d]:
        p.move()
        if key[w]:
            tmp = 315
        elif key[s]:
            tmp = 225
        else:
            tmp = 270
    elif key[w]:
        p.move()
        tmp = 0
    elif key[s]:
        p.move()
        tmp = 180
    else:
        tmp = p.ang
    
    if abs(p.ang - tmp) == 180 or abs(p.ang - tmp) == 90:
        p.ang = tmp
    elif p.ang < tmp and p.ang + 180 > tmp:
        p.ang += 5
    elif p.ang > tmp and p.ang - 180 < tmp:
        p.ang -= 5
    elif p.ang < tmp:
        p.ang += 360
    elif p.ang > tmp:
        p.ang -= 360
    
    return p.ang
'''