# Sources
# https://www.geeksforgeeks.org/how-to-rotate-and-scale-images-using-pygame/#:~:text=To%20scale%20the%20image%20we,manually%20according%20to%20our%20need.
# https://stackoverflow.com/questions/39201171/pygame-smoother-movement
# https://www.geeksforgeeks.org/pygame-drawing-objects-and-shapes/#:~:text=To%20draw%20a%20circle%20in,circle()%20function.

# other sources used that were referenced in the rock paper scissors project:
# https://www.geeksforgeeks.org/python-display-text-to-pygame-window/
# https://www.geeksforgeeks.org/how-to-rotate-and-scale-images-using-pygame/#:~:text=To%20scale%20the%20image%20we,manually%20according%20to%20our%20need.
# https://www.tutorialspoint.com/python/time_clock.htm

 

"""
What is the game?
- Platformer where the player attempts to reach the black platform at the end.

Inputs:
Up arrow to jump
Left and right arrows to move left and right.
Down arrow to shift downward throuh a platform

Special Platforms:

Green platforms are normal (no special)
Certain platforms change color and will disappear soon

Quick Note: The game does have sound, so make sure to not have volume high before starting the game


Code for User: Have to change file paths for 2 lines. 
- Line 59 in main should go to the image CharacterV3 in the Images Folder
- Line 2 in settings should be a file path to the jumpsound file in the Audio folder




Level Solutions:

Level 1 - Simple jumps

Level 2 - Probably the same as Level 1 but easier

Level 3 - Press down key at the starting platform
        - Rest is up to skill
"""
# did not use the pygame.sprite.Group() function since the need of differentiating between different sprites in the all sprites prevents certain movements from being generalized as a whole

import pygame
import time
import random
import sprites
from pygame.sprite import Sprite
import settings
import Level1
import Level2
import Level3
pygame.init()
pygame.mixer.init()
screen = settings.screen
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
tcImg  = pygame.image.load(r'C:\Users\S.Lin25\OneDrive - Bellarmine College Preparatory\Intro to Computer Programming\Python Files\Game\Images\CharacterV3.png')
width = 60
clock = pygame.time.Clock()
tcImg = pygame.transform.scale(tcImg, (width, width))
testC = sprites.Player(400, 500 - width / 2, width, tcImg, clock)


levels = [0]*settings.levelCnt

levels[0] = Level1.platforms
levels[1] = Level2.platforms
levels[2] = Level3.platforms

curLevel = 0
sprites.curLevel = curLevel

# function to draw text
def draw_text(text, size, color, x, y):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# defining the order in which the loops should check for platform collision
for i in range(len(levels)):
    for j in range(len(levels[i])):
        sprites.heights[i].append(levels[i][j].y)

for j in range(len(levels)):
    for i in range(len(levels[j])):
        levels[j][i].setIdx(i)



# defining clouds and defining locations

clouds = []
for i in range(4):
    clouds.append(sprites.Cloud(screen))
for i in range(len(clouds[1].circList)):
    clouds[1].circList[i][0] += 275
for i in range(len(clouds[2].circList)):
    clouds[2].circList[i][0] += 550
for i in range(len(clouds[3].circList)):
    clouds[3].circList[i][0] += 825
success = False

# tracking which platforms are "phasable"
bannedIndices = []

enteredOnce = False
gameWon = False

curTime = 0
startTime = -1
# game loop
while True:
    clock.tick(60)
    bannedIndices = []
    screen.fill((0, 255, 255))
    # basic game loop event checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not enteredOnce:
                enteredOnce = True
                startTime = time.time()
                curTime = 0
    # checking whether user has chosen to enter the level or not
    if (not enteredOnce):
        screen.fill(WHITE)
        draw_text("PRESS ENTER TO START Level " + str(curLevel + 1), 25, BLACK, settings.WIDTH / 2, settings.HEIGHT / 2)
        pygame.display.update()
        continue
    # checking if user has won the game and displaying text accordingly

    
    if (gameWon):
        time.sleep(0.4)
        testC = sprites.Player(400, 500 - width / 2, width, tcImg, clock)
        screen.fill(WHITE)
        if (curLevel + 1 != settings.levelCnt):
            draw_text("CONGRATS! You Beat Level " + str(curLevel + 1) + " in " + str(curTime) + " seconds", 25, BLACK, settings.WIDTH / 2, settings.HEIGHT / 2)
            pygame.display.update()
            enteredOnce = False
            sprites.curLevel += 1
            curLevel += 1
            gameWon = False
            time.sleep(2)
            continue
        else:
            draw_text("CONGRATS! You Beat The Game!", 25, BLACK, settings.WIDTH / 2, settings.HEIGHT / 2)
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        quit()


    keys = pygame.key.get_pressed()



    # getting keyboard inputs and responding accordingly
    if keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]:
        pass
    elif keys[pygame.K_RIGHT]:
        for i in range(len(levels[curLevel])):
            levels[curLevel][i].moveRight()
    elif keys[pygame.K_LEFT]:
        for i in range(len(levels[curLevel])):
            levels[curLevel][i].moveLeft()
    if keys[pygame.K_UP] and levels[curLevel][testC.idx].y == 500:
        # testC.jump()
        pygame.mixer.music.load(settings.jumpSound)
        pygame.mixer.music.play()
        for i in range(len(levels[curLevel])):
            levels[curLevel][i].jump()
    if keys[pygame.K_DOWN] and levels[curLevel][testC.idx].y == 500:
        bannedIndices.append(testC.idx)
        for i in range(len(levels[curLevel])):
            levels[curLevel][i].yVel = -2

    # move and display clouds
    for i in range(len(clouds)):
        if (clouds[i].circList[len(clouds[i].circList) - 1][0] + 25 < 0):
            clouds[i] = sprites.Cloud(screen) 
        clouds[i].move()
        clouds[i].display()
    

    foundGround = False
    for i in range(len(levels[curLevel])):
        # exclude banned platforms from stopping the player
        if (i in bannedIndices):
            continue
        # check what platform the player is on, and update all platforms accordingly
        if (levels[curLevel][i].x <= testC.x + testC.width / 2 and levels[curLevel][i].x + levels[curLevel][i].width >= testC.x - testC.width / 2 and levels[curLevel][i].y >= (int)(testC.y) + testC.width / 2):
            if (type(levels[curLevel][i]) == sprites.TempPlatform and levels[curLevel][i].color[1] == 0):
                continue
            foundGround = True
            testC.updateIdx(i)
            for j in range(len(levels[curLevel])):
                levels[curLevel][j].updateFalse()
                levels[curLevel][j].updateCurIdx(i)
            levels[curLevel][i].updateTrue()
    # checks if player has reached final platform
    if (type(levels[curLevel][testC.idx]) == sprites.EndPlatform and levels[curLevel][testC.idx].y == 500):
        gameWon = True
    
    
    # moving all platforms
    for i in range(len(levels[curLevel])):
        if (levels[curLevel][i].POP and type(levels[curLevel][i]) == sprites.TempPlatform):
            levels[curLevel][i].tickDown()
        elif (type(levels[curLevel][i]) == sprites.TempPlatform):
            levels[curLevel][i].tickUp()
        if (type(levels[curLevel][i]) == sprites.TempPlatform and levels[curLevel][i].color[1] == 0):
            bannedIndices.append(i)
        levels[curLevel][i].move()
        levels[curLevel][i].callResistance()
        if (type(levels[curLevel][i]) == sprites.TempPlatform and i in bannedIndices):
            foundGround = False
            continue
        levels[curLevel][i].display()

    # reset the rotation if the player is touching a platform, or else keep rotating
    if (levels[curLevel][testC.idx].y - testC.width / 2 == testC.y):
        testC.img = testC.rotationList[0]
    else:
        time.sleep(0.01)
        if (levels[curLevel][0].xVel <= 0):
            testC.rotate(True)
        else:
            testC.rotate(False)
    if (not(foundGround) and levels[curLevel][testC.idx].y == levels[curLevel][testC.idx].cY):
        pass
    else:
        foundGround = True
    # checking if player is falling and not on a platform
    if (not foundGround):
        testC.updateIdx(0)
        while not foundGround:
            clock.tick(60)
            for i in range(len(levels[curLevel])):
                if (i in bannedIndices):
                    continue
                # check if player has reached a platform after falling
                if (levels[curLevel][i].x <= testC.x + testC.width / 2 and levels[curLevel][i].x + levels[curLevel][i].width >= testC.x - testC.width / 2 and levels[curLevel][i].y >= testC.y + testC.width / 2 and levels[curLevel][i].y < 3000):
                    if (type(levels[curLevel][i]) == sprites.TempPlatform and levels[curLevel][i].color[1] == 0):
                        continue
                    foundGround = True
                    testC.updateIdx(i)
                    for j in range(len(levels[curLevel])):
                        levels[curLevel][j].updateFalse()
                        levels[curLevel][j].updateCurIdx(i)
                    levels[curLevel][i].updateTrue()
            if (foundGround):
                break

            x = True
            screen.fill((0, 255, 255))
            # continue to move clouds even when falling
            for f in range(len(clouds)):
                if (clouds[f].circList[len(clouds[f].circList) - 1][0] + 25 < 0):
                    clouds[f] = sprites.Cloud(screen) 
                clouds[f].move()
                clouds[f].display()
            for i in range(len(levels[curLevel])):
                val = levels[curLevel][i].reset()
                x = x and val
                testC.display(screen)
                if (type(levels[curLevel][i]) == sprites.TempPlatform and i in bannedIndices):
                    continue
                levels[curLevel][i].display() 
                
            draw_text(str(curTime), 25, BLACK, settings.WIDTH * 9 / 10, settings.HEIGHT * 1/10)
            t = int(time.time() - startTime)

            if (t != curTime):
                curTime = t
            pygame.display.update()
            if (x):
                for i in range(len(levels[curLevel])):
                    levels[curLevel][i].resetX()
                break
    else:
        draw_text(str(curTime), 25, BLACK, settings.WIDTH * 9 / 10, settings.HEIGHT * 1/10)
        x = int(time.time() - startTime)

        if (x != curTime):
            curTime = x
        testC.display(screen)
        pygame.display.update()

