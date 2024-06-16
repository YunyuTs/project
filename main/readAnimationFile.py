# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 18:51:09 2021

@author: t7410
"""

import os
import pygame

#適用於檔案號碼可為單位數字者
def getImagesFromDirectory(imageDir, namePrefix, numPics , targetSize = (0,0), startIndex=0, flipX=False):
    '''
	函數功能: 從目錄中讀取動續圖像, 設定成圖像串列
	
	參數說明:
	imgDir : 字串
		動畫圖像的目錄
	namePrefix : 字串
		檔案名稱前綴	
	numPics : 整數
		動畫圖像數量
	targetSize : 二值整數元組
		設定圖像尺寸，(0,0)表示不變更
	startIndex : 整數
		檔案編號開始值，預設值為 0
    flipX: Bool
        左右互換
	
	'''
	
    images = []
    for num in range(startIndex, startIndex + numPics):
        filename = f"{imageDir}/{namePrefix}{num}.png"

        if not os.path.isfile(filename):
            print(filename + " 檔案不存在 !!!!!!!!!!!!!!!!!!!!!")
            break
		
        img = pygame.image.load(filename).convert_alpha()        
        
        if flipX == True:
            img = pygame.transform.flip(img, flipX, False)
        if targetSize[0]>0:
            img = pygame.transform.scale(img, (targetSize))
        images.append(img)
    return images

#適用於檔案號碼為雙位數字者
def getImagesFromDirectory2(imageDir, namePrefix, namePostFix, numPics , targetSize = (0,0) , startIndex=0, flipX=False):
	'''
	函數功能: 從目錄中讀取動續圖像, 設定成圖像串列
	
	參數說明:
	imgDir : 字串
		動畫圖像的目錄
	namePrefix : 字串
		檔案名稱前綴	
	namePostfix : 字串
		檔案名稱後綴	
	numPics : 整數
		動畫圖像數量
	targetSize : 二值整數元組
		設定圖像尺寸，(0,0)表示不變更
	startIndex : 整數
		檔案編號開始值，預設值為 0
    flipX: Bool
        左右互換
	
	'''
	
	images = []
	for num in range(startIndex, startIndex + numPics):
		filename = f"{imageDir}/{namePrefix}{num:02d}{namePostFix}.png"
		if not os.path.isfile(filename):
			print(filename + "  檔案不存在 !!!!!!!!!!!!!!!!!!!!!")
			break
		img = pygame.image.load(filename).convert_alpha()
		if flipX == True:
			img = pygame.transform.flip(img, flipX, False)
		if targetSize[0]>0:
			img = pygame.transform.scale(img, targetSize)
		images.append(img)
	return images	

		
def getImagesFromSpiteSheet(imgFilename, cols, rows, targetSize = (0,0), flipX=False):
	'''
	函數功能: 從圖像表單中讀取動畫圖像，設定成圖像串列

	參數說明
	----------
	imgFilename : 字串
		動畫圖像表單的名稱
	cols : 整數
		圖像表單中圖像行數.
	rows : 數整
		圖像表單中圖像列數.
	targetSize : 二值整數元組, optional
		設定讀取圖像的尺寸. 預設值為 (0,0).

	回傳值
	-------
	images : 圖像串列
		讀取到的圖像串列.

	'''
	if not os.path.isfile(imgFilename):
		print(imgFilename + "  檔案不存在 !!!!!!!!!!!!!!!!!!!!!")
		return []
		
	
	image_sheet = pygame.image.load(imgFilename).convert_alpha()
	images = []
	imgWidth, imgHeight = image_sheet.get_size()

	w,h = imgWidth // cols ,imgHeight //rows
	for i in range(rows):
		for j in range(cols):
			img = image_sheet.subsurface( ( j * w, i*h, w, h ) )
			if flipX == True:
				img = pygame.transform.flip(img, flipX, False)
			if targetSize[0]>0:
				img = pygame.transform.scale(img,targetSize)
			images.append( img )
	return images


