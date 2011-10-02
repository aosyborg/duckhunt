import os, sys, time
import pygame
import gun, duck
from gun import Gun
from duck import Duck

class Driver(object):
    def __init__(self, surface):
        self.surface = surface
        self.gun = Gun(surface)
        self.ducks = [Duck(surface), Duck(surface)]
        self.round = 1
        self.phase = 'shoot'
        self.score = 0
        self.birdCount = 10
        self.timer = int(time.time())
        self.roundTime = 10 # Seconds in a round

    def handleEvent(self, event):
        # If we are in the shooting phase, pass event off to the gun
        if event.type == pygame.MOUSEMOTION:
            self.gun.moveCrossHairs(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gunFired = self.gun.shoot()
            for duck in self.ducks:
                if gunFired:
                    if (duck.isShot(event.pos)):
                        self.score = self.score + 10
                        self.birdCount = self.birdCount - 1
                else:
                     duck.flyOff = True

    def update(self):
        allDone = False

        # Update all ducks
        for duck in self.ducks:
            duck.update()

        self.manageRound()


    def render(self):
        for duck in self.ducks:
            duck.render()
        self.gun.render()

    def manageRound(self):
        timer = int(time.time())

        # Check round end
        timesUp = (timer - self.timer) > self.roundTime
        if not (timesUp or (self.ducks[0].isFinished and self.ducks[1].isFinished)):
            return

        # Let any remaining ducks fly off
        for duck in self.ducks:
            if not duck.isDead:
                duck.flyOff = True
                return

        # Populate screen with new ducks
        self.ducks = [Duck(self.surface), Duck(self.surface)]
        self.timer = int(time.time())
        self.gun.reloadIt()
