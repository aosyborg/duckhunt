import os, sys, random
import pygame

FRAME_SIZE = 77, 70

class Duck(object):
    def __init__(self, surface):
        self.surface = surface
        self.image = pygame.image.load(os.path.join('media', 'duck.png'))
        self.imageReversed = False
        self.isDead = False
        self.isFinished = False
        self.flyOff = False

        # Animation
        self.animationDelay = 10
        self.frame = 0
        self.animationFrame = 0
        self.justShot = False

        # Find a starting position
        x = random.randint(0, 1)
        y = random.randint(0, surface.get_height() / 2)
        self.position = x, y

        # Find direction
        while True:
            self.dx = random.randint(-4, 4)
            self.dy = random.randint(-4, 4)
            if not self.dx == 0 and not self.dy == 0:
                break

    def update(self):
        self.frame = (self.frame + 1) % self.animationDelay
        x, y = self.position

        # Update position
        self.position = (x + self.dx), (y + self.dy)
        if not self.isDead:
            self.changeDirection()

        # If they have flown off they are good as dead to us
        frameWidth, frameHeight = FRAME_SIZE
        pastLeft = (x + frameWidth) < 0
        pastTop = (y + frameHeight) < 0
        pastRight = x > self.surface.get_width()
        if self.flyOff and (pastLeft or pastTop or pastRight):
            self.isDead = True
            self.isFinished = True

    def render(self):
        width, height = FRAME_SIZE
        x, y = self.position

        # Set offsets
        xOffset, yOffset = FRAME_SIZE
        if not self.imageReversed:
            xOffset = 0

        # Only update animation on key frames
        if self.frame == 0:
            self.animationFrame = (self.animationFrame + 1) % 4

        # Animate flying
        if not self.isDead:
            rect = ((width * self.animationFrame) + xOffset), 0, width, height
            self.surface.blit(self.image, self.position, rect)

        # Animate the duck drop
        else:
            if self.imageReversed:
                self.image = pygame.transform.flip(self.image, True, False)
                self.imageReversed = False

            # First frame is special
            if self.justShot:
                if self.frame == 0:
                    self.justShot = False
                y -= self.dy
                self.position = (x, y)
                rect = (width * 4), height, width, height
                return self.surface.blit(self.image, self.position, rect)

            # Animate falling
            if y < (self.surface.get_height() / 2):
                rect = (width * 4), 0, width, height
                return self.surface.blit(self.image, self.position, rect)
            else:
                self.isFinished = True

    def isShot(self, pos):
        x1, y1 = self.position
        x2, y2 = pos
        frameX, frameY = FRAME_SIZE

        # If shot was outside the duck image
        if x2 < x1 or x2 > (x1 + frameX):
            return False
        if y2 < y1 or y2 > (y1 + frameY):
            return False

        # Prepare for the fall
        self.isDead = True
        self.justShot = True
        self.frame = 1
        self.dy = 4
        self.dx = 0
        return True

    def changeDirection(self):
        x, y = self.position
        frameWidth, frameHeight = FRAME_SIZE

        # Only update on key frames
        if not self.frame == 0:
            return

        # At the left side of the screen
        if x <= 0 and not self.flyOff:
            while True:
                self.dx = random.randint(2, 4)
                self.dy = random.randint(-4, 4)
                if not self.dy == 0:
                    break

        # At the right side of the screen
        elif (x + frameWidth) > self.surface.get_width() and not self.flyOff:
            while True:
                self.dx = random.randint(-4, -2)
                self.dy = random.randint(-4, 4)
                if not self.dy == 0:
                    break

        # At the top of the screen
        elif y <= 0 and not self.flyOff:
            while True:
                self.dx = random.randint(-4, 4)
                self.dy = random.randint(2, 4)
                if not self.dx == 0:
                    break

        # At the bottom of the screen
        elif y > (self.surface.get_height() / 2):
            while True:
                self.dx = random.randint(-4, 4)
                self.dy = random.randint(-4, -2)
                if not self.dx == 0:
                    break

        # Reverse image if duck is flying opposite direction
        if self.dx < 0 and not self.imageReversed:
            self.imageReversed = True
            self.image = pygame.transform.flip(self.image, True, False)
        elif self.dx > 0 and self.imageReversed:
            self.imageReversed = False
            self.image = pygame.transform.flip(self.image, True, False)
