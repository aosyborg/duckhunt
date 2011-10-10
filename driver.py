import os, sys, time
import pygame
import gun, duck
from gun import Gun
from duck import Duck

HIT_POSITION = 255, 440
HIT_RECT = 0, 0, 287, 43
HIT_DUCK_POSITION = 339, 445
HIT_DUCK_WHITE_RECT = 217, 43, 19, 16
HIT_DUCK_RED_RECT = 199, 43, 19, 16

class Driver(object):
    def __init__(self, surface):
        self.surface = surface
        self.gun = Gun(surface)
        self.ducks = [Duck(surface), Duck(surface)]
        self.round = 1
        self.phase = 'shoot'
        self.score = 0
        self.timer = int(time.time())
        self.roundTime = 10 # Seconds in a round
        self.controlImgs = pygame.image.load(os.path.join('media', 'screenobjects.png'))
        self.hitDucks = [False for i in range(10)]
        self.hitDuckIndex = 0

    def handleEvent(self, event):
        # If we are in the shooting phase, pass event off to the gun
        if event.type == pygame.MOUSEMOTION:
            self.gun.moveCrossHairs(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gunFired = self.gun.shoot()
            for duck in self.ducks:
                if gunFired:
                    if (duck.isShot(event.pos)):
                        self.score += 10
                        self.hitDucks[self.hitDuckIndex] = True
                        self.hitDuckIndex += 1
                else:
                    duck.flyOff = True
                    self.hitDuckIndex += 1

    def update(self):
        allDone = False

        # Update all ducks
        for duck in self.ducks:
            duck.update()

        self.manageRound()

    def render(self):
        for duck in self.ducks:
            duck.render()

        # Update game controls
        self.surface.blit(self.controlImgs, HIT_POSITION, HIT_RECT)
        startingX, startingY = HIT_DUCK_POSITION
        for i in range(10):
            x = startingX + (19 * i)
            y = startingY
            if self.hitDucks[i]:
                self.surface.blit(self.controlImgs, (x, y), HIT_DUCK_RED_RECT)
            else:
                self.surface.blit(self.controlImgs, (x, y), HIT_DUCK_WHITE_RECT)

        self.gun.render()

    def manageRound(self):
        timer = int(time.time())

        # Check round end
        timesUp = (timer - self.timer) > self.roundTime
        if not (timesUp or (self.ducks[0].isFinished and self.ducks[1].isFinished)):
            return

        # Let any remaining ducks fly off
        for duck in self.ducks:
            if not duck.isFinished:
                duck.flyOff = True
                return

        # Check for fly offs and increment the index
        for duck in self.ducks:
            if duck.flyOff:
                self.hitDuckIndex += 1

        # Start new around if duck index is at the end
        if self.hitDuckIndex >= 9:
            self.round += 1
            self.hitDucks = [False for i in range(10)]
            self.hitDuckIndex = 0

        # Populate screen with new ducks
        self.ducks = [Duck(self.surface), Duck(self.surface)]
        self.timer = int(time.time())
        self.gun.reloadIt()
