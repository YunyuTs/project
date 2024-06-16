# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:18:46 2021

@author: t7410
"""
import pygame
import readAnimationFile
import random
from AnimationBase import AnimationBase

pygame.init()

# #類別 鳥類類別，繼承自動畫基礎類別
# class Bird(AnimationBase):
# 	#物件 建構函數
# 	def __init__(self, x, y, dx=5,  images=None, image_size=(100,100)):
# 		#呼叫 父類別建構函數
# 		AnimationBase.__init__(self, x, y,images, image_size)
# 		self.dx = dx
# 		self.dy = 0
		
# 	#更新位置
# 	def updatePosition(self):
# 		self.rect.move_ip(self.dx, self.dy)
# 		if self.rect.left > screen_width:
# 			self.rect.top = random.randint(10,screen_height//2)
# 			self.rect.right = -100

# #類別 岩石類別，繼承自動畫基礎類別
# class Rock(AnimationBase):
# 	#物件 建構函數
# 	def __init__(self, x, y, dy=5, images=None, image_size=(100,100)):
# 		#呼叫 父類別建構函數
# 		AnimationBase.__init__(self, x, y,images, image_size)
# 		self.dx = 0
# 		self.dy = dy
		
# 	#更新位置
# 	def updatePosition(self):
# 		self.rect.move_ip(self.dx, self.dy)
# 		if self.rect.top > screen_height:
# 			self.rect.left = random.randint(10,screen_width-10)
# 			self.rect.bottom = -100
			

#設定畫面大小
screen_width = 1200
screen_height = 700
screen_size = (screen_width, screen_height)

#設定顏色
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)
#設定主畫布與標題
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('動畫')

# #載入背景圖
# background_image = pygame.image.load("forest2.jpg").convert()
# background_image = pygame.transform.scale(background_image,screen.get_size())

#設定讀入圖像顯示大小		
img_size = (320, 320)

#讀入動畫圖像
# imgs_explosion1 = readAnimationFile.getImagesFromDirectory("imgDir","explosion1/exp", 5, img_size, 1)
# imgs_parrot= readAnimationFile.getImagesFromSpiteSheet("image_sheet/parrot2_3x3.png",3,3)
# imgs_bee1 = readAnimationFile.getImagesFromDirectory("imgDir","bee1.png/1d7cc2b4d7e94fe5f2c89185a0845f69lJuvE63aweIKAMcM-",15,img_size)
#imgs_lama = readAnimationFile.getImagesFromDirectory("imgDir","lama.png/7cdafdf64bdc477bbd8f63e089f323c1ZCYFmFgHa8KXUORy-",29,img_size)
imgs_prop = readAnimationFile.getImagesFromDirectory("src", "images/prop/", 11)
#建立群組
# Assuming imgs_prop and imgs_lama are lists of Pygame Surface objects

allGroup = pygame.sprite.Group()

# Use the scaled images when creating the AnimationBase objects
prop = AnimationBase(0, 0, images=imgs_prop, image_size=(48,48))
allGroup.add(prop)

# #建立物件2
# parrot = Bird(100,500,5,images=imgs_parrot)
# #加入群組
# allGroup.add(parrot)

#建立時鐘物件
clock = pygame.time.Clock()
fps = 60

#迴圈控制變數
run = True
start_time = pygame.time.get_ticks()
while run:
	#播放速度控制
	clock.tick(fps)

	#群組資料更新
	allGroup.update()

	#繪製背景
	screen.fill(white)

	#群組繪製圖像
	allGroup.draw(screen)

	#pygame.draw.rect(screen, black, (0, 0, 48, 48))

	# Remove prop from allGroup after 5 seconds
	current_time = pygame.time.get_ticks()
	if current_time - start_time >= 5000:
		allGroup.remove(prop)

	#event handler
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()

pygame.quit()	