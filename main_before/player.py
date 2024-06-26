import pygame
import math
import random
from module import blitRotate #turn from center

# #設定玩家最大最小速度
# max_speed = 8
# min_speed = 3

#角速度
ang_speed = 5

#衝刺延遲時間
sprint_time = 100 #衝刺延遲時間
sprint_duration = 80 #衝刺持續時間
drift_duration = 10 #衝刺遺落物件持續時間

#--------------------------------------------------------------

#衝刺物件
class sprint():
    def __init__(
            self, x, y, #中心點
            direction = 0, speed = 0, #方向, 速度
            o_speed = 0, ang = 0, #原始速度, 角度
            time = 0 #時間
        ):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.o_speed = o_speed
        self.ang = ang
        self.time = time
    
    def drift(self): #移動 旋轉
        self.x += self.speed * math.sin(math.radians(self.ang))
        self.y += self.speed * math.cos(math.radians(self.ang))
        self.direction -= 2

    def setsp(self): #減速度
        self.speed = self.o_speed * math.cos((sprint_time - self.time) / sprint_duration)
    
    def draw(self, screen, img): #畫出物件
        if self.speed > 0 and self.time > 0:
            blitRotate(screen, img, (self.x, self.y), (img.get_width() / 2, img.get_height() / 2), self.direction)

#--------------------------------------------------------------

#玩家基本屬性
class player():
    def __init__(
            self, x = 0, y = 0, #中心點
            speed = 3, ang = 0, #速度, 角度
            life = 8, state = 0, sprint_time = 0, #生命值, 狀態(攻擊, 防禦), 衝刺時間
            drift_parts = [0, 0, 0], #衝刺物件
            max_speed = 8, min_speed = 3, #最大速度, 最小速度
            ):
        self.x = x
        self.y = y
        self.speed = speed
        self.ang = ang
        self.life = life
        self.state = state
        self.sprint_time = sprint_time
        self.drift_parts = drift_parts
        self.max_speed = max_speed
        self.min_speed = min_speed
    
    #--------------------------------------------------------------

    def setpos(self, x, y): #設定位置
        self.x = x
        self.y = y
    
    #--------------------------------------------------------------

    def getpos(self): #取得位置
        return (self.x, self.y)
    
    #--------------------------------------------------------------

    def move(self): #移動
        self.x -= self.speed * math.sin(math.radians(self.ang))
        self.y -= self.speed * math.cos(math.radians(self.ang))
    
    #--------------------------------------------------------------

    def setspeed(self): #速度控制
        if self.sprint_time > 0 and self.speed > self.min_speed + 1: #衝刺速度
            self.speed = self.max_speed + (self.max_speed - self.min_speed) * math.sin(sprint_time - self.sprint_time / drift_duration)
            self.sprint_time -= 1
        else: #基本速度
            self.speed = self.min_speed
            self.sprint_time = 0

    #--------------------------------------------------------------

    def setdrift(self): #衝刺遺落物件
        self.sprint_time = sprint_time
        self.speed = self.max_speed
        for i in range(3):
            o_speed = random.randint(1, 2)
            self.drift_parts[i] = (sprint(self.x, self.y, 0, o_speed, o_speed, random.randint(0, 360), self.sprint_time))
    
    #--------------------------------------------------------------

    def drift(self, screen, img_sp): #衝刺物件(畫出
        if self.drift_parts[0]: #衝刺遺落物件
            if self.drift_parts[0].time > 0 and self.drift_parts[0].speed > 0:
                for i in range(3):
                    self.drift_parts[i].setsp()
                    self.drift_parts[i].drift()
                    self.drift_parts[i].draw(screen, img_sp)
                    self.drift_parts[i].time -= 1
            else:
                for i in range(3):
                    self.drift_parts[i] = 0
    
    #--------------------------------------------------------------

    def draw(self, screen, img, face, invince_time, size): #畫出玩家
        img_tmp = pygame.transform.scale(img, (size, size))
        face_tmp = pygame.transform.scale(face, (size, size))
        if self.state == 0:
            blitRotate(screen, img_tmp, self.getpos(), (size / 2, size / 2), self.ang)
            blitRotate(screen, face_tmp, self.getpos(), (size / 2, size / 2), self.ang)
        elif (invince_time % 50 < 25 or invince_time <= 0):
            blitRotate(screen, img_tmp, self.getpos(), (size / 2, size / 2), self.ang)
            blitRotate(screen, face_tmp, self.getpos(), (size / 2, size / 2), self.ang)

    #--------------------------------------------------------------
    
    def turn_move(self, key, left, up, down, right): #轉向
        if key[left]:
            self.move()
            if key[up]:
                tmp = 45
            elif key[down]:
                tmp = 135
            else:
                tmp = 90
        elif key[right]:
            self.move()
            if key[up]:
                tmp = 315
            elif key[down]:
                tmp = 225
            else:
                tmp = 270
        elif key[up]:
            self.move()
            tmp = 0
        elif key[down]:
            self.move()
            tmp = 180
        else:
            tmp = self.ang

        if abs(self.ang - tmp) == 180 or abs(self.ang - tmp) == 90:
            self.ang = tmp
        elif self.ang < tmp and self.ang + 180 > tmp:
            self.ang += ang_speed
        elif self.ang > tmp and self.ang - 180 < tmp:
            self.ang -= ang_speed
        elif self.ang < tmp:
            self.ang += 360
        elif self.ang > tmp:
            self.ang -= 360

#--------------------------------------------------------------
 
