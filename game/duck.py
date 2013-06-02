import os, sys, random
import pygame
import states
from registry import adjpos, adjrect, adjwidth, adjheight

FRAME_SIZE = adjpos (81, 75)
XOFFSET, YOFFSET = adjpos (250, 225)
FLYOFF_YOFFSET = YOFFSET + adjheight (155)
FALL_YOFFSET = YOFFSET + adjheight (235)

class Duck(object):

    def __init__(self, registry):
        self.registry = registry
        self.imageReversed = False
        self.isDead = False
        self.isFinished = False
        self.flyOff = False
        self.sprites = registry.get('sprites')
        self.rsprites = registry.get('rsprites')

        # Animation
        self.animationDelay = 8
        self.frame = 0
        self.animationFrame = 0
        self.justShot = False

        # Find a starting position
        surface = registry.get('surface')
        x = random.choice([0, surface.get_width()])
        y = random.randint(0, surface.get_height() / 2)
        self.position = x, y

        # Find direction
        self.changeDirection()

    def update(self):
        surface = self.registry.get('surface')
        self.frame = (self.frame + 1) % self.animationDelay
        x, y = self.position

        # Update position
        self.position = (x + self.dx), (y + self.dy)
        if not self.isDead or not self.isFinished:
            self.changeDirection()

        # If they have flown off they are good as dead to us
        frameWidth, frameHeight = FRAME_SIZE
        pastLeft = (x + frameWidth) < 0
        pastTop = (y + frameHeight) < 0
        pastRight = x > surface.get_width()
        if self.flyOff and (pastLeft or pastTop or pastRight):
            self.isFinished = True

    def render(self):
        surface = self.registry.get('surface')
        width, height = FRAME_SIZE
        x, y = self.position

        # If we are finished, don't just return
        if self.isFinished:
            return

        # Set offsets
        xOffset = XOFFSET
        yOffset = FLYOFF_YOFFSET if self.flyOff else YOFFSET

        # Only update animation on key frames
        if self.frame == 0:
            self.animationFrame += 1
        animationFrame = 1 if (self.animationFrame % 4 is 3) else (self.animationFrame % 4)

        # Animate flying
        if not self.isDead:
            rect = ((width * animationFrame) + xOffset), yOffset, width, height
            surface.blit(self.rsprites if self.imageReversed else self.sprites, self.position, rect)

        # Animate the duck drop
        else:
            # First frame is special
            if self.justShot:
                if self.frame == 0:
                    self.justShot = False
                y -= self.dy
                self.position = (x, y)
                rect = XOFFSET, FALL_YOFFSET, width, height
                return surface.blit(self.sprites, self.position, rect)

            # Animate falling
            if y < (surface.get_height() / 2):
                rect = (XOFFSET + width), FALL_YOFFSET, width, height
                return surface.blit(self.sprites, self.position, rect)
            else:
                self.isFinished = True
                self.registry.get('soundHandler').enqueue('drop')

    def isShot(self, pos):
        x1, y1 = self.position
        x2, y2 = pos
        frameX, frameY = FRAME_SIZE

        # If the duck is already dead or flying off, they can't be shot
        if self.flyOff or self.isDead:
            return False

        # If shot was outside the duck image
        if x2 < x1 or x2 > (x1 + frameX):
            return False
        if y2 < y1 or y2 > (y1 + frameY):
            return False

        # Prepare for the fall
        self.isDead = True
        self.justShot = True
        self.frame = 1
        self.dx, self.dy = adjpos (0, 4)
        return True

    def changeDirection(self):
        surface = self.registry.get('surface')
        round = self.registry.get('round')
        frameWidth, frameHeight = FRAME_SIZE
        speedRange = range(4+round, 6+round)
        x, y = self.position
        coinToss = 1 if random.randint(0, 1) else -1

        # Only update on key frames
        if not self.frame == 0:
            return

        # Set flyoff
        if self.flyOff:
            self.dx, self.dy = adjpos (0, -4)
            return

        # Die!
        if self.isDead:
            self.dx, self.dy = adjpos (0, 4)
            return

        # At the left side of the screen
        if x <= 0:
            while True:
                self.dx = random.choice(speedRange)
                self.dy = random.randint(-4, 4)
                self.dx, self.dy = adjpos (self.dx, self.dy)
                if not self.dy == 0:
                    break

        # At the right side of the screen
        elif (x + frameWidth) > surface.get_width():
            while True:
                self.dx = random.choice(speedRange) * -1
                self.dy = random.randint(-4, 4)
                self.dx, self.dy = adjpos (self.dx, self.dy)
                if not self.dy == 0:
                    break

        # At the top of the screen
        elif y <= 0:
            while True:
                self.dx = random.choice(speedRange) * coinToss
                self.dy = random.randint(2, 4)
                self.dx, self.dy = adjpos (self.dx, self.dy)
                if not self.dx == 0:
                    break

        # At the bottom of the screen
        elif y > (surface.get_height() / 2):
            while True:
                self.dx = random.choice(speedRange) * coinToss
                self.dy = random.randint(-4, -2)
                self.dx, self.dy = adjpos (self.dx, self.dy)
                if not self.dx == 0:
                    break

        # Reverse image if duck is flying opposite direction
        if self.dx < 0 and not self.imageReversed:
            self.imageReversed = True
        elif self.dx > 0 and self.imageReversed:
            self.imageReversed = False
