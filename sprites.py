import pygame
import time
import random
import settings

characterY = 500
characterWidth = 60
curLevel = 0
levelCnt = settings.levelCnt
heights = [[] for i in range(levelCnt)]
# majority of player class is useless as the movement centers around the platform
# only attributes used for player are probably the y and x for certain comparisons, and the idx for which platform it's on
class Player():
    def __init__(self, x, y, width, img, clock):
        self.x = x
        self.y = y
        self.width = width
        self.xVel = 0
        self.yVel = 0
        self.grav = -2
        self.friction = .3
        self.img = img
        self.clock = clock
        self.rotationList = []
        self.ground = 600
        self.cnt = 0
        self.idx = 0
        for i in range(24):
            self.rotationList.append(pygame.transform.rotate(self.img, i * 15))
    def display(self, screen):
        screen.blit(self.img, self.img.get_rect(center = (self.x, self.y)))
    def moveLeft(self):
        self.xVel = -5
    def moveRight(self):
        self.xVel = 5
    def updateIdx(self, idx):
        self.idx = idx
    def callResistance(self):
        # self.yVel -= self.grav
        if (self.xVel < 0):
            self.xVel += self.friction
            self.xVel = min(self.xVel, 0)
        elif (self.xVel > 0):
            self.xVel -= self.friction
            self.xVel = max(self.xVel, 0)
    def updateGround(self, ground):
        self.ground = ground
    def jump(self):
        self.yVel = -20
    def move(self):
        # will be commented out for the horizontal movement as the only movement should be background not character itself
        if ((self.xVel > 0 and self.x + self.xVel + self.width / 2 > 800) or (self.xVel < 0 and self.x + self.xVel - self.width / 2 < 0)):
            if (self.xVel > 0 and self.x + self.xVel + self.width / 2 > 800):
                self.x = 800 - self.width / 2
            else:
                self.x = self.width / 2
            self.xVel = 0
        else: 
            self.x += self.xVel
        if (self.y + self.yVel + self.width / 2 > self.ground):
            self.img = self.rotationList[0]
            self.cnt = 0
            self.y = self.ground - self.width / 2
            self.yVel = 0
        else:
            self.y += self.yVel
    def rotate(self, check):
        if (not(check)):
            self.img = self.rotationList[self.cnt]
            self.cnt += 1
            if (self.cnt == 12):
                self.cnt = 0
        else:
            self.img = self.rotationList[self.cnt]
            self.cnt -= 1
            if (self.cnt == -1):
                self.cnt = 11
    def check(self):
        if (self.y + self.width / 2 <= self.ground):
            self.yVel = 0



class Cloud():
    def __init__(self, screen):
        self.screen = screen
        self.circCnt = random.randint(3, 5)
        self.lowerBound = random.randint(100, 250)
        self.circList = []
        self.color = random.randint(220, 255)
        self.velocity = random.uniform(0.5,0.7)
        self.curX = random.randint(800, 815)
        for i in range(0, self.circCnt):
            self.circList.append([random.randint(self.curX, self.curX + 15), random.randint(self.lowerBound, self.lowerBound + 20)])
            self.curX += 20
    def move(self):
        for i in range(self.circCnt):
            self.circList[i][0] -= self.velocity
    def display(self):
        for i in range(self.circCnt):
            pygame.draw.circle(self.screen, (self.color, self.color, self.color), (self.circList[i][0], self.circList[i][1]), 25)






class Platform():
    def __init__(self, screen, x, y, width):
        self.screen = screen
        self.originalX = x
        self.originalY = y
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.acceleration = -1
        self.friction = 0.3
        self.width = width
        self.grav = -2
        self.ground = y
        self.cY = characterY
        self.cWidth = characterWidth
        self.POP = False
        self.curIdx = 0
        self.color = (0, 180, 0)
    def updateCurIdx(self, idx):
        self.curIdx = idx
    def updateTrue(self):
        self.POP = True
    def updateFalse(self):
        self.POP = False
    def updateGround(self, grnd):
        self.ground = grnd
    def display(self):
        pygame.draw.rect(self.screen, self.color, pygame.Rect(self.x, self.y, self.width, 25))
    def moveLeft(self):
        self.xVel = 7
    def setIdx(self, idx):
        self.idx = idx
    def moveRight(self):
        self.xVel = -7
    # using gravity and friction
    # this is not "real" physics, but serves the same purpose, as the equation implemented in class did not simulate good looking jumps
    def callResistance(self):
        if (self.yVel < 0 and (self.y + self.yVel < (self.cY + (heights[curLevel][self.idx] - heights[curLevel][self.curIdx])))):
            self.y = self.cY + (heights[curLevel][self.idx] - heights[curLevel][self.curIdx])
            self.yVel = 0
        else:
            self.y += self.yVel
            self.yVel += self.grav

        if (self.xVel < 0):
            self.xVel += self.friction
            self.xVel = min(self.xVel, 0)
        elif (self.xVel > 0):
            self.xVel -= self.friction
            self.xVel = max(self.xVel, 0)
    
    # moving all direcitons
    def move2(self):
        self.yVel += self.acceleration
        self.x += self.xVel
        self.y += self.yVel

    # only moving x
    def move(self):
        self.x += self.xVel
    
    # resetting platforms vertically
    def vertMove(self):
        if (self.yVel < 0 and self.y + self.yVel < self.cY + self.cWidth / 2 and self.y >= self.cY + self.cWidth / 2 and self.POP):
            self.y = self.cY
            self.yVel = 0
            return True
        return False

    # jumping
    def jump(self):
        self.yVel = 24

    # resetting platforms horiziontally
    def reset(self):
        if (self.y > 0 and self.y <= (self.cY + (heights[curLevel][self.idx] - heights[curLevel][self.curIdx]))):
            self.move2()
            return False
        # self.y = 1000
        self.y = 3000
        return True

    def resetX(self):
        self.x = self.originalX
    
    # display info
    def dInfo(self):
        print("IDX: " + str(self.idx))
        print(self.y)
        print(self.originalY)
        print(self.yVel)
        
    
# just a platform that changes color
class TempPlatform(Platform):
    def __init__(self, screen, x, y, width):
        super().__init__(screen, x, y, width)
        self.time = -1
    def tickDown(self):
        # change from 0 Red to 255 Red
        # if Red == 255, change from 178 Green to 0 Green
        # if Green == 0, disappear platform, but check will be in main loop
        if (self.color[0] == 255):
            self.color = (self.color[0], max(self.color[1] - 15, 0), self.color[2])
        else:
            self.color = (min(255, self.color[0] + 15), self.color[1], self.color[2])
    def tickUp(self):
        # change from 0 Green to 178 Green
        # change from 255 Red to 0 Red
        if (self.color[1] == 180):
            self.color = (max(self.color[0] - 5, 0), self.color[1], self.color[2])
        else:
            self.color = (self.color[0], min(180, self.color[1] + 5), self.color[2])

# just a black platform
class EndPlatform(Platform):
    def __init__(self, screen, x, y, width):
        super().__init__(screen, x, y, width)
        self.color = (0, 0, 0)
    
    