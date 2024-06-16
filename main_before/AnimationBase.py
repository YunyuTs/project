# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 19:37:35 2021

@author: t7410
"""

import pygame

#設定顏色
white = (255,255,255)
black = (0, 0, 0)
red = (255, 0, 0)

#類別 動畫基礎類別，繼承自圖像精靈
class AnimationBase(pygame.sprite.Sprite):
	#物件 建構函數
	def __init__(self, x, y, images=None, image_size=(100,100)):
		
		#呼叫 父類別建構函數
		pygame.sprite.Sprite.__init__(self)
		
		#動畫圖像變數(屬性)
		self.animationImages = None;
		
		#檢查輸入圖像是否存在，圖像存在時
		if images is not None:
			#檢查圖像格式，若圖像不是串列格式時，轉換為串列格式
			#isinstance(images, list):
			if type(images) != type([]):			
				images = [images]
			for i in range(len(images)):
				images[i] = pygame.transform.scale(images[i],image_size)
			
		else: #輸入圖像為空時，建立畫布，畫上紅色的圓
			images = pygame.Surface(image_size).convert()
			images.fill(white)
			pygame.draw.circle(images,red,(image_size[0]//2,image_size[1]//2),image_size[1]//2)
			#設定為串列格式
			images = [images]
			
		#設定動畫圖像
		self.animationImages = images;
		#圓像框數
		self.frames = len(self.animationImages)		
		#設定圖像變數
		self.image = self.animationImages[0]	
		
		#讀取背景顏色
		self.colorkey =self.image.get_at((1,1))
		
		#設定透明色
		self.image.set_colorkey(self.colorkey)
		#圖像矩形
		self.rect = self.image.get_rect()
		#矩形定位
		self.rect.center = (x, y)		
	
		
		#動畫變數
		#畫框計數變數
		self.frame = 0
		#畫面重複播放數 同一畫框重複播放數. 預設值為5.
		self.playRepeatCount = 5		
		#畫面重複播放計數變數
		self.repeatCounter = 0
		
	
	#更新資料	
	def update(self):
		#更新位置
		self.updatePosition()
		
		#更新圖像
		if self.frames > 1:
			self.updateImage()
	
	#更新位置
	def updatePosition(self):
		pass
	
	#更新圖像
	def updateImage(self):		
		#print('play frame:', self.frame, ' repeat:', self.repeatCounter)
		#畫面重複播放計數變數 + 1
		self.repeatCounter += 1
		
		#畫面重複播放結束
		if self.repeatCounter >= self.playRepeatCount and self.frame < self.frames - 1:
			self.repeatCounter = 0
			#換下一張圖像
			self.frame += 1
			self.image = self.animationImages[self.frame]			

		#畫框播放完畢，重置畫框變數
		if self.frame >= self.frames - 1 and self.repeatCounter >= self.playRepeatCount:
			self.frame=0
