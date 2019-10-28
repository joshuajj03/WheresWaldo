# Wack.py
# Whack-a-mole game using pygame


import pygame, random, sys, time
from pygame.locals import *
from pygame.font import *

pygame.init()

# some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (47, 79, 79)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
BLUE = (0, 0, 255)



WINDOWWIDTH = 1547
WINDOWHEIGHT = 1000
WALDOWIDTH = 30
WALDOHEIGHT = 50
CURSORHEIGHT = 32
CURSORWIDTH = 32
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
points = 0
BASICFONTSIZE = 40
ENDFONTSIZE = 160
BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
ENDFONT = pygame.font.Font('freesansbold.ttf', ENDFONTSIZE)
ENDSURF = ENDFONT.render('GAME OVER', True, RED)
soundEffect = pygame.mixer.Sound('ha-got-eeem.wav')
FPS = 60



background = pygame.transform.scale(pygame.image.load("background.jpg"), (WINDOWWIDTH, WINDOWHEIGHT))







def main():
    global startTime, searchTime, wack, cursor, FPSCLOCK
    FPSCLOCK = pygame.time.Clock()
    startTime = time.time()
    searchTime = 60
    wack = Waldo()
    cursor = MagnifyingGlass()
    pygame.display.set_caption('Wack')
    isPlaying = True
    pygame.mouse.set_visible(False)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if isPlaying:
                if event.type == MOUSEMOTION:
                    cursor.moveGlass(event.pos)
                if event.type == MOUSEBUTTONUP:
                    if wack.waldoRect.colliderect(cursor.cursorRect):
                        wack.reincarnate()

        if( time.time() - startTime>= searchTime):
            isPlaying = False
            DISPLAYSURF.blit(ENDSURF, (325, 400))


        if(isPlaying):
            updateScreen()
            updatePoints()
            updateTime()
        FPSCLOCK.tick(FPS)
        pygame.display.update()











class Waldo():

    def __init__(self):
        self.waldoImage = pygame.transform.scale(pygame.image.load("waldo.png"), (WALDOWIDTH, WALDOHEIGHT))
        self.waldoRect = self.waldoImage.get_rect()
        self.xpos = random.randrange(WINDOWWIDTH - WALDOWIDTH)
        self.ypos = random.randrange(100, WINDOWHEIGHT - WALDOHEIGHT)
        self.waldoRect.topleft = (self.xpos, self.ypos)

    def reincarnate(self):
        resetSearch()
        self.xpos = random.randrange(WINDOWWIDTH - WALDOWIDTH)
        self.ypos = random.randrange(WINDOWHEIGHT - WALDOHEIGHT)
        self.waldoRect.topleft = (self.xpos, self.ypos)
        soundEffect.play()



class MagnifyingGlass():

    def __init__(self):
        self.glassImg = pygame.transform.scale(pygame.image.load("glass.png"), (CURSORWIDTH, CURSORHEIGHT))
        self.cursorRect = self.glassImg.get_rect()

    def moveGlass(self, center):
        self.cursorRect.center = center
        
        






def resetSearch():
    global points, startTime, searchTime
    points += 1
    startTime = time.time()
    if (points > 20):
        searchTime = 15
    elif (points > 15):
        searchTime = 20
    elif (points > 10):
        searchTime = 30
    elif (points > 5):
        searchTime = 45
    else:
        searchTime = 60

def updateScreen():

    DISPLAYSURF.blit(background, (0, 0))
    DISPLAYSURF.blit(wack.waldoImage, wack.waldoRect)
    DISPLAYSURF.blit(cursor.glassImg, cursor.cursorRect)

def updatePoints():
    POINTS_SURF = BASICFONT.render("Points: " + str(points) , True, BLACK)
    DISPLAYSURF.blit(POINTS_SURF, (500, 30))

def updateTime():
    POINTS_SURF = BASICFONT.render("Time Remaining: " + str(int(searchTime - (time.time() - startTime))), True, BLACK)
    DISPLAYSURF.blit(POINTS_SURF, (750, 30))



main()




