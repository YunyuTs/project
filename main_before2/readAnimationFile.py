# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 18:51:09 2021

@author: t7410
"""

import os
import pygame

def getImagesFromDirectory(imageDir, namePrefix, numPics , targetSize = (0,0), startIndex=0, flipX=False):
	
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