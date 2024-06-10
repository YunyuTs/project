import pygame
import math

#turn from center
def blitRotate(surf, image, origin, pivot, angle):
    image_rect = image.get_rect(topleft = (origin[0] - pivot[0], origin[1]-pivot[1]))
    offset_center_to_pivot = pygame.math.Vector2(origin) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (origin[0] - rotated_offset.x, origin[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

#--------------------------------------------------------------

#background music
def load_music(song1):
    """Load the music"""
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.load(song1)
    pygame.mixer.music.play(-1)

#--------------------------------------------------------------

# #物件導入
# #設定玩家圖片
# img_player1 = []
# img_player2 = []

# #玩家大小
# player_size = 50

# #load images
# for i in range(2):
#     img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
#     img_player1.append(pygame.transform.scale(img, (player_size, player_size)))
#     img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
#     img_player2.append(pygame.transform.scale(img, (player_size, player_size)))

# #設定衝刺物件圖片
# img_sp = []

# #衝刺物件大小
# sp_size = 32

# #attack music
# attack_sound = pygame.mixer.Sound('src/sound/attack.ogg')


# #load images
# for i in range(2):
#     img = pygame.image.load('src/images/sprint' + str(i) + '.png')
#     img_sp.append(pygame.transform.scale(img, (sp_size, sp_size)))


# #playing game
# def play_game(screen, P1, P2, time, STATE, STATE_flag, flag, t_flag, invince_time, key):
    
#     #偵測鍵盤按鍵
#     if key[pygame.K_v]: #"v":衝刺
#         if flag[0] == 0:
#             if P1.sprint_time <= 0:
#                 P1.setdrift()
#             flag[0] = 1
#     else:
#         flag[0] = 0
        
#     if key[pygame.K_COMMA]: #",":衝刺
#         if flag[1] == 0:
#             if P2.sprint_time <= 0:
#                 P2.setdrift()
#             flag[1] = 1
#     else:
#         flag[1] = 0
    
#     #--------------------------------------------------

#     #偵測碰撞
#     if abs(P1.x - P2.x) < player_size and abs(P1.y - P2.y) < player_size and invince_time <= 0:
#         if t_flag == 0:
#             t_flag = 1
#             attack_sound.play()
#             invince_time = 200
#             if STATE == 0:
#                 P2.life -= 1
#             else:
#                 P1.life -= 1
#     else:
#         t_flag = 0

#     #無敵時間
#     if invince_time > 0:
#         invince_time -= 1
#     if STATE != STATE_flag:
#         invince_time = 0
#         STATE_flag = STATE
    
#     #--------------------------------------------------

#     #完加速度控制
#     P1.setspeed()
#     P2.setspeed()

#     #玩家移動
#     P1.turn_move(key, pygame.K_a, pygame.K_w, pygame.K_s, pygame.K_d)
#     P2.turn_move(key, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT)

#     #--------------------------------------------------

#     #繪製玩家
#     if STATE == 0:
#         P2.drift(screen, img_sp[1 - STATE])
#         P2.draw(screen, img_player2[1 - STATE], invince_time)
#         P1.drift(screen, img_sp[STATE])
#         P1.draw(screen, img_player1[STATE], invince_time)
#         screen.blit(P2.text, (P2.x - (player_size / 5), P2.y - player_size))
#         screen.blit(P1.text, (P1.x - (player_size / 5), P1.y - player_size))
#     else:
#         P1.drift(screen, img_sp[STATE])
#         P1.draw(screen, img_player1[STATE], invince_time)
#         P2.drift(screen, img_sp[1 - STATE])
#         P2.draw(screen, img_player2[1 - STATE], invince_time)
#         screen.blit(P1.text, (P1.x - (player_size / 5), P1.y - player_size))
#         screen.blit(P2.text, (P2.x - (player_size / 5), P2.y - player_size))
    
#     #--------------------------------------------------

#     #狀態切換
#     time += 1
#     if time % 250 == 0:
#         STATE = 1 - STATE
#         P1.state = STATE
#         P2.state = 1 - STATE

