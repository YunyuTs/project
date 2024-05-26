# -*- coding: utf-8 -*-
"""
Created on Sat May 18 18:46:02 2024

@author: USER
"""
import pygame
import math

img_player1 = []
img_player2 = []

for i in range(2):
    img = pygame.image.load('src/images/player' + str(0) + str(i) + '.png')
    img_player1.append(pygame.transform.scale(img, (64, 64)))
    img = pygame.image.load('src/images/player' + str(1) + str(i) + '.png')
    img_player2.append(pygame.transform.scale(img, (64, 64)))

class player():
    def __init__(self, x = 300, y = 300, speed = 2, ang = 0, life = 8):
        self.x = x
        self.y = y
        self.speed = speed
        self.ang = ang
        self.life = life

    def move(self):
        self.x -= self.speed * math.sin(math.radians(self.ang))
        self.y -= self.speed * math.cos(math.radians(self.ang))

    def setspeed(self, speed):
        self.speed = speed
