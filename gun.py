import os, sys
import pygame

class Gun(object):
    def __init__(self, surface):
        self.surface = surface 
        self.mouseImg = pygame.image.load(os.path.join('media', 'crosshairs.png'))
        self.mousePos = (0,0)
        self.sounds = {
            'blast': os.path.join('media', 'blast.mp3'),
            'drop': os.path.join('media', 'drop.mp3'),
            'hit': os.path.join('media', 'hit.mp3'),
            'point': os.path.join('media', 'point.mp3'),
            'quack': os.path.join('media', 'quack.mp3')}
        self.rounds = 3

    def render(self):
        self.surface.blit(self.mouseImg, self.mousePos)

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

        pygame.mixer.music.load(self.sounds['blast'])
        pygame.mixer.music.play()
        self.rounds = self.rounds - 1
        return True
