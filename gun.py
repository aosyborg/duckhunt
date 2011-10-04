import os, sys
import pygame

SHOT_BG_POSITION = 60, 440
SHOT_POSITION = 60, 440
SHOT_RECT = 0, 43, 70, 43
BULLET_RECT = 200, 59, 13, 17

class Gun(object):
    def __init__(self, surface):
        self.surface = surface
        self.mouseImg = pygame.image.load(os.path.join('media', 'crosshairs.png'))
        self.mousePos = (0,0)
        self.rounds = 3
        self.blastSound = os.path.join('media', 'blast.mp3')
        self.shotImgs = pygame.image.load(os.path.join('media', 'screenobjects.png'))

    def render(self):
        self.surface.blit(self.mouseImg, self.mousePos)
        self.surface.blit(self.shotImgs, SHOT_POSITION, SHOT_RECT)

        # Show the rounds left
        startingX, startingY = SHOT_POSITION
        for i in range(self.rounds):
            x = startingX + 10 + (i * 20)
            y = startingY + 5
            self.surface.blit(self.shotImgs, (x, y), BULLET_RECT)

    def reloadIt(self):
        self.rounds = 3

    def moveCrossHairs(self, pos):
        xOffset = self.mouseImg.get_width() / 2
        yOffset = self.mouseImg.get_height() / 2
        x, y = pos
        self.mousePos = (x - xOffset), (y - yOffset)

    def shoot(self):
        if self.rounds <= 0:
            return False

        pygame.mixer.music.load(self.blastSound)
        pygame.mixer.music.play()
        self.rounds = self.rounds - 1
        return True
